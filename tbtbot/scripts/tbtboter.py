# console program for creating, registering
# and etc. telegram bots which will help to
# automate some routines while creating and 
# developing telegram bots

import os
import sys
import subprocess
import argparse
import re

import requests
import tornado.httpclient

import tbtbot
from tbtbot.scripts import templatestrings



def get_parser():
	"""command line argument parser"""
	pparser = argparse.ArgumentParser(
		description='A console program which helps to create telegram bots'
	)
	pparser.add_argument('-s', '--serve', help='start the bot', action="store_true")
	pparser.add_argument('-c', '--create', help="create a tornado based telegram bot",
						type=str, nargs='?', const='')
	pparser.add_argument('-cs', '--create_certificate', help='create self-signed certificate',
						action="store_true")
	pparser.add_argument('-lc', '--list_commands', help='List available bot commands',
						action="store_true")
	pparser.add_argument('-sdb', '--syncdb', help='Syncronizes database with models module',
						action="store_true")
	pparser.add_argument('-sw', '--set_webhook', help='set webhook to get updates', 
						action="store_true")
	pparser.add_argument('-gw', '--get_webhookInfo', help='gets webhookInfo', 
						action="store_true")
	pparser.add_argument('-dw', '--delete_webhook', help='deletes webhook so you\
						can switch to getUpdates', action="store_true")
	return pparser


# these will ease the life of
# the telegram bot developers
def set_webhook():
	# sets webHook to listen for new updates
	import sys
	sys.path.insert(0, os.getcwd())

	try:
		import configuration
	except ImportError:
		error_ms = '%s\n%s' % ('Couln\'t import configuration!',
			'Please, go the directory where your bot code lives and then try')
		raise Exception(error_ms)
	else:
		print('setting webhook for', configuration.API)

		files = {
			'certificate': ('certificate', open(configuration.CERTFILE, 'rb')),
		}

		data = {
			'url': configuration.WEBHOOK_URL,
		}

		url = configuration.API % 'setWebhook'
		rp = requests.post(url, files=files, data=data)
		print('result of setWebhook: ', rp.status_code, rp.text, rp.reason)
	finally:
		sys.path.pop(0)

def get_webhookInfo():
	# gets the webhook info 
	import sys
	sys.path.insert(0, os.getcwd())

	try:
		import configuration
	except ImportError:
		error_ms = '%s\n%s' % ('Couln\'t import configuration!',
			'Please, go the directory where your bot code lives and then try')
		raise Exception(error_ms)
	else:
		print('getting webhookinfo for', configuration.API)
		rp = tornado.httpclient.HTTPClient().fetch(configuration.API % 'getWebhookInfo')
		print(rp.body)
	finally:
		sys.path.pop(0)

def delete_webhook():
	# deletes the webHook
	import sys
	sys.path.insert(0, os.getcwd())

	try:
		import configuration
	except ImportError:
		error_ms = '%s\n%s' % ('Couln\'t import configuration!',
			'Please, go the directory where your bot code lives and then try')
		raise Exception(error_ms)
	else:
		print('Deleting webhook', configuration.API)
		rp = tornado.httpclient.HTTPClient().fetch(configuration.API % 'deleteWebhook')
		print('result of deleteWebhook: ', rp.body)
	finally:
		sys.path.pop(0)


def create_certificate(bot_name):
	# creates self signed ssl certificate
	cwd = os.getcwd()
	cert_path = input('Please specify the path for the certificate [default: current dir]: ', )

	try:
		os.chdir(cert_path)
	except FileNotFoundError:
		print('Using default value for the path')
		cert_path = cwd
		pass

	rtncode = subprocess.call([
		"openssl",
		"req", "-newkey", "rsa:2048", "-sha256", "-nodes",
		"-keyout", "%s_private.key" % bot_name,
		"-x509", "-days", "365", "-out", "%s_public.pem" % bot_name
	])
	if not rtncode:
		print("Self-signed certificate is created in '%s'" % os.path.abspath(cert_path))
		return cert_path
	os.chdir(cwd)
	return False


def sync_db():
	# deletes the webHook
	import sys
	sys.path.insert(0, os.getcwd())

	try:
		import configuration
	except ImportError:
		error_ms = '%s\n%s' % ('Couln\'t import configuration!',
			'Please, go the directory where your bot code lives and then try')
		raise Exception(error_ms)
	else:
		import importlib
		try:
			db = importlib.import_module(configuration.DB_MODULE)
		except ImportError:
			error_ms = '%s\n%s' % ('Couln\'t import db module!',
			'Maybe you\'ve deleted db.py or moved to somewhere else?')
			raise Exception(error_ms)
		else:
			db.create_all()
	finally:
		sys.path.pop(0)


def get_command_list():
	# todo: make more elegant
	def remove_slash(cmd):
		return cmd[1:]

	import sys
	sys.path.insert(0, os.getcwd())
	try:
		from routes import get_routes
	except ImportError:
		error_ms = '%s\n%s' % ('Couln\'t import routes!',
			'Please, go the directory where your bot code lives and then try')
		raise Exception(error_ms)
	else:
		print('Available commands for your bot')
		for entry in get_routes():
			try:
				cmd, __, __, desc = entry
			except ValueError:
				cmd = entry[0]
				desc = ''
			cmd = remove_slash(cmd)
			print('%s - %s' % (cmd, desc))
	finally:
		sys.path.pop(0)



def create_with_webhook(bot_name, cert_path = False):
	# creates the telegram bot skeleton suited
	# to get updates by webHook
	cwd = os.getcwd()
	print('creating with webhook')
	os.mkdir(bot_name)
	os.chdir(os.path.abspath(bot_name))
	temp_dir = os.path.join(os.path.dirname(tbtbot.__file__), 'template')

	if cert_path:
		cert_path = os.path.abspath(cert_path)

	for entry in os.listdir(temp_dir):
		if os.path.isfile(os.path.join(temp_dir, entry)):
			with open(os.path.join(temp_dir, entry)) as f:
				with open(entry, 'w') as w:
					if entry == '.env.example' and cert_path:
						w.write(templatestrings.envtemplate % (
							os.path.join(cert_path, bot_name + '_private.key'),
							os.path.join(cert_path, bot_name + '_public.key')
							))
					elif entry == 'configuration.py':
						w.write(templatestrings.configtemplate)
					else:
						w.write(f.read())
	os.chdir(cwd)
	return


def create_with_getUpdates(bot_name):
	# creates the telegram bot skeleton without
	# webhook functionality for some reasons
	# for example when the host hasn't static ip
	cwd = os.getcwd()
	print('creating with getUpdates')
	os.mkdir(bot_name)
	os.chdir(os.path.abspath(bot_name))
	temp_dir = os.path.join(os.path.dirname(tbtbot.__file__), 'template2')

	for entry in os.listdir(temp_dir):
		if os.path.isfile(os.path.join(temp_dir, entry)):
			with open(os.path.join(temp_dir, entry)) as f:
				with open(entry, 'w') as w:
					if entry == '.env.example':
						w.write(templatestrings.env2template)
					elif entry == 'configuration.py':
						w.write(templatestrings.config2template)
					else:
						w.write(f.read())
	os.chdir(cwd)
	return


def create_bot(bot_name):

	if not bot_name:
		bot_name = input('Please, specify a name for your bot: ', )
		if not bot_name:
			exit("Can't create a bot without a name")
	updates_type = input('Ok, how do you want to get your updates?\n\
						Through 1 webhooks / 2 long polling [1/2]: ', )

	if int(updates_type) not in [1,2]:
		exit('Unkown option, please retry')

	if int(updates_type) is 1:
		create_ssl = input('Want to create self-signed certificate? [Yes/No]: ', )
		if create_ssl not in ['Yes', 'No']:
			exit('Unkown option, please retry')
		if create_ssl == 'Yes':
			cert_path = create_certificate(bot_name)
			if cert_path is False:
				exit('Couldn\'t create certificate')
			create_with_webhook(bot_name, cert_path)
		if create_ssl == 'No':
			create_with_webhook(bot_name)

	if int(updates_type) is 2:
		create_with_getUpdates(bot_name)

	print('DONE!')
	return


def serve():
	# deletes the webHook
	import sys
	sys.path.insert(0, os.getcwd())

	try:
		import configuration
	except ImportError:
		error_ms = '%s\n%s' % ('Couln\'t import configuration!',
			'Please, go the directory where your bot code lives and then try')
		raise Exception(error_ms)
	else:
		# if everything is ok then we are in the bot directory
		# so we can import the `app` without any problem
		import app
		print('Bot started!')
		try:
			app.start_bot()
		except KeyboardInterrupt:
			print('stopping the bot...')
			app.stop_bot()
			print("BYE!")

	finally:
		sys.path.pop(0)


def main():
	# main entry point of the console program
	CMD_PARSER = get_parser()
	CMD_ARGS = CMD_PARSER.parse_args()

	if CMD_ARGS.serve:
		print('Starting the bot...')
		serve()

	if CMD_ARGS.create or CMD_ARGS.create == '':
		print('Creating bot')
		create_bot(CMD_ARGS.create)

	if CMD_ARGS.create_certificate:
		print('Creating self-signed certificate')
		create_certificate('my_bot')

	if CMD_ARGS.list_commands:
		get_command_list()

	if CMD_ARGS.syncdb:
		sync_db()

	if CMD_ARGS.set_webhook:
		print('Setting webhook')
		set_webhook()

	if CMD_ARGS.get_webhookInfo:
		print('Getting webhookInfo')
		get_webhookInfo()

	if CMD_ARGS.delete_webhook:
		print('Deleting webhook')
		delete_webhook()

	# a kind of a hack to display help message
	# when there is no command line arguments
	# TODO: Find out how to do it with `argparse`
	if not any(CMD_ARGS.__dict__.values()):
		CMD_PARSER.print_help()

	return False
