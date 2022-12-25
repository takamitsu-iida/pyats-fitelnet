from unicon.plugins.generic.connection_provider import GenericSingleRpConnectionProvider
from unicon.eal.dialogs import Dialog

from .statemachine import FitelnetStatements

# see __init__.py

class FitelnetConnectionProvider(GenericSingleRpConnectionProvider):

    def get_connection_dialog(self):

        statements = FitelnetStatements()

        # TODO: telnet login

        dialog = super().get_connection_dialog()
        dialog += Dialog([statements.bad_password_stmt])
        return dialog
