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
from tipboard.api import Push2
from tipboard.redis_utils import db_events_path

log = logging.getLogger(__name__)


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

    def check_origin(self, origin):
        # TODO:: rm it, it's tmp
        return True

    # Only cache keys. Values will be retrieved from Redis
    # every time. This ensures users don't get stale data.
    cache = set()

    def __init__(self, *args, **kwargs):
        super(DashboardSocketHandler, self).__init__(*args, **kwargs)
        self.listen()
        self.getter = self.setup_redis()

    @tornado.gen.engine
    def listen(self):
        log.info('Web socket opened.')
        self.pubsub = self.setup_redis()
        yield tornado.gen.Task(
            self.pubsub.subscribe, db_events_path()
        )
        self.pubsub.listen(self.on_publish)
        log.info('Subscribed to %s on Redis.' % db_events_path())

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
            self.cache.add(tile_id)
            self.write_message(data)
            log.info('Sent new data for %s through the Web socket.', tile_id)

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
            self.write_message(data)
        if stale_keys:
            self.cache.difference_update(stale_keys)

    def on_close(self):
        log.info('Web socket closed.')
        if self.pubsub.subscribed:
            self.pubsub.unsubscribe(db_events_path())
            self.pubsub.disconnect()
        self.getter.disconnect()


class MainHandler(tornado.web.RequestHandler, SentryMixin):
    def get(self):
        self.render(
            'dashboard.html',
            # page_title=flipboard.get_flipboard_title(),
            # tipboard_css=settings.TIPBOARD_CSS_STYLES,
            # tipboard_js=['js/lib/jquery.js', 'js/flipboard.js'],
            # flipboard_interval=settings.FLIPBOARD_INTERVAL,
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
    (r"/", MainHandler),
    (r"/communication/websocket", DashboardSocketHandler),
    (r"/api/{}/{}/push".format(2, settings.API_KEY), Push2),
]

app = tornado.web.Application(
    urls,
    template_path=os.path.join(settings.TIPBOARD_PATH, 'templates'),
    static_path=os.path.join(settings.TIPBOARD_PATH, "static"),
    # static_handler_class=MultiStaticFileHandler,
    debug=settings.DEBUG,
    sentry_client=AsyncSentryClient(settings.SENTRY_DSN),
)
