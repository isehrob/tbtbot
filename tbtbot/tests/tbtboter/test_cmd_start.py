"""
	Here we test our main console utility functionality
"""
import os
import sys
# import shutil

import pytest
import mock
from click.testing import CliRunner

from tbtbot.tbtboter import cli
from tbtbot.tbtboter.commands.cmd_create_bot import set_env	



@pytest.fixture
def runner():
	return CliRunner()


def test_start_bot_command(runner):
	with runner.isolated_filesystem():
		# creating test bot
		runner.invoke(cli.main, ['create_bot', 'new_bot'], input='2')
		# creating `.env` file for testing purposes
		set_env()
		# adding current dir to the PYTHONPATH so we could patch module here
		sys.path.insert(0, os.getcwd())
		# raise Exception(sys.path)
		with mock.patch('app.start_bot') as mocked:
			result = runner.invoke(cli.main, ['start'])
			assert 'Starting the bot...' in result.output
			assert mocked.called == True
			assert mocked.called_once_with()
		sys.path.pop(0)

		# NOTICE: interesting things happening here
		# in /tmp/ directory click creates temporary directory
		# and in this dir this test creates temp bot files 
		# but after test evaluation temporary directory gets deleted
		# But here magic (in a sense that dumbs like me can't understand it).
		# Even if tempo bot files are not here anymore, my another test finds 
		# it's configuration somehow. Belove I emplicitly deleted files and checked
		# with os.chdir if directory here still it and it confirmed
		# BUT even after that configuration.py which is already deleted as you see
		# SUCCESSFULLY IMPORTED! I know nothing in python I guess

		# os.chdir('../')
		# shutil.rmtree('new_bot')
		# os.chdir('new_bot')
		# conf = __import__('configuration')
		# raise Exception('in start bot', os.listdir(os.getcwd()), str(conf))