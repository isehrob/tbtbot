import requests
import time
import json

from datetime import datetime
import tornado

from tornado import ioloop, gen, httpclient

import bot_db

# our bot token
# sehrob_bot
BOT_TOKEN = "224642244:AAHBHgcyUXyJyjYOaUbORf64k4kKAqcXv2U"
# use like this: API % method_name
API = "https://api.telegram.org/bot%s/%s" % (BOT_TOKEN, "%s")

# client = httpclient.HTTPClient()
client = httpclient.AsyncHTTPClient()

@gen.coroutine
def getMe():
    result = yield client.fetch(API % 'getMe')
    print(result.body)
    return

def getLastOffset():
    upd = bot_db.Updates()
    return upd.select_one()

def putLastOffset(updid, offset):
    upd = bot_db.Updates()
    dt = datetime.now().toordinal()
    return upd.update(updid, "offset=%d, date=%d" % (offset, dt))

@gen.coroutine
def getUpdates(timeout):
    updid, lastUpdOffset, _ = getLastOffset()
    result = yield client.fetch(API % 'getUpdates?timeout=%d&offset=%d'
                          % (timeout, lastUpdOffset))
    updates = json.loads(result.body.decode())['result']

    if not len(updates):
        return False

    for update in updates:
        # print(update)
        text = update['message']['text']
        command = text if text.startswith('/') else '/main'
        request = tornado.httpclient.HTTPRequest(
            url=('http://127.0.0.1:8787%s' % command),
            allow_nonstandard_methods=True,
            body=json.dumps(update)
        )
        response = yield client.fetch(request)
        yield client.fetch(API % 'sendMessage?chat_id=%s&text=%s'
                     % (update['message']['from']['id'], response.body.decode()))
        time.sleep(1)
    lastOffset = updates[-1]['update_id'] + 1
    putLastOffset(updid, lastOffset)
    return True

@gen.coroutine
def main():
    yield getMe()
    while True:
        yield getUpdates(5)
        time.sleep(1)


if __name__ == "__main__":
    print("Here's me!")
    ioloop.IOLoop.current().run_sync(main)

