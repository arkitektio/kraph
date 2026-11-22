# The service is declared with arkitekt-spec, a core dependency: it is always there.
from .arkitekt import kraph as kraph_service
from .kraph import Kraph

__all__ = ["Kraph", "kraph_service"]
