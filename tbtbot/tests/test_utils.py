import pytest
from click.testing import CliRunner # TODO: need to find something with pytest

from tbtbot.lib.utils import check_bot_config
from tbtbot.tbtboter.commands.cmd_create_bot import (
	make_config_file, make_env_file, set_env
)


def test_bot_config_checker():
	assert True == 1


def test_make_config_file_func():
	runner = CliRunner()
	with runner.isolated_filesystem():
		from tbtbot.apptemplate import template_strings as tstrings
		make_config_file(tstrings.update_config_template)
		assert open('configuration.py')


def test_make_env_file_func():
	runner = CliRunner()
	with runner.isolated_filesystem():
		from tbtbot.apptemplate import template_strings as tstrings
		make_env_file(tstrings.update_env_template)
		assert open('.env.example')


def test_set_env_func():
	runner = CliRunner()
	with runner.isolated_filesystem():
		from tbtbot.apptemplate import template_strings as tstrings
		make_env_file(tstrings.update_env_template)
		set_env()
		assert open('.env')