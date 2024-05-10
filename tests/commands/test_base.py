import io
from unittest.mock import call, patch

import pytest
from gcm.commands.base import PACKAGE_NAME, Command, ensure_desired_env_line

DUMMY_CCACHE = """# foo
bar
# foo
# baz
"""


@pytest.mark.parametrize(
    'desired,undesired,expected',
    (
        ('foo\n', '# foo\n', 'foo\nbar\n# baz\n'),
        ('bar\n', '# bar\n', '# foo\nbar\n# foo\n# baz\n'),
        ('baz\n', '# baz\n', '# foo\nbar\n# foo\nbaz\n'),
        ('new\n', '# new\n', '# foo\nbar\n# foo\n# baz\nnew\n'),
        ('# foo\n', 'foo\n', '# foo\nbar\n# foo\n# baz\n'),
        ('# bar\n', 'bar\n', '# foo\n# bar\n# foo\n# baz\n'),
        ('# baz\n', 'baz\n', '# foo\nbar\n# foo\n# baz\n'),
        ('# new\n', 'new\n', '# foo\nbar\n# foo\n# baz\n# new\n'),
    ),
)
@patch('gcm.commands.base.ENV_CCACHE_PATH')
def test_ensure_desired_env_line(
    env_ccache_path, desired, undesired, expected
):
    ccache = io.StringIO(DUMMY_CCACHE)
    env_ccache_path.open.return_value.__enter__.return_value = ccache

    ensure_desired_env_line(desired, undesired)

    env_ccache_path.touch.assert_called_once()
    env_ccache_path.open.assert_called_once_with('r+')
    assert ccache.getvalue() == expected


def test_command_callback_not_implemented():
    with pytest.raises(NotImplementedError):
        Command.callback('app-misc/foo')


class DummyCommand(Command):
    """Do nothing."""

    INVOKE_MESSAGE = f'Doing nothing with {PACKAGE_NAME}'

    callback_is_called = False

    def callback(self, package):
        self.callback_is_called = True
        assert package == 'app-misc/foo'


@patch('click.echo')
def test_command_invoke(echo):
    command = DummyCommand()

    with pytest.raises(SystemExit):
        command(['foo'])

    assert command.callback_is_called
    assert echo.call_args_list == [
        call('Doing nothing with \x1b[32m\x1b[1mapp-misc/foo\x1b[0m'),
        call('\x1b[32mDone :-)\x1b[0m'),
    ]
