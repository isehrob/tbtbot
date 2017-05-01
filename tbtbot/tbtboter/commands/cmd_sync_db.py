import click
from tbtbot.tbtboter.cli import pass_context, needs_config


@click.command('sync_db', short_help='Syncs a db for your bot creating missing tables')
@pass_context
@needs_config
def cli(context):
	"""Syncs a db for your bot creating missing tables"""
	db = __import__(context.config.DB_MODULE)
	try:
		db.create_all()
	except Exception as e:
		error_ms = '%s\n%s' % ('Couln\'t create db tables!', e)
		raise Exception(click.style(error_ms, fg='red'))
	return True