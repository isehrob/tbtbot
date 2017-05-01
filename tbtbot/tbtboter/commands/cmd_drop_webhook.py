import click
import tornado

from tbtbot.tbtboter.cli import pass_context, needs_config


@click.command('drop_webhook', short_help='Deletes current webhook if one exist')
@pass_context
@needs_config
def cli(context):
	"""Starts bot server"""
	click.echo('Deleting webhook', context.config.API)
	rp = tornado.httpclient.HTTPClient().fetch(context.config.API % 'deleteWebhook')
	click.echo('result of deleteWebhook\n ', rp.body)