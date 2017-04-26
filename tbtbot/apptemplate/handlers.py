"""Request handlers
"""
from tbtbot.lib import RequestHandler
import configuration


class MainHandler(RequestHandler):
    def post(self):
        self.message = "Hey, I'm a new bot and waiting for instructions!"
        self.send()


class UnknownCommandHandler(RequestHandler):
	def post(self):
		self.send_help()