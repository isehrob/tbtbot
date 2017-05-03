"""
	Here we test our main console utility functionality
"""
# import os
# import importlib
import pytest

from click.testing import CliRunner

from tbtbot.tbtboter import cli


@pytest.mark.parametrize("cmd", [
	'start', 'set_webhook', 'drop_webhook', 
	'webhook_info', 'list_bot_commands', 'sync_db'
])
def test_call_config_required_cmd_outside_of_bot_folder(cmd):
	# NOTICE: interesting things happening here
	# in /tmp/ directory click creates temporary directory
	# and in this dir the other test creates temp bot files 
	# but after test evaluation temporary directory gets deleted
	# But here is the magic (in a sense that dumbs like me can't understand it).
	# Even if tempo bot files are not here anymore, this test finds 
	# it's configuration somehow. 
	# the only solution for now is to make pytest call this test file
	# before the one that causes this issue. So renamed this file from
	# test_other.py to test_ather.py - elegant solution!
	#  Guess pytest is responsible for this anomaly
	runner = CliRunner()
	with runner.isolated_filesystem():
		result = runner.invoke(cli.main, [cmd])
		# import sys
		# cnf = importlib.import_module('configuration')
		# raise Exception(os.listdir(os.getcwd()), cnf)
		assert type(result.exception) is SystemExit
		assert 'Couln\'t import configuration!' in result.output