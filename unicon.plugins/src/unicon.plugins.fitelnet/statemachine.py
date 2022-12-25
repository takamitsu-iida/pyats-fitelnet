from unicon.eal.dialogs import Dialog
from unicon.statemachine import State, Path
from unicon.statemachine import StateMachine

from .patterns import FitelnetPatterns
from .statements import FitelnetStatements

# see __init__.py

class FitelnetSingleRpStateMachine(StateMachine):

    def create(self):

        patterns = FitelnetPatterns()
        statements = FitelnetStatements()

        # 'disable' State definition
        disable = State('disable', patterns.disable_prompt)

        # 'enable' State definition
        enable = State('enable', patterns.enable_prompt)

        # 'config' State definition
        config = State('config', patterns.config_prompt)

        # from 'disable' to 'enable'
        # fx201-pe1>enable
        # password:
        # <WARNING> weak enable password: set the password
        # fx201-pe1#
        disable_to_enable = Path(disable, enable, 'enable',
                                 Dialog([statements.enable_password_stmt,
                                         statements.bad_password_stmt]))

        # from 'enable' to 'disable'
        # fx201-pe1#disable
        # fx201-pe1>
        enable_to_disable = Path(enable, disable, 'disable', None)

        # from 'enable' to 'config'
        # fx201-pe1#configure terminal
        # fx201-pe1(config)#
        enable_to_config = Path(enable, config, 'config terminal', None)

        # from 'config' to 'enable'
        # fx201-pe1(config)#end
        # fx201-pe1#
        config_to_enable = Path(config, enable, 'end', None)

        self.add_state(disable)
        self.add_state(enable)
        self.add_state(config)

        self.add_path(disable_to_enable)
        self.add_path(enable_to_disable)
        self.add_path(enable_to_config)
        self.add_path(config_to_enable)
