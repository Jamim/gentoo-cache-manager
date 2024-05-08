import argparse
import sys
from functools import partial
from typing import Any

from portage.exception import AmbiguousPackageName, PackageNotFound
from termcolor import cprint

from .commands import COMMANDS
from .utils import normalize_package_name, pretty_name

# exit codes
OK = 0
AMBIGUOUS_PACKAGE_NAME = 1
PACKAGE_NOT_FOUND = 2

warn = partial(cprint, color='yellow')


def run(args: Any) -> int:
    package = args.package
    try:
        package = normalize_package_name(package)
    except AmbiguousPackageName as error:
        warn(f'The short name "{package}" is ambiguous:')
        for name in error.args[0]:
            print(f'    {pretty_name(name)}')
        warn('Please specify one of the above fully-qualified names instead.')
        return AMBIGUOUS_PACKAGE_NAME
    except PackageNotFound:
        warn(f'There are no packages to satisfy "{package}".')
        return PACKAGE_NOT_FOUND

    command = COMMANDS[args.command]
    command.execute(package)

    return OK


def parse_args() -> Any:
    parser = argparse.ArgumentParser(description='Gentoo Cache Manager')
    parser.add_argument('command', type=str, choices=COMMANDS.keys())
    parser.add_argument('package', type=str)
    return parser.parse_args()


def main() -> None:
    status = run(parse_args())
    if status:
        cprint('Aborted!', 'red')
    else:
        cprint('Done :-)', 'green')
    sys.exit(status)


if __name__ == '__main__':
    main()
