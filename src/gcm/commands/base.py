from pathlib import Path

import click

from ..utils import pretty_name
from .context import Context
from .validators import validate_package_name

CCACHE_DIR = Path('/var/cache/ccache')
ENV_DIR = Path('/etc/portage/env')
PACKAGE_ENV_DIR = Path('/etc/portage/package.env')

ENV_CCACHE_PATH = PACKAGE_ENV_DIR / 'ccache'

ENABLE_TEXT = '{package}\t{package}/ccache.env\n'
DISABLE_TEXT = f'# {ENABLE_TEXT}'

PACKAGE_NAME = pretty_name('{package}')


def ensure_desired_env_line(desired: str, undesired: str) -> None:
    ENV_CCACHE_PATH.touch()
    with ENV_CCACHE_PATH.open('r+') as ccache:
        ccache.seek(0)
        lines = ccache.readlines()
        written = desired in lines
        if undesired in lines:
            ccache.seek(0)
            for line in lines:
                if line == undesired:
                    if not written:
                        ccache.write(desired)
                        written = True
                else:
                    ccache.write(line)
            ccache.truncate()
        elif not written:
            ccache.write(desired)


class Command(click.Command):
    INVOKE_MESSAGE: str

    context_class = Context

    # https://github.com/python/mypy/issues/15015
    @staticmethod
    def callback(package: str) -> int | None:  # type: ignore[override]
        raise NotImplementedError

    def __init__(self) -> None:
        name = self.__class__.__name__.lower()
        click.BaseCommand.__init__(self, name)

        self.params = [
            click.Argument(['package'], callback=validate_package_name)
        ]
        self.help = self.__class__.__doc__
        self.epilog = None
        self.options_metavar = '[OPTIONS]'
        self.short_help = None
        self.add_help_option = True
        self.no_args_is_help = False
        self.hidden = False
        self.deprecated = False

    def invoke(self, ctx: Context) -> None:  # type: ignore[override]
        click.echo(self.INVOKE_MESSAGE.format(**ctx.params))
        code = super().invoke(ctx)
        if code:
            ctx.abort(code)
        click.echo(click.style('Done :-)', 'green'))
