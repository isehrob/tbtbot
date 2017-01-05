"""tbtbot configuration lives here
"""

from envparse import env


# reading env
env.read_envfile('.env')

# our bot token
# sehrob_bot
BOT_TOKEN = env('BOT_TOKEN')

# use like this: API % method_name
API = "https://api.telegram.org/bot%s/%s" % (BOT_TOKEN, "%s")

CERTFILE = env('CERTFILE')
KEYFILE = env("KEYFILE")

SERVER_PORT = env('SERVER_PORT')
SERVER_HOST = env('SERVER_HOST')

BOSSES = [139912293,]