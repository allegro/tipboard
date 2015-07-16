import logging
import json

import tornado.escape
import tornado.ioloop
import tornado.web

from tipboard import redis_utils

logger = logging.getLogger(__name__)

api_version = 'v0.1'


class Push2(tornado.web.RequestHandler):
    """
    Handles pushing tile's data.
    """
    def post(self):
        request_data = json.loads(self.request.body.decode('utf8'))
        errors = []
        if 'tile-id' not in request_data:
            errors.append('send data has no "tile-id"')
        if 'tile-data' not in request_data:
            errors.append('send data has no "tile-data"')
        if errors:
            self.set_status(400)
            for error in errors:
                self.write(error + '\n')
        else:
            redis_utils.redis_save(request_data['tile-id'], request_data)
            self.set_status(200)
