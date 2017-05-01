import json
import click


def get_command(updateObj):
	# updateObj is ether already decoded telegrams update object
	# or a request object resulting from calling telegram bot api's
	# `getUpdates` method
	if hasattr(updateObj, 'body'):
		text = json.loads(updateObj.body.decode())['message']['text']
	else:
		text = updateObj['message']['text']
	return text if text.startswith('/') else '/main'


def check_bot_config(configuration):
	"""Bot configuration check for misconfiguration"""
	# these attributes must be declared in the bot's config
	mustbeattrs = [
		'APP_MODULE',
		'BOT_TOKEN',
		'DB_MODULE',
		'ROUTE_MODULE',
		'WEBHOOK_URL',
		'SERVER_PORT',
		'SERVER_HOST'
	]

	notpresents = []

	for attrib in mustbeattrs:
		if not hasattr(configuration, attrib):
			notpresents.append(attrib)

	if notpresents:
		error_ms = ''
		if notpresents:
			error_ms += 'These attributes are not defined in configuration: \n%s' \
							% "\n".join(notpresents)
		exit(click.style(error_ms, fg='red'))
	return True