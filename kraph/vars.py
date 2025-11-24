import contextvars
from kraph.protocols import GraphProtocol

current_ontology = contextvars.ContextVar("current_ontology")
current_graph: contextvars.ContextVar[GraphProtocol] = contextvars.ContextVar(
    "current_graph"
)
current_datalayer = contextvars.ContextVar("current_datalayer")
