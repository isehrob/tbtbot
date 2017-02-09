import json



class TelegramBotApiBaseType():

	def __init__(self, json_object=None):

		if json_object:
			type_object = json.loads(json_object)
			for key in type_object.keys():
				self.__dict__.update(dict(key=type_object[key]))

	def __str__(self):
		type_object = self.__dict__
		return json.dumps(type_object)


class TelegramBotApiMethods():

	def make_request(self, method, params):
		# https://core.telegram.org/bots/api#making-requests
		pass

	def getUpdates(self):
		# https://core.telegram.org/bots/api#getupdates
		pass

	def setWebhook(self):
		# https://core.telegram.org/bots/api#setwebhook
		pass

	def deleteWebhook(self):
		# https://core.telegram.org/bots/api#deletewebhook
		pass

	def getWebhookInfo(self):
		# https://core.telegram.org/bots/api#getwebhookinfo
		pass

	def getMe(self):
		# https://core.telegram.org/bots/api#getme
		pass

	def sendMessage(self):
		# https://core.telegram.org/bots/api#sendmessage
		pass

	def forwardMessage(self):
		# https://core.telegram.org/bots/api#forwardmessage
		pass

	def sendPhoto(self):
		# https://core.telegram.org/bots/api#sendphoto
		pass

	def sendAudio(self):
		# https://core.telegram.org/bots/api#sendaudio
		pass

	def sendDocument(self):
		# https://core.telegram.org/bots/api#senddocument
		pass

	def sendSticker(self):
		# https://core.telegram.org/bots/api#sendsticker
		pass

	def sendVideo(self):
		# https://core.telegram.org/bots/api#sendvideo
		pass

	def sendVoice(self):
		# https://core.telegram.org/bots/api#sendvoice
		pass

	def sendLocation(self):
		# https://core.telegram.org/bots/api#sendlocation
		pass

	def sendVenue(self):
		# https://core.telegram.org/bots/api#sendvenue
		pass

	def sendContact(self):
		# https://core.telegram.org/bots/api#sendcontact
		pass

	def sendChatAction(self):
		# https://core.telegram.org/bots/api#sendchataction
		pass

	def getUserProfilePhotos(self):
		# https://core.telegram.org/bots/api#getuserprofilephotos
		pass

	def getFile(self):
		# https://core.telegram.org/bots/api#getfile
		pass

	def kickChatMember(self):
		# https://core.telegram.org/bots/api#kickchatmember
		pass

	def leaveChat(self):
		# https://core.telegram.org/bots/api#leavechat
		pass

	def unbanChatMember(self):
		# https://core.telegram.org/bots/api#unbanchatmember
		pass

	def getChat(self):
		# https://core.telegram.org/bots/api#getchat
		pass

	def getChatAdministrators(self):
		# https://core.telegram.org/bots/api#getchatadministrators
		pass

	def getChatMembersCount(self):
		# https://core.telegram.org/bots/api#getchatmemberscount
		pass

	def getChatMember(self):
		# https://core.telegram.org/bots/api#getchatmember
		pass

	def answerCallbackQuery(self):
		# https://core.telegram.org/bots/api#answercallbackquery
		pass

	def editMessageText(self):
		# https://core.telegram.org/bots/api#editmessagetext
		pass

	def editMessageCaption(self):
		# https://core.telegram.org/bots/api#editmessagecaption
		pass

	def editMessageReplyMarkup(self):
		# https://core.telegram.org/bots/api#editmessagereplymarkup
		pass

	# TODO (sehrob): inline mode will be implemented later
	# def answerInlineQuery(self):
	# 	# https://core.telegram.org/bots/api#editmessagereplymarkup
	# 	pass


class User(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#user
	pass


class Chat(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#chat
	pass


class Message(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#message
	pass


class MessageEntity(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#messageentity
	pass


class PhotoSize(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#photosize
	pass


class Audio(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#audio
	pass


class Document(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#document
	pass


class Sticker(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#sticker
	pass


class Video(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#video
	pass


class Voice(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#voice
	pass


class Contact(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#contact
	pass


class Location(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#location
	pass


class Venue(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#venue
	pass


class UserProfilePhotos(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#userprofilephotos
	pass


class File(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#file
	pass


class ReplyKeyboardMarkup(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#replykeyboardmarkup
	pass


class KeyboardButton(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#keyboardbutton
	pass


class ReplyKeyboardRemove(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#replykeyboardremove
	pass


# TODO (sehrob): Inline mode will be implemented later
# class InlineKeyboardMarkup(TelegramBotApiBaseType):
# 	# https://core.telegram.org/bots/api#inlinekeyboardmarkup
# 	pass


# class InlineKeyboardButton(TelegramBotApiBaseType):
# 	# https://core.telegram.org/bots/api#inlinekeyboardbutton
# 	pass


class CallbackQuery(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#callbackquery
	pass


class ForceReply(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#forcereply
	pass


class ChatMember(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#chatmember
	pass


class ResponseParameters(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#responseparameters
	pass


class InputFile(TelegramBotApiBaseType):
	# https://core.telegram.org/bots/api#inputfile
	pass



