"""Context variables.

``current_graph`` and ``current_ontology`` used to live here, carrying the ambient graph that the
old ``with graph:`` DSL set. They are gone: in the evidence model no write names a graph, so an
ambient one has nothing to scope. What remains is the datalayer, which the upload and download
helpers resolve from context.
"""

import contextvars
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from kraph.datalayer import DataLayer

current_datalayer: contextvars.ContextVar[Optional["DataLayer"]] = contextvars.ContextVar(
    "current_datalayer", default=None
)
