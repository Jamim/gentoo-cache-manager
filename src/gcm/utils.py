import click
import portage
from portage.exception import PackageNotFound
from portage.versions import pkgsplit


def warn(message: str) -> None:
    click.echo(click.style(message, 'yellow'))


def pretty_name(name: str) -> str:
    return click.style(name, 'green', bold=True)


def normalize_package_name(name: str) -> str:
    dbapi = portage.db[portage.root]['porttree'].dbapi
    pacakges = dbapi.match(name)
    if not pacakges:
        raise PackageNotFound(name)

    package: str = pkgsplit(pacakges[0])[0]
    return package
