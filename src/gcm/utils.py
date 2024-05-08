import portage
from portage.exception import PackageNotFound
from portage.versions import pkgsplit
from termcolor import colored


def pretty_name(name: str) -> str:
    return colored(name, 'green', attrs=['bold'])


def normalize_package_name(name: str) -> str:
    dbapi = portage.db[portage.root]['porttree'].dbapi
    pacakges = dbapi.match(name)
    if not pacakges:
        raise PackageNotFound(name)

    package: str = pkgsplit(pacakges[0])[0]
    return package
