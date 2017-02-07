import json


def get_command(updateObj):
	# updateObj is ether already decoded telegrams update object
	# or a request object resulting from calling telegram bot api's
	# `getUpdates` method
	if hasattr(updateObj, 'body'):
		text = json.loads(updateObj.body.decode())['message']['text']
	else:
		text = updateObj['message']['text']
	return text if text.startswith('/') else '/main'