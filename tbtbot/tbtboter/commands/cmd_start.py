import click
from tbtbot.tbtboter.cli import pass_context


@click.command('start', short_help='Starts bot server')
@pass_context
def cli(context):
	"""Starts bot server"""
	app = __import__(context.config.APP_MODULE)
	click.echo('Starting the bot...')
	try:
		app.start_bot()
	except KeyboardInterrupt:
		click.echo('stopping the bot...')
		app.stop_bot()
		click.echo("BYE!")