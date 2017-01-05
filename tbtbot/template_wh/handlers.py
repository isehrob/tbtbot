"""Request handlers
"""
from tbtbot.lib.custom import TelegramRequestHandler
import configuration


class MainHandler(TelegramRequestHandler):
    def post(self):
        self.message = "Hey, I'm a new bot and waiting for instructions!"
        self.send()


class UnknownCommandHandler(TelegramRequestHandler):
	def post(self):
		self.send_help()


class NameHandler(TelegramRequestHandler):
    def post(self):
        self.message = "My name is this!"
        self.send()


class QuestionHandler(TelegramRequestHandler):
    def post(self):
        self.message = "I don't know!"
        self.send()


class GreetHandler(TelegramRequestHandler):
	def post(self):
		self.message = "Hi %s! What's up?" \
			% self.update['message']['chat']['username']
		self.send()


class BroadcastHandler(TelegramRequestHandler):
	def post(self):
		if self.chat_id in configuration.BOSSES:
			self.message = "Started broadcasting"
			self.send()
		else:
			self.send_help()