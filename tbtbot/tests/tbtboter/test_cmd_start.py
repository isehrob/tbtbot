"""
	Here we test our main console utility functionality
"""
import os
import sys
import shutil

import pytest
import mock
from click.testing import CliRunner

from tbtbot.apptemplate import template_strings as tstrings
from tbtbot.tbtboter import cli
from tbtbot.tbtboter.commands.cmd_create_bot import (
	make_config_file, make_env_file, set_env
)
from tbtbot.tbtboter import commands



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
		os.chdir('../')
		shutil.rmtree('new_bot')
		conf = __import__('configuration')
		raise Exception('in start bot' + str(conf))