import click
from tbtbot.tbtboter.cli import pass_context, needs_config


@click.command('set_webhook', short_help='Sets a webhook for your bot')
@pass_context
@needs_config
def cli(context):
	"""Sets a webhook for your bot"""
	click.echo('setting webhook for', context.config.API)
	files = {
		'certificate': ('certificate', open(context.config.CERTFILE, 'rb')),
	}
	data = {'url': context.config.WEBHOOK_URL}
	url = config.API % 'setWebhook'
	rp = requests.post(url, files=files, data=data)
	click.echo('result of setWebhook: ', rp.status_code, rp.text, rp.reason)