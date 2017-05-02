
webhook_env_template = """
# put here your bot token
BOT_TOKEN=<BOT_TOKEN>

# self-signed ssl cert files
CERTFILE=%s
KEYFILE=%s

# tornado server params
SERVER_PORT=8443
SERVER_HOST=0.0.0.0
"""

webhook_config_template = """
\"\"\"tbtbot configuration lives here
\"\"\"

from envparse import env


# reading env
env.read_envfile('.env')

# our bot token
BOT_TOKEN = env('BOT_TOKEN')

# use like this: API % method_name
API = "https://api.telegram.org/bot%s/%s" % (BOT_TOKEN, "%s")

CERTFILE = env('CERTFILE')
KEYFILE = env("KEYFILE")

SERVER_PORT = env('SERVER_PORT')
SERVER_HOST = env('SERVER_HOST')

APP_MODULE = 'app'

DB_MODULE = 'db'

ROUTE_MODULE = 'routes'

WEBHOOK_URL = None
"""

update_env_template = """
# put here your bot token
BOT_TOKEN=<BOT_TOKEN>

# tornado server params
SERVER_PORT=8585
SERVER_HOST=0.0.0.0
"""

update_config_template = """
\"\"\"tbtbot configuration lives here
\"\"\"

from envparse import env


# reading env
env.read_envfile('.env')

# our bot token
BOT_TOKEN = env('BOT_TOKEN')

# use like this: API % method_name
API = "https://api.telegram.org/bot%s/%s" % (BOT_TOKEN, "%s")

SERVER_PORT = env('SERVER_PORT')
SERVER_HOST = env('SERVER_HOST')

# in milliseconds
POLL_INTERVAL = 2000

APP_MODULE = 'app'

DB_MODULE = 'db'

ROUTE_MODULE = 'routes'

WEBHOOK_URL = None

"""