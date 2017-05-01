"""
	Here we test our main console utility functionality
"""
import os

import pytest
import mock
from click.testing import CliRunner

from tbtbot.apptemplate import template_strings as tstrings
from tbtbot.tbtboter import cli
from tbtbot.tbtboter.commands.cmd_create_bot import (
	make_config_file, make_env_file, set_env
)
from tbtbot.tbtboter import commands



def make_fake_config():
	""" Utility function which creates config files in 
		isolated by click directory to stop the main cli 
		tool from complining about the absence of config files
	"""
	make_config_file(tstrings.update_config_template)
	make_env_file(tstrings.update_env_template)
	set_env()


@pytest.fixture
def runner():
	return CliRunner()


@pytest.mark.parametrize("cmd", [
	'start', 'set_webhook', 'drop_webhook', 
	'webhook_info', 'list_bot_commands', 'sync_db'
])
def test_call_config_required_cmd_outside_of_bot_folder(runner, cmd):
	result = runner.invoke(cli.main, [cmd])
	assert type(result.exception) is SystemExit
	assert 'Couln\'t import configuration!' in result.output


def test_create_ssl_cert_command_invalid_path(runner):
	""" This test must rise SystemExit because we are giving nonexistent directory name
		which casues to prompt: "Use current dir?" then gets again 'koko' and aborts
	"""
	with runner.isolated_filesystem():
		make_fake_config()
		result = runner.invoke(cli.main, ['create_ssl_cert', '--path'], input='koko\nchocolate')
		assert type(result.exception) == SystemExit
		assert 'Error: --path option requires an argument' in result.output


def test_create_ssl_cert_failed(runner):
	"""In this test create_ssl_cert command fails to create keys in koko dir"""
	with runner.isolated_filesystem():
		make_fake_config()
		os.mkdir('koko')
		with mock.patch('subprocess.call') as mocked_call:
			subprocess_cmd = commands.cmd_create_ssl_cert.get_openssl_command
			mocked_call.return_value = 1
			result = runner.invoke(cli.main, ['create_ssl_cert'], input="koko\nchocolate")
			assert mocked_call.called == True
			assert mocked_call.called_once_with(subprocess_cmd('chocolate'))
			assert type(result.exception) == IOError


def test_create_ssl_cert_succed(runner):
	"""In this test create_ssl_cert command successfully creates keys in koko dir"""
	with runner.isolated_filesystem():
		make_fake_config()
		os.mkdir('koko')
		with mock.patch('subprocess.call') as mocked_call:
			mocked_call.return_value = 0
			result = runner.invoke(cli.main, ['create_ssl_cert'], input="koko\nchocolate")
			assert mocked_call.called == True
			assert 'Self-signed certificate is created in' in result.output
			assert 'koko' in result.output


def test_create_ssl_cert_succed_in_current_directory(runner):
	""" In this test create_ssl_cert command successfully creates keys in current dir
		after unsuccessfull attempt with an nonexsistant directory
	"""
	with runner.isolated_filesystem():
		make_fake_config()
		with mock.patch('subprocess.call') as mocked_call:
			mocked_call.return_value = 0
			result = runner.invoke(cli.main, ['create_ssl_cert'], input="koko\nchocolate\ny")
			assert mocked_call.called == True
			assert 'Self-signed certificate is created in' in result.output
