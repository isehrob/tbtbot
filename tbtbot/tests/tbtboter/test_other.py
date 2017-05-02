"""
	Here we test our main console utility functionality
"""
import os
import importlib
import pytest

from click.testing import CliRunner

from tbtbot.tbtboter import cli


@pytest.mark.parametrize("cmd", [
	'start', #'set_webhook', 'drop_webhook', 
	# 'webhook_info', 'list_bot_commands', 'sync_db'
])
def test_call_config_required_cmd_outside_of_bot_folder(cmd):
	runner = CliRunner()
	with runner.isolated_filesystem():
		result = runner.invoke(cli.main, [cmd])
		import sys
		cnf = importlib.import_module('configuration')
		raise Exception(cnf)
		assert type(result.exception) is SystemExit
		assert 'Couln\'t import configuration!' in result.output