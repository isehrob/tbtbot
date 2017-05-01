import click
import tornado

from tbtbot.tbtboter.cli import pass_context, needs_config


@click.command('webhook_info', short_help='Displays current webhook set for your bot if any')
@pass_context
@needs_config
def cli(context):
	"""Displays current webhook set for your bot if any"""
	click.echo('getting webhookinfo for', context.config.API)
	rp = tornado.httpclient.HTTPClient().fetch(context.config.API % 'getWebhookInfo')
	click.echo(rp.body)