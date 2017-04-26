import os
import click

import tbtbot
from tbtbot.tbtboter.cli import pass_context


# @main.command()
# @click.option('--bot_name', prompt=True)
# @click.option('--certificate_path', default=os.getcwd())
def create_with_webhook(bot_name, certificate_path=os.getcwd()):
	# creates the telegram bot skeleton suited
	# to get updates by webHook
	click.echo('creating with webhook')
	os.mkdir(bot_name)
	os.chdir(os.path.abspath(bot_name))
	template = os.path.join(os.path.dirname(tbtbot.__file__), 'apptemplate')
	cert_path = os.path.abspath(certificate_path)

	for entry in os.listdir(template):
		if os.path.isfile(os.path.join(template, entry)):
			with open(os.path.join(template, entry)) as f:
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
	return


# @main.command()
# @click.option('--bot_name', prompt=True)
def create_with_getUpdates(bot_name):
	# creates the telegram bot skeleton without
	# webhook functionality for some reasons
	# for example when the host hasn't static ip
	click.echo('creating with getUpdates')
	os.mkdir(bot_name)
	os.chdir(os.path.abspath(bot_name))
	template = os.path.join(os.path.dirname(tbtbot.__file__), 'apptemplate')

	for entry in os.listdir(template):
		if os.path.isfile(os.path.join(template, entry)):
			with open(os.path.join(template, entry)) as f:
				with open(entry, 'w') as w:
					if entry == '.env.example':
						w.write(templatestrings.env2template)
					elif entry == 'configuration.py':
						w.write(templatestrings.config2template)
					else:
						w.write(f.read())
	return


@click.command('create_bot', short_help='Create grand new bot in cwd')
@click.option('--bot_name', prompt="Please, specify a name for your bot")
@click.option(
	'--update_type', 
	prompt="Ok, how do you want to get your updates?\n1 webhooks / 2 long polling",
	type=click.Choice(['1', '2']))
@pass_context
def cli(context):
	"""Create grand new bot in cwd"""
	if int(updates_type) is 1:
		if click.confirm('Want to create self-signed certificate? [Yes/No]'):
			cert_path = create_certificate(bot_name)
			if cert_path is False:
				exit('Couldn\'t create certificate')
			create_with_webhook(bot_name, cert_path)
		else:
			create_with_webhook(bot_name)
	if int(updates_type) is 2:
		create_with_getUpdates(bot_name)
	click.echo(click.style('DONE!', fg='green'))
	return