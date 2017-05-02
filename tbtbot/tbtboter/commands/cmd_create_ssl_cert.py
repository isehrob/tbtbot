import os
import subprocess

import click


def get_openssl_command(bot_name):
	""" Extracting for testing purposes"""
	return [
		"openssl",
		"req", "-newkey", "rsa:2048", "-sha256", "-nodes",
		"-keyout", "%s_private.key" % bot_name,
		"-x509", "-days", "365", "-out", "%s_public.pem" % bot_name
	]


def create_certificate(bot_name, path=False):
	if not path:
		path = 'ssl'
		os.mkdir(path)
	os.chdir(path)
	params = get_openssl_command(bot_name)
	rtncode = subprocess.call(params)
	os.chdir('../')
	if rtncode is 0: # then child process returned 0 which means success
		return path
	# TODO: is this right thing to do?
	return False


@click.command('create_ssl_cert', short_help='Create self signed certificate for bot')
@click.option('--bot_name', prompt=True)
@click.option('--path', prompt=True)
def cli(bot_name, path):
	"""Create self signed certificate for bot"""
	try:
		os.path.isdir(path)
	except FileNotFoundError:
		click.echo(click.style('Danger! Looks like there is no such a directory.'))
		if click.confirm('Use current directory instead?', abort=True):
			result = create_certificate(bot_name)
	else:
		result = create_certificate(bot_name, path)
	if result:
		click.echo("Self-signed certificate is created in '%s'" % os.path.abspath(path))
		return result
	raise IOError(click.style('Couldn\'t create certificate!', fg='red'))
	