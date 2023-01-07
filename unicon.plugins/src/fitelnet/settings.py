from unicon.plugins.generic.settings import GenericSettings

# see GenericSettings class to confirm default value

class FitelnetSettings(GenericSettings):

    def __init__(self):
        super().__init__()

        self.CONNECTION_TIMEOUT = 60 * 5

        # overwrite init_exec_commands
        self.HA_INIT_EXEC_COMMANDS = ['no more']

        # overwrite init_config_commands
        self.HA_INIT_CONFIG_COMMANDS = []

        # append ERROR_PATTERN
        self.ERROR_PATTERN += [
            r"<ERROR> Invalid input detected at '\^' marker\.",
            r"<ERROR> '\S+' is Unrecognized command",
            r"<ERROR> Unrecognized command",
        ]

        # append CONFIGURE_ERROR_PATTERN
        self.CONFIGURE_ERROR_PATTERN += [
            r"<ERROR> Invalid input detected at '\^' marker\.",
            r'\S+: No such file or directory',
        ]

        # see less_prompt_handler in statements.py
        self.LESS_CONTINUE = ' '

        # overwrite RELOAD_TIMEOUT, see services.py
        # interval 30 sec, 20 attempts, total 600 sec
        self.RELOAD_RECONNECT_ATTEMPTS = 20 # default 3
        self.RELOAD_WAIT = 30               # default 240
        self.RELOAD_TIMEOUT = 600           # default 300
