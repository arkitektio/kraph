from .kraph import Kraph

__all__ = ["Kraph"]

# Marks every type kraph sends by id, so an app using `Kraph` finds them.
from . import structures as _structures  # noqa: E402, F401
