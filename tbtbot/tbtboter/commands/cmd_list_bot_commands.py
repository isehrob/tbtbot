import click
from tbtbot.tbtboter.cli import pass_context, needs_config


@click.command('list_bot_commands', short_help='Lists available commands set for your bot')
@pass_context
@needs_config
def cli(context):
	"""Lists available commands set for your bot"""
	def remove_slash(cmd):
		return cmd[1:]

	routes = __import__(context.config.ROUTE_MODULE)
	click.echo('Available commands for your bot')
	for entry in routes.get_routes():
		try:
			cmd, __, __, desc = entry
		except ValueError:
			cmd = entry[0]
			desc = ''
		cmd = remove_slash(cmd)
		click.echo(click.style('%s - %s' % (cmd, desc), fg='green'))