
class FitelnetPatterns:

    def __init__(self) -> None:

        # priv mode,  #
        # priv mode,  hostname#
        self.enable_prompt = r'^(.*?)%N{0,1}#\s?$'

        # user mode,  >
        # user mode,  hostname>
        self.disable_prompt = r'^(.*?)%N{0,1}>\s?$'

        # fx201-pe1(config)#
        # fx201-pe1(config-if-ge 1/1)#
        self.config_prompt = r'^(.*?)%N{0,1}\(config.*\)#\s*$'

        # enable
        # fx201-pe1>enable
        #
        # password:
        # fx201-pe1#
        self.enable_password = r'^password:\s?$'

        # fx201-pe1>enable
        #
        # password:
        # <ERROR> Authentication failed
        # password:
        self.bad_password = r'^<ERROR> Authentication failed$'

        # pager less is enabled by default
        self.less_prompt = r'\r\n:'

        # save
        # save ok?[y/N]:
        self.confirm_save = r'^(.*?)save ok\?\[y/N\]:\s?$'

        # load
        # load ok?[y/N]:
        self.confirm_load = r'^(.*?)load ok\?\[y/N\]:\s?$'

        # restore
        # restore ok?[y/N]:
        self.confirm_restore = r'^(.*?)restore ok\?\[y/N\]:\s?$'

        # refresh
        # refresh ok?[y/N]:
        self.confirm_refresh = r'^(.*?)refresh ok\?\[y/N\]:\s?$'

        # reset
        # reset ok?[y/N]:
        self.confirm_reset = r'^(.*?)reset ok\?\[y/N\]:\s?$'

        # telnet login
        self.login_prompt = r'login: *?'
        self.password_prompt = r'password: *?'
