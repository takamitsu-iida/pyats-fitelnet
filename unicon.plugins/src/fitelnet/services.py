import logging

from unicon.eal.dialogs import Dialog

## create service from scratch
# from unicon.core.errors import SubCommandFailure
# from unicon.bases.routers.services import BaseService

## extend generic plugin services
from unicon.plugins.generic.service_implementation import Execute as GenericExecute
from unicon.plugins.generic.service_implementation import Configure as GenericConfigure
from unicon.plugins.generic.service_implementation import Reload as GenericReload
from unicon.plugins.generic import service_implementation as svc
from unicon.plugins.generic.utils import GenericUtils

from .statements import FitelnetStatements

logger = logging.getLogger(__name__)


class FitelnetExecute(GenericExecute):

    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)

        # if 'no more' is not sent, less pager is enabled
        self.is_pager_enabled = connection.init_exec_commands is not None and 'no more' not in connection.init_exec_commands

        # in case of pager enabled, add extra Dialog
        if self.is_pager_enabled:
            statements = FitelnetStatements()
            self.dialog += Dialog([statements.less_stmt])

    def call_service(self, *args, **kwargs):
        super().call_service(*args, **kwargs)

    def extra_output_process(self, output):
        # in case of pager enabled, strip ':'
        if self.is_pager_enabled:
            utils = GenericUtils()
            output = utils.remove_backspace_ansi_escape(output)
            output = output.replace('\r\n:\r', '\r\n')

        return output


class FitelnetConfigure(GenericConfigure):

    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)
        self.start_state = 'config'
        self.end_state = 'enable'
        self.valid_transition_commands = ['end']

    def call_service(self, command=[], reply=Dialog([]), timeout=None, *args, **kwargs):
        super().call_service(command, reply=reply, timeout=timeout, *args, **kwargs)


class FitelnetSave(GenericExecute):

    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)
        self.start_state = 'enable'
        self.end_state = 'enable'

    def call_service(self, *args, **kwargs):

        if 'moff' not in args:
            statements = FitelnetStatements()
            self.dialog += Dialog([statements.save_stmt])

        command = ' '.join(['save'] + list(args))

        super().call_service(command, **kwargs)


class FitelnetLoad(GenericExecute):

    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)
        self.start_state = 'enable'
        self.end_state = 'enable'

    def call_service(self, *args, **kwargs):

        if 'moff' not in args:
            statements = FitelnetStatements()
            self.dialog += Dialog([statements.load_stmt])

        command = ' '.join(['load'] + list(args))
        super().call_service(command, **kwargs)


class FitelnetRestore(GenericExecute):

    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)
        self.start_state = 'enable'
        self.end_state = 'enable'

    def call_service(self, *args, **kwargs):

        if 'moff' not in args:
            statements = FitelnetStatements()
            self.dialog += Dialog([statements.restore_stmt])

        command = ' '.join(['restore'] + list(args))
        super().call_service(command, **kwargs)


class FitelnetRefresh(GenericExecute):

    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)
        self.start_state = 'enable'
        self.end_state = 'enable'

    def call_service(self, *args, **kwargs):

        if 'moff' not in args:
            statements = FitelnetStatements()
            self.dialog += Dialog([statements.refresh_stmt])

        command = ' '.join(['refresh'] + list(args))
        super().call_service(command, **kwargs)


class FitelnetReset(GenericReload):

    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)
        self.start_state = 'enable'
        self.end_state = 'enable'
        self.timeout = connection.settings.RELOAD_TIMEOUT

    def call_service(self, *args, **kwargs):

        if 'moff' in args:
            dialog = Dialog([])
        else:
            statements = FitelnetStatements()
            dialog = Dialog([statements.reset_stmt])

        command = ' '.join(['reset'] + list(args))

        try:
            super().call_service(reload_command=command, dialog=dialog, timeout=self.timeout, kwargs=kwargs)
        except Exception:
            pass


#
# ServiceList, see __init__.py
#
class FitelnetServiceList:

    def __init__(self):
        self.execute = FitelnetExecute
        self.configure = FitelnetConfigure
        self.save = FitelnetSave
        self.load = FitelnetLoad
        self.restore = FitelnetRestore
        self.refresh = FitelnetRefresh
        self.reset = FitelnetReset

        # mixin common services
        self.send = svc.Send
        self.sendline = svc.Sendline
        self.transmit = svc.Send
        self.receive = svc.ReceiveService
        self.receive_buffer = svc.ReceiveBufferService
        self.expect = svc.Expect
        self.expect_log = svc.ExpectLogging
        self.log_user = svc.LogUser
        self.log_file = svc.LogFile
        self.ping = svc.Ping