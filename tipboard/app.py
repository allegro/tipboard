#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json
import logging

from raven.contrib.tornado import SentryMixin, AsyncSentryClient
import tornado.gen
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornadoredis

from tipboard import settings
from tipboard.api import api_version, MetaProperty, TileData, ProjectInfo, Push
from tipboard.parser import process_layout_config, get_config_files_names
from tipboard.redis_utils import db_events_path

log = logging.getLogger(__name__)


class Flipboard(object):

    def __init__(self):
        self.last_found_configs_number = -1
        self.paths = []

    def get_paths(self):
        """
        Returns url paths to dashboards (created from .yaml config from
        userspace).
        """
        config_names = self._get_config_names()
        if len(config_names) != self.last_found_configs_number:
            self.paths = self._config_names2paths(config_names)
            self.last_found_configs_number = len(config_names)
        return self.paths

    def get_flipboard_title(self):
        """
        Returns title to display as a html title.
        """
        title = ''
        config_names = self._get_config_names()
        if len(config_names) == 1:
            config = process_layout_config(config_names[0])
            try:
                title = config['details']['page_title']
            except KeyError:
                msg = 'config {} has no key: details/page_title'.format(
                    config_names[0]
                )
                log.error(msg)
        elif len(config_names) > 1:
            # TODO: put here more suitable title?
            title = 'Flipboard Mode'
        return title

    def _get_config_names(self):
        config_names = settings.FLIPBOARD_SEQUENCE
        if not any(config_names):
            config_names = get_config_files_names()
            if not any(config_names):
                raise Exception('No config (.yaml) file found in ~/.tipboard/')
        return config_names

    def _config_names2paths(self, config_names):
        paths = []
        for name in config_names:
            path = '/' + name
            paths.append(path)
        return paths


class RedisMixin(object):
    """Trivial connection mixin."""

    def setup_redis(self):
        # We don't have to manage reconnections, tornadoredis does that
        # automatically.
        client = tornadoredis.Client(**settings.REDIS_ASYNC)
        client.connect()
        return client


class DashboardSocketHandler(tornado.websocket.WebSocketHandler, RedisMixin,
                             SentryMixin):
    """Handles client connections on web sockets and listens on a Redis
    subscription."""

    cache = set()   # Only cache keys. Values will be retrieved from Redis
                    # every time. This ensures users don't get stale data.
    tipboard_helpers = {
        'color': settings.COLORS,
        'log_level': settings.JS_LOG_LEVEL,
    }

    def __init__(self, *args, **kwargs):
        super(DashboardSocketHandler, self).__init__(*args, **kwargs)
        self.listen()
        self.getter = self.setup_redis()

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def on_close(self):
        log.info('Web socket closed.')
        if self.pubsub.subscribed:
            self.pubsub.unsubscribe(db_events_path())
            self.pubsub.disconnect()
        self.getter.disconnect()


    @tornado.gen.engine
    def on_message(self, message):
        log.info('Message received: %s.', message)
        if message != 'update':
            return
        stale_keys = set()
        for tile_id in self.cache:
            log.debug('Putting data for tile: {}'.format(tile_id))
            raw = yield tornado.gen.Task(self.getter.get, tile_id)
            if not raw:
                log.warn('No data in key %s on Redis.', tile_id)
                stale_keys.add(tile_id)
                continue
            data = json.loads(raw)
            data['tipboard'] = self.tipboard_helpers
            self.write_message(data)
        if stale_keys:
            self.cache.difference_update(stale_keys)


    @tornado.gen.engine
    def on_publish(self, msg):
        if msg.kind == 'disconnect':
            log.warn('Redis disconnected, closing Web socket.')
            self.write_message(
                'The connection terminated  due to a Redis server error.'
            )
            self.close()
        elif msg.kind == 'message':
            tile_id = str(msg.body)
            log.info('Updating %s...', tile_id)
            raw = yield tornado.gen.Task(self.getter.get, tile_id)
            if not raw:
                log.warn('No data in key %s on Redis.', tile_id)
                return
            data = json.loads(raw)
            data['tipboard'] = self.tipboard_helpers
            self.cache.add(tile_id)
            self.write_message(data)
            log.info('Sent new data for %s through the Web socket.', tile_id)

    @tornado.gen.engine
    def listen(self):
        log.info('Web socket opened.')
        self.pubsub = self.setup_redis()
        yield tornado.gen.Task(
            self.pubsub.subscribe, db_events_path()
        )
        self.pubsub.listen(self.on_publish)
        log.info('Subscribed to %s on Redis.' % db_events_path())


class DashboardRendererHandler(tornado.web.RequestHandler, SentryMixin):
    def get(self, layout_name):
        def _verify_statics(static_file):
            user_tiles_path = os.path.join(
                os.path.expanduser('~'), '.tipboard/custom_tiles'
            )
            tipboard_tiles_path = os.path.join(settings.TIPBOARD_PATH, 'tiles')
            found = False
            for path in user_tiles_path, tipboard_tiles_path:
                if os.path.exists(os.path.join(path, static_file)):
                    found = True
                    break
            return found

        def _tile_path(tile_name):
            """
            Searches for tile's html file (in user's 'custom_tiles' folder,
            and then in app's 'tiles' folder) and returns full path of
            the tile, or raises exception if html file is not present in none
            of those locations.
            """
            user_tiles_path = os.path.join(
                os.path.expanduser('~'), '.tipboard/custom_tiles'
            )
            tipboard_tiles_path = os.path.join(settings.TIPBOARD_PATH, 'tiles')
            tile_html = '.'.join((tile_name, 'html'))
            for path in user_tiles_path, tipboard_tiles_path:
                tile_path = os.path.join(path, tile_html)
                if os.path.exists(tile_path):
                    return tile_path
            raise UserWarning('No such tile: %s' % tile_name)

        try:
            config = process_layout_config(layout_name or 'layout_config')
        except IOError as e:
            msg = '<br>'.join([
                '<div style="color: red">',
                'No config file found for dashboard: {}'.format(layout_name),
                'Make sure that file: "{}" exists.'.format(e.filename),
                '</div>',
            ])
            self.write(msg)
            return

        tiles_js = ['.'.join((name, 'js')) for name in config['tiles_names']]
        tiles_js = filter(_verify_statics, tiles_js)
        tiles_css = ['.'.join((name, 'css')) for name in config['tiles_names']]
        tiles_css = filter(_verify_statics, tiles_css)
        self.render(
            'layout.html',
            details=config['details'],
            layout=config['layout'],
            tipboard_css=settings.TIPBOARD_CSS_STYLES,
            tipboard_js=settings.TIPBOARD_JAVASCRIPTS,
            tiles_css=tiles_css,
            tiles_js=tiles_js,
            tile_path=_tile_path,
        )

    def head(self):
        # muted
        pass


class GetDashboardsPaths(tornado.web.RequestHandler):
    def post(self):
        paths = flipboard.get_paths()
        jsoned = json.dumps({'paths': paths})
        self.set_header("Content-Type", 'application/json')
        self.write(jsoned)


class FlipboardHandler(tornado.web.RequestHandler, SentryMixin):
    def get(self):
        self.render(
            'flipboard.html',
            page_title=flipboard.get_flipboard_title(),
            tipboard_css=settings.TIPBOARD_CSS_STYLES,
            tipboard_js=['js/lib/jquery.js', 'js/flipboard.js', 'js/lib/require.js'],
            flipboard_interval=settings.FLIPBOARD_INTERVAL,
        )


class MultiStaticFileHandler(tornado.web.StaticFileHandler, SentryMixin):
    def initialize(self, path):
        self.static_paths = []
        self.static_paths.extend(self.settings.get('tiles_paths'))
        self.static_paths.append(path)

    def get(self, path):
        # static paths are examined in following order:
        # custom_tiles --> tipboard/tiles --> tipboard/static
        for p in self.static_paths:
            try:
                super(MultiStaticFileHandler, self).initialize(p)
                return super(MultiStaticFileHandler, self).get(path)
            except tornado.web.HTTPError as exc:
                if exc.status_code == 404:
                    continue
                raise
        raise tornado.web.HTTPError(404)

    @classmethod
    def get_version(cls, settings, path):
    # temporarily muted
        return None


urls = [
    (r"/", FlipboardHandler),
    (r"/flipboard/getDashboardsPaths", GetDashboardsPaths),
    (r"/communication/websocket", DashboardSocketHandler),
    (r"/([a-zA-Z0-9_-]*)", DashboardRendererHandler),
    (r"/api/{}/{}/tileconfig/([a-zA-Z0-9_-]+)".format(
        api_version, settings.API_KEY), MetaProperty),
    (r"/api/{}/{}/tiledata/([a-zA-Z0-9_-]+)".format(
        api_version, settings.API_KEY), TileData),
    (r"/api/{}/{}/info".format(api_version, settings.API_KEY), ProjectInfo),
    (r"/api/{}/{}/push".format(api_version, settings.API_KEY), Push),
]

flipboard = Flipboard()
app = tornado.web.Application(
    urls,
    template_path=os.path.join(settings.TIPBOARD_PATH, 'templates'),
    static_path=os.path.join(settings.TIPBOARD_PATH, "static"),
    static_handler_class=MultiStaticFileHandler,
    debug=settings.DEBUG,
    tiles_paths=settings.TILES_PATHS,
    sentry_client=AsyncSentryClient(settings.SENTRY_DSN),
)
