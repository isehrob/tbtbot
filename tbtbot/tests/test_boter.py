import os
import pytest
from click.testing import CliRunner

from tbtbot.tbtboter import cli
from tbtbot.tbtboter.commands.cmd_create_bot import make_config_file


@pytest.mark.parametrize("cmd", [
	'start', 'set_webhook', 'drop_webhook', 
	'webhook_info', 'list_bot_commands', 'sync_db'
])
def test_call_config_required_cmd_outside_of_bot_folder(cmd):
	runner = CliRunner()
	result = runner.invoke(cli.main, [cmd])
	assert type(result.exception) is SystemExit
	assert 'Couln\'t import configuration!' in result.output
