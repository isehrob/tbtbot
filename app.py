import json

import tornado.ioloop
import tornado.web


class TelegramRequestHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(TelegramRequestHandler, self).__init__(*args, **kwargs)
        self.message = json.loads(self.request.body.decode())

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
        (r"/name", NameHandler),
        (r"/ask", QuestionHandler),
        (r"/.*", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8787, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()
