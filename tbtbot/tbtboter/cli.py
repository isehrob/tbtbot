# got from: https://github.com/pallets/click/blob/master/examples/complex/complex/cli.py
import os
import sys
import click

from tbtbot.lib.utils import check_bot_config


CONTEXT_SETTINGS = dict(auto_envvar_prefix='TBTBOT')


class Context():

    def __init__(self, *args, **kwargs):
        self.verbose = False
        self.home = os.getcwd()
        self.config = None

pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))

def needs_config(func):
    """Decorator function which ensures that the configuration of bot is present"""
    def wrapper(ctx, *args, **kwargs):
        result = None
        if ctx.config is None:
            try:
                # putting current path into PYTHONPATH so we could
                # import module from the bots directory if it is
                sys.path.insert(0, os.getcwd())
                config = __import__('configuration')
            except ImportError as e:
                sys.path.pop(0)
                error_ms = '%s\n%s' % ('Couln\'t import configuration!',
                    'Please, go to the directory where your bot code lives and then try')
                exit(click.style(error_ms, fg='red'))
            else:
                check_bot_config(config)
                ctx.config = config
                result = func(ctx, *args, **kwargs)
            finally:
                sys.path.pop(0)
        return result
    return wrapper


class ComplexCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('tbtbot.tbtboter.commands.cmd_' + name, None, None, ['cli'])
        except ImportError as e:
            raise e
        return mod.cli


@click.command(cls=ComplexCLI, context_settings=CONTEXT_SETTINGS)
@pass_context
def main(ctx):
    """A complex command line interface."""
    pass