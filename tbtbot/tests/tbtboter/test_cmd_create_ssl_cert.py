"""
	Here we test our main console utility functionality
"""
import os
import sys

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


def test_create_ssl_cert_command_invalid_path(runner):
	""" This test must rise SystemExit because we are giving nonexistent directory name
		which casues to prompt: "Use current dir?" then gets again 'koko' and aborts
	"""
	with runner.isolated_filesystem():
		result = runner.invoke(cli.main, ['create_ssl_cert', '--path'], input='koko\nchocolate')
		assert type(result.exception) == SystemExit
		assert 'Error: --path option requires an argument' in result.output



def test_create_certificat_success(runner):
	func = commands.cmd_create_ssl_cert.create_certificate
	with runner.isolated_filesystem():
		with mock.patch('subprocess.call') as mocked_call:
			subprocess_cmd = commands.cmd_create_ssl_cert.get_openssl_command
			mocked_call.return_value = 0
			result = func('jeje')
			assert mocked_call.called == True
			assert mocked_call.called_once_with(subprocess_cmd('jeje'))
			assert 'ssl' in result


def test_create_certificat_fail(runner):
	func = commands.cmd_create_ssl_cert.create_certificate
	with runner.isolated_filesystem():
		with mock.patch('subprocess.call') as mocked_call:
			subprocess_cmd = commands.cmd_create_ssl_cert.get_openssl_command
			mocked_call.return_value = 1
			result = func('jeje')
			assert mocked_call.called == True
			assert mocked_call.called_once_with(subprocess_cmd('jeje'))
			assert result == False


def test_create_ssl_cert_failed(runner):
	"""In this test create_ssl_cert command fails to create keys in koko dir"""
	with runner.isolated_filesystem():
		os.mkdir('koko')
		commands.cmd_create_ssl_cert.create_certificate = mock.Mock(return_value=False)
		func = commands.cmd_create_ssl_cert.create_certificate
		result = runner.invoke(cli.main, ['create_ssl_cert'], input="chocolate\nkoko")
		assert func.called == True
		assert len(func.call_args) is 2
		assert len(os.listdir('koko')) == 0
		assert type(result.exception) == IOError


def test_create_ssl_cert_succed(runner):
	"""In this test create_ssl_cert command successfully creates keys in koko dir"""
	with runner.isolated_filesystem():
		os.mkdir('koko')
		commands.cmd_create_ssl_cert.create_certificate = mock.Mock(return_value=True)
		func = commands.cmd_create_ssl_cert.create_certificate
		result = runner.invoke(cli.main, ['create_ssl_cert'], input="chocolate\nkoko")
		assert func.called == True
		assert len(func.call_args) is 2
		assert 'koko' in result.output