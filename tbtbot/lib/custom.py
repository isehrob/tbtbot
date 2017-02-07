"""Custom classes
"""

import json

import tornado.web
import tornado.httpclient



# Custom `RequestHandler` class which encapsulates the 
# common functionality for telegram requests
class RequestHandler(tornado.web.RequestHandler):

    def initialize(self, api):
        self.message = None
        self.update = None
        self.chat_id = None
        self.client = tornado.httpclient.HTTPClient()
        self.api = api

        if self.request.body:
            self.update = json.loads(self.request.body.decode())
            self.chat_id = self.update['message']['from']['id']

    def prepare(self):
    	self.client.fetch(self.api % 'sendChatAction?chat_id=%s&action=%s'
            % (self.chat_id, "typing"))

    def send(self):
        self.client.fetch(self.api % 'sendMessage?chat_id=%s&text=%s&reply_markup=%s'
            % (self.chat_id, self.message, json.dumps({'remove_keyboard': True})))

    def send_help(self):
        self.message = "What?"
        self.send()
    	


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
            text = json.loads(
                self.request.body.decode()
            )['message']['text']
            command = text if text.startswith('/') else '/main'
            self.request.path = command
            self._find_handler()

        self.execute()


# implementing our above mentioned hack
class Application(tornado.web.Application):

	def start_request(self, server_conn, request_conn):
		print(dir(request_conn))
		return _CustomRequestDispatcher(self, request_conn)
