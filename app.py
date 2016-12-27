import json

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient


# our bot token
# sehrob_bot
BOT_TOKEN = "<BOT_TOKEN>"
# use like this: API % method_name
API = "https://api.telegram.org/bot%s/%s" % (BOT_TOKEN, "%s")

# client = httpclient.HTTPClient()
client = tornado.httpclient.AsyncHTTPClient()


class TelegramRequestHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(TelegramRequestHandler, self).__init__(*args, **kwargs)
        self.message = None
        if self.request.body:
            self.message = json.loads(self.request.body.decode())


class WebHookHandler(TelegramRequestHandler):
    def post(self):
        print(self.message)
        self.write("kuku")

    def get(self):
        self.post()


class WebHookInfo(tornado.web.RequestHandler):
    def get(self):
        pass

class MainHandler(TelegramRequestHandler):
    def get(self):
        print('/main', self.message)
        self.write("Hello world")


class NameHandler(TelegramRequestHandler):
    def get(self):
        name = "Juju"
        print('/name', self.message)
        self.write("My name is %s" % name)


class QuestionHandler(TelegramRequestHandler):
    def get(self):
        answer = "I don't know"
        print('/ask', self.message)
        self.write(answer)


def make_app():
    return tornado.web.Application([
        (r"/webhook", WebHookHandler),
        (r"/name", NameHandler),
        (r"/ask", QuestionHandler),
        (r"/.*", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    # app.listen(8787, '0.0.0.0')
    http_server = tornado.httpserver.HTTPServer(app, ssl_options={
        "certfile": "/home/s_ibrohimov/projects/tornado/ssl/tbotprkey.pem",
        "keyfile": "/home/s_ibrohimov/projects/tornado/ssl/tbotprkey.key"
    })
    http_server.listen(8443, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()
