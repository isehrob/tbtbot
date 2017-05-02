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


def test_create_with_webhook_without_cert(runner):
	func = commands.cmd_create_bot.create_with_webhook
	with runner.isolated_filesystem():
		func('bujala', 'False')
		assert open('app.py')


def test_create_bot_with_upd(runner):
	"""In this test we test the create bot with updates method"""
	with runner.isolated_filesystem():
		result = runner.invoke(cli.main, ['create_bot', 'testbot'], input='2')
		assert "DONE" in result.output
		assert open('app.py')
		assert open('configuration.py')
		assert open('.env.example')


def test_create_bot_with_unknown_argument(runner):
	"""In this test we test the create bot with updates method"""
	with runner.isolated_filesystem():
		result = runner.invoke(cli.main, ['create_bot', 'new_bot'], input='2')
		assert "DONE" in result.output
		assert open('app.py')
		assert open('configuration.py')
		assert open('.env.example')