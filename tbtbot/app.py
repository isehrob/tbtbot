import json

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.gen

from envparse import env


# reading env
env.read_envfile('.env')

# our bot token
# sehrob_bot
BOT_TOKEN = env('BOT_TOKEN')
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

    @tornado.gen.coroutine
    def post(self):
        if self.message:
            text = self.message['message']['text']
            command = text if text.startswith('/') else '/main'
            print('yes message', command)
            self.redirect(command)
        else:
            print('no message')
            self.redirect("/main")
        # request = tornado.httpclient.HTTPRequest(
        #     url=('https://91.212.89.6:8443%s' % command),
        #     allow_nonstandard_methods=True,
        #     body=json.dumps(self.message)
        # )
        # response = yield client.fetch(request)
        # yield client.fetch(API % 'sendMessage?chat_id=%s&text=%s'
        #     % (self.message['message']['from']['id'], response.body.decode()))
    
    def get(self):
        self.post()


class WebHookInfo(tornado.web.RequestHandler):
    def get(self):
        pass

class MainHandler(TelegramRequestHandler):
    def get(self):
        print('/main', self.message)
        self.redirect("/name")


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
    app = tornado.web.Application([
        (r"/webhook", WebHookHandler),
        (r"/name", NameHandler),
        (r"/ask", QuestionHandler),
        (r"/.*", MainHandler),
    ])

    #app.add_handlers(r"https://91.212.89.6",[
     #   (r"/name", NameHandler),
      #  (r"/ask", QuestionHandler),
       # (r"/.*", MainHandler),
    #])

    return app


def kuku():
    with open('check.txt', 'a') as f:
        f.write('working-ku\n')

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(make_app(), ssl_options={
        "certfile": env('CERTFILE'),
        "keyfile": env("KEYFILE")
    })
    http_server.listen(env('SERVER_PORT'), env('SERVER_HOST'))
    pcb = tornado.ioloop.PeriodicCallback(kuku, 2000)
    pcb.start()
    tornado.ioloop.IOLoop.current().start()
