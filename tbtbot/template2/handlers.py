"""Request handlers
"""
from tbtbot.lib.custom import TelegramRequestHandler
import configuration


class MainHandler(TelegramRequestHandler):
    def get(self):
        self.message = "Hey, I'm a new bot and waiting for instructions!"
        self.send()


class UnknownCommandHandler(TelegramRequestHandler):
	def get(self):
		self.send_help()