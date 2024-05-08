from pathlib import Path

from ..utils import pretty_name

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


class Command:
    START_MESSAGE: str

    @staticmethod
    def command(package: str) -> None:
        raise NotImplementedError

    @classmethod
    def execute(cls, package: str) -> None:
        print(cls.START_MESSAGE.format(package=package))
        cls.command(package)
