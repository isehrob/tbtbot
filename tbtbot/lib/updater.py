import json
import pickle

import tornado
import tornado.httpclient

from tbtbot.lib import utils



class Updater():
    """Class instances get updates from telegram bot api"""

    def __init__(self, api, bot_adress, db=None):
        self.api = api
        self.db = db
        self.client = tornado.httpclient.HTTPClient()
        self.bot_adress = bot_adress

    def getMe(self):
        result = self.client.fetch(self.api % 'getMe')
        print(result.body)
        return

    def getLastOffset(self):
        try:
            with open('offset.txt', 'r') as f:
                return int(f.readline())
        except FileNotFoundError:
            print('zero offset')
            return 0

    def putLastOffset(self, updates):
        updid = updates[-1]['update_id'] + 1
        with open('offset.txt', 'w') as f:
            return f.write(str(updid))

    def dispatchAll(self, updates):
        for update in updates:
            command = utils.get_command(update)
            request = tornado.httpclient.HTTPRequest(
                url=('%s%s' % (self.bot_adress, command)),
                allow_nonstandard_methods=True,
                body=json.dumps(update),
                request_timeout=1
            )
            self.client.fetch(request, raise_error=False)
        return True

    def getUpdates(self, timeout):
        updid = self.getLastOffset()
        result = self.client.fetch(self.api % 'getUpdates?timeout=%d&offset=%d'
                              % (timeout, updid))
        updates = json.loads(result.body.decode())['result']

        if not len(updates):
            return False
        else:
            self.putLastOffset(updates)

        return self.dispatchAll(updates)