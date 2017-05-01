import os
import subprocess

import click


def get_openssl_command(bot_name):
	return [
		"openssl",
		"req", "-newkey", "rsa:2048", "-sha256", "-nodes",
		"-keyout", "%s_private.key" % bot_name,
		"-x509", "-days", "365", "-out", "%s_public.pem" % bot_name
	]


@click.command('create_ssl_cert', short_help='Create self signed certificate for bot')
@click.option('--path', prompt=True)
@click.option('--bot_name', prompt=True)
def cli(path, bot_name):
	"""Create self signed certificate for bot"""
	try:
		os.chdir(path)
	except FileNotFoundError:
		click.echo(click.style('Danger! Looks like there is no such a directory.'))
		if click.confirm('Use current directory instead?', abort=True):
			path = os.getcwd()
		pass
	rtncode = subprocess.call(get_openssl_command(bot_name))
	if not rtncode: # then child process returned 0 which means success
		click.echo("Self-signed certificate is created in '%s'" % os.path.abspath(path))
		return path
	# TODO: is this right thing to do?
	raise IOError('Couldnt create')