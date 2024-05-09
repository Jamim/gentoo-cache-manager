import click
from click.core import Argument
from portage.exception import AmbiguousPackageName, PackageNotFound

from ..utils import normalize_package_name, pretty_name, warn
from .context import Context

# exit codes
OK = 0
AMBIGUOUS_PACKAGE_NAME = 1
PACKAGE_NOT_FOUND = 2


def validate_package_name(ctx: Context, param: Argument, package: str) -> str:
    try:
        package = normalize_package_name(package)
    except AmbiguousPackageName as error:
        warn(f'The short name "{package}" is ambiguous:')
        for name in error.args[0]:
            click.echo(f'    {pretty_name(name)}')
        warn('Please specify one of the above fully-qualified names instead.')
        ctx.abort(AMBIGUOUS_PACKAGE_NAME)
    except PackageNotFound:
        warn(f'There are no packages to satisfy "{package}".')
        ctx.abort(PACKAGE_NOT_FOUND)

    return package
