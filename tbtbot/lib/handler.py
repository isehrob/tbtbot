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