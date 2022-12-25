from unicon.plugins.generic.settings import GenericSettings

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
        self.RELOAD_WAIT = 300     # default 240
        self.RELOAD_TIMEOUT = 360  # default 300
