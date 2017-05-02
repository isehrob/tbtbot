import json
import tornado.web


from tbtbot.lib import utils


class _CustomRequestDispatcher(tornado.web._RequestDispatcher):

    def finish(self):
        # kind of a hack of tornado routing 
        # here if we get some update through our
        # webhook then we extract the command from
        # the telegram update and reroute the request
        if self.stream_request_body:
            self.request.body.set_result(None)
        else:
            self.request.body = b''.join(self.chunks)
            self.request._parse_body()

        if self.request.path == '/webhook':
            self.request.path = utils.get_command(self.request)
            self._find_handler()

        debug = self.application.settings.get('debug')
        if debug:
            telegram_message = json.loads(self.request.body.decode())
            user = telegram_message['message']['from']['username']
            user_id = telegram_message['message']['from']['id']
            text = telegram_message['message']['text']
            print('Got request for %s from %s (%s) with text "%s"' % (self.request.path, user, user_id, text))

        self.execute()


# implementing our above mentioned hack
class Application(tornado.web.Application):

    def start_request(self, server_conn, request_conn):
        return _CustomRequestDispatcher(self, request_conn)