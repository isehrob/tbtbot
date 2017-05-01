import os
import shutil

import click
import tbtbot
from tbtbot.tbtboter.cli import pass_context
from tbtbot.tbtboter.commands import cmd_create_ssl_cert
from tbtbot.apptemplate import template_strings as tstrings


# these constants should be self-explanatory
COMMON_TEMPLATE_FILES = [
	'models.py',
	'db.py',
	'routes.py',
	'handlers.py'
]
WEBHOOK_APP_TEMPLATE_FILE = 'app.py'
UPDATE_APP_TEMPLATE_FILE = 'app_with_updates.py'
TEMPLATE_DIR = os.path.join(os.path.dirname(tbtbot.__file__), 'apptemplate')


# helper functions
def copy_common_templates(tmpfiles):
	"""copies common template files into current directory"""
	for filename in tmpfiles:
		src_file = os.path.join(TEMPLATE_DIR, filename)
		tgt_file = os.path.join(os.getcwd(), filename)
		shutil.copy(src_file, tgt_file)


def copy_app_template(apptemplatefile):
	"""copies app template file into current directory"""
	src_app_file = os.path.join(TEMPLATE_DIR, apptemplatefile)
	tgt_app_file = os.path.join(os.getcwd(), 'app.py')
	shutil.copy(src_app_file, tgt_app_file)


def make_env_file(env_string):
	"""creates .env.example file in current directory"""
	with open('.env.example', 'w') as f:
		f.write(env_string)


def set_env():
	shutil.copy('.env.example', '.env')


def make_config_file(config_string):
	"""creates bot configuration file from provided string
		in current directory"""
	with open('configuration.py', 'w') as f:
		f.write(config_string)


def create_with_webhook(bot_name, certificate_path):
	# creates the telegram bot skeleton suited
	# to get updates by webHook
	cert_path = os.path.abspath(certificate_path)

	copy_common_templates(COMMON_TEMPLATE_FILES)
	# copying app file
	copy_app_template(WEBHOOK_APP_TEMPLATE_FILE)
	# creating configuration and .env.example files
	make_config_file(tstrings.webhook_config_template)
	env_template_string = tstrings.webhook_env_template % (
								'<your_bots_private.key>',
								'<your_bots_public.key>'
								)
	if certificate_path:
		env_template_string = tstrings.webhook_env_template % (
								os.path.join(cert_path, bot_name + '_private.key'),
								os.path.join(cert_path, bot_name + '_public.key')
								)
	make_env_file(env_template_string)


def create_with_getUpdates():
	# creates the telegram bot skeleton without
	# webhook functionality for some reasons
	# for example when the host hasn't static ip
	copy_common_templates(COMMON_TEMPLATE_FILES)
	# copying app file
	copy_app_template(UPDATE_APP_TEMPLATE_FILE)
	# creating configuration and .env.example files
	make_config_file(tstrings.update_config_template)
	make_env_file(tstrings.update_env_template)


@click.command('create_bot', short_help='Create grand new bot in cwd')
@click.option('--bot_name', prompt="Please, specify a name for your bot")
@click.option(
	'--update_type', 
	prompt="Ok, how do you want to get your updates?\nwebhooks[1]/long polling[2]",
	type=click.Choice(['1', '2']))
@pass_context
def cli(context, bot_name, update_type):
	"""Creates grand new bot in cwd"""
	os.mkdir(bot_name)
	os.chdir(os.path.abspath(bot_name))

	if update_type == '1':
		click.echo('creating with webhook')
		cert_path = False
		if click.confirm('Want to create self-signed certificate?'):
			# TODO: is this right?
			cert_path = cmd_create_ssl_cert.create_certificate(bot_name)
			if cert_path is False:
				click.echo(click.style('Couldn\'t create certificate.\
					Creating bot without ssl cert', fg='yellow'))
		create_with_webhook(bot_name, cert_path)

	if update_type == '2':
		click.echo('creating with getUpdates')
		create_with_getUpdates()

	click.echo(click.style('DONE!', fg='green'))