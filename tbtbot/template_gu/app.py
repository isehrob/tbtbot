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
env.read_envfile('.env2')

# our bot token
# sehrob_bot
BOT_TOKEN = env('BOT_TOKEN')
# use like this: API % method_name
API = "https://api.telegram.org/bot%s/%s" % (BOT_TOKEN, "%s")



def getMe():
    # client = httpclient.HTTPClient()
    client = tornado.httpclient.HTTPClient()
    result = client.fetch(API % 'getMe')
    print(result.body)
    return

def getLastOffset():
    try:
        with open('offset.txt', 'r') as f:
            return int(f.readline())
    except FileNotFoundError:
        print('zero offset')
        return 0

def putLastOffset(updid):
    with open('offset.txt', 'w') as f:
        return f.write(str(updid))


def getUpdates(timeout):
    client = tornado.httpclient.HTTPClient()

    updid = getLastOffset()
    result = client.fetch(API % 'getUpdates?timeout=%d&offset=%d'
                          % (timeout, updid))
    updates = json.loads(result.body.decode())['result']

    if not len(updates):
        return False
    else:
        lastOffset = updates[-1]['update_id'] + 1
        putLastOffset(lastOffset)

    for update in updates:
        print(update)
        text = update['message']['text']
        command = text if text.startswith('/') else '/main'
        request = tornado.httpclient.HTTPRequest(
            url=('http://127.0.0.1:%s%s' % (env('SERVER_PORT'), command)),
            allow_nonstandard_methods=True,
            body=json.dumps(update)
        )
        response = client.fetch(request)
    return True


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
    def get(self):
        self.message = "Hello!"
        self.send()


def make_app():
    app = tornado.web.Application([
        (r"/.*", MainHandler),
    ])

    return app


def updater():
    # some kind of parallel task
    getUpdates(10)


if __name__ == "__main__":

    pcb = tornado.ioloop.PeriodicCallback(updater, 3000)
    pcb.start()

    http_server = tornado.httpserver.HTTPServer(make_app())
    http_server.listen(env('SERVER_PORT'), env('SERVER_HOST'))
    tornado.ioloop.IOLoop.current().start()
