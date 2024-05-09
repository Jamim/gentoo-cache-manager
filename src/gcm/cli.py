import click

import gcm
from .commands import COMMANDS


@click.group(help=gcm.__name__, commands=COMMANDS)
def cli() -> None:
    pass


if __name__ == '__main__':
    cli()
