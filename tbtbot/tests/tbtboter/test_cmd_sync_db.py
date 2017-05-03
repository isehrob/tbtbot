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


def test_sync_db_command(runner):
	pass