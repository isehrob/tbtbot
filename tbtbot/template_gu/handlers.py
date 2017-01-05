"""Request handlers
"""
import lib.custom
import configuration


class MainHandler(lib.custom.TelegramRequestHandler):
    def post(self):
        self.message = "Hey, I'm a new bot and waiting for instructions!"
        self.send()


class UnknownCommandHandler(lib.custom.TelegramRequestHandler):
	def post(self):
		self.send_help()


class NameHandler(lib.custom.TelegramRequestHandler):
    def post(self):
        self.message = "My name is this!"
        self.send()


class QuestionHandler(lib.custom.TelegramRequestHandler):
    def post(self):
        self.message = "I don't know!"
        self.send()


class GreetHandler(lib.custom.TelegramRequestHandler):
	def post(self):
		self.message = "Hi %s! What's up?" \
			% self.update['message']['chat']['username']
		self.send()


class BroadcastHandler(lib.custom.TelegramRequestHandler):
	def post(self):
		if self.chat_id in configuration.BOSSES:
			self.message = "Started broadcasting"
			self.send()
		else:
			self.send_help()