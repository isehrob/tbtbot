import json
import pickle

import tornado
import tornado.httpclient

import configuration



def getMe():
    client = tornado.httpclient.HTTPClient()
    result = client.fetch(configuration.API % 'getMe')
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
    result = client.fetch(configuration.API % 'getUpdates?timeout=%d&offset=%d'
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
            url=('http://127.0.0.1:%s%s' % (configuration.SERVER_PORT, command)),
            allow_nonstandard_methods=True,
            body=json.dumps(update),
            request_timeout=1
        )
        response = client.fetch(request, raise_error=False)
    return True