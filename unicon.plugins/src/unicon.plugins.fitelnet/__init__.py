from unicon.bases.routers.connection import BaseSingleRpConnection

from .statemachine import FitelnetSingleRpStateMachine
from .provider import FitelnetConnectionProvider
from .services import FitelnetServiceList
from .settings import FitelnetSettings

class FitelnetSingleRPConnection(BaseSingleRpConnection):
    os = 'fitelnet'
    chassis_type = 'single_rp'
    state_machine_class = FitelnetSingleRpStateMachine
    connection_provider_class = FitelnetConnectionProvider
    subcommand_list = FitelnetServiceList
    settings = FitelnetSettings()
