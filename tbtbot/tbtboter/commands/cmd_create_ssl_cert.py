import click
from tbtbot.tbtboter.cli import pass_context


@click.command('create_ssl_cert', short_help='Create self signed certificate for bot')
@click.option('--path', prompt=True, default=lambda: os.getcwd())
@pass_context
def cli(path):
	"""Create self signed certificate for bot"""
	try:
		os.chdir(path)
	except FileNotFoundError:
		click.echo(click.style('Danger! Looks like there is no such a directory.'))
		if click.confirm('Use current directory instead?', abort=True):
			path = os.getcwd()
		pass
	rtncode = subprocess.call([
		"openssl",
		"req", "-newkey", "rsa:2048", "-sha256", "-nodes",
		"-keyout", "%s_private.key" % bot_name,
		"-x509", "-days", "365", "-out", "%s_public.pem" % bot_name
	])
	if not rtncode: # then child process returned 0 which means success
		click.echo("Self-signed certificate is created in '%s'" % os.path.abspath(path))
		return path
	return False