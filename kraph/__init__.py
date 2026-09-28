from .kraph import Kraph


# The service is declared with arkitekt-spec, a core dependency: it is always there.
from .arkitekt import kraph as kraph_service

__all__ = ["Kraph", "kraph_service"]
