import json
import pickle

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.gen
import tornado.httputil

from envparse import env


# reading env
env.read_envfile('.env')

# our bot token
# sehrob_bot
BOT_TOKEN = env('BOT_TOKEN')
# use like this: API % method_name
API = "https://api.telegram.org/bot%s/%s" % (BOT_TOKEN, "%s")


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
class CustomApplication(tornado.web.Application):

    def start_request(self, server_conn, request_conn):
        return _CustomRequestDispatcher(self, request_conn)


# Custom `RequestHandler` class which encapsulates the 
# common functionality for telegram requests
class TelegramRequestHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(TelegramRequestHandler, self).__init__(*args, **kwargs)
        self.message = None
        self.update = None
        # client = httpclient.HTTPClient()
        self.client = tornado.httpclient.HTTPClient()

        if self.request.body:
            self.update = json.loads(self.request.body.decode())

    def send(self):
        self.client.fetch(API % 'sendMessage?chat_id=%s&text=%s'
            % (self.update['message']['from']['id'], self.message))


class MainHandler(TelegramRequestHandler):
    def post(self):
        self.message = "Hello!"
        self.send()


class NameHandler(TelegramRequestHandler):
    def post(self):
        self.message = "My name is this!"
        self.send()  


class QuestionHandler(TelegramRequestHandler):
    def post(self):
        self.message = "I don't know!"
        self.send()


def make_app():
    app = CustomApplication([
        (r"/webhook", tornado.web.RequestHandler),
        (r"/name", NameHandler),
        (r"/ask", QuestionHandler),
        (r"/.*", MainHandler),
    ])

    return app



if __name__ == "__main__":

    http_server = tornado.httpserver.HTTPServer(make_app(), ssl_options={
        "certfile": env('CERTFILE'),
        "keyfile": env("KEYFILE")
    })

    http_server.listen(env('SERVER_PORT'), env('SERVER_HOST'))
    tornado.ioloop.IOLoop.current().start()
