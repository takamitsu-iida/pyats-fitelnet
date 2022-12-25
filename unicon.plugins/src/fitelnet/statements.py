#
# ダイアログを自動処理するための文(statements)を定義する
#

from unicon.eal.dialogs import Statement
from unicon.plugins.generic.statements import enable_password_handler
from unicon.plugins.generic.statements import bad_password_handler

from .patterns import FitelnetPatterns


def less_prompt_handler(spawn):

    # remove ':' here works properly, but junk '\r' left
    # spawn.match.match_output = spawn.buffer.replace('\r\n:', '\r\n')

    # to remove ':' see services.py
    spawn.match.match_output = spawn.buffer

    # send ' '
    spawn.send(spawn.settings.LESS_CONTINUE)



class FitelnetStatements():

    def __init__(self) -> None:

        patterns = FitelnetPatterns()

        # see statemachine.py
        self.enable_password_stmt = Statement(pattern=patterns.enable_password,
                                              action=enable_password_handler,
                                              args=None,
                                              loop_continue=True,
                                              continue_timer=False)

        # see statemachine.py
        # see provider.py
        self.bad_password_stmt = Statement(pattern=patterns.bad_password,
                                           action=bad_password_handler,
                                           args=None,
                                           loop_continue=False,
                                           continue_timer=False)

        # see services.py
        self.less_stmt = Statement(pattern=patterns.less_prompt,
                                   action=less_prompt_handler,
                                   args=None,
                                   loop_continue=True,
                                   continue_timer=False)

        # see services.py
        self.save_stmt = Statement(pattern=patterns.confirm_save,
                                   action='sendline(y)',
                                   args=None,
                                   loop_continue=True,
                                   continue_timer=False)

        # see services.py
        self.load_stmt = Statement(pattern=patterns.confirm_load,
                                   action='sendline(y)',
                                   args=None,
                                   loop_continue=True,
                                   continue_timer=False)

        # see services.py
        self.reset_stmt = Statement(pattern=patterns.confirm_reset,
                                   action='sendline(y)',
                                   args=None,
                                   loop_continue=True,
                                   continue_timer=False)
