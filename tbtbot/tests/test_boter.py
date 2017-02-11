import pytest
import argparse

from tbtbot.scripts import tbtboter



def test_pytest():
	assert 0 == 0

def test_pytest_again():
	assert 1 == 1

def test_boter_cmd_args(mocker):
	class ArgObject():
		pass

	parser = argparse.ArgumentParser()
	mocked_args = mocker.patch.object(parser, 'parse_args', autospec=True)
	obj = ArgObject()
	obj.serve = True
	mocked_args.return_value = obj

	assert tbtboter.main() == tbtboter.serve()