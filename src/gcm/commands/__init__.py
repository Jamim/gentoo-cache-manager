from .base import Command
from .disable import Disable
from .enable import Enable

COMMANDS: dict[str, type[Command]] = {
    command.__name__.lower(): command for command in [Enable, Disable]
}
