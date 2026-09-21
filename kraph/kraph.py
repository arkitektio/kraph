"""The kraph client, and how it executes its generated operations.

Every operation of the API is a method of the generated ``KraphApi`` (see
``kraph/api/schema.py``), and each one hands its operation class and variables
to a method of ``self``: ``execute``/``aexecute`` for queries and mutations,
``subscribe``/``asubscribe`` for subscriptions. :class:`Kraph` implements those
four over its rath. Nothing is looked up. The objects a call returns remember the
client it was called on (and its rath and datalayer), so what they fetch later
(``.download()``, ``.wait_until_projected()``) goes through the same client.

Variables are dumped with ``exclude_none=True``. turms emits ``default=None`` for any input
field the schema gave a non-null default — ``[]``, ``false``, ``"0.0.1"`` — so serializing None
would send an explicit null where the server requires a value, and every nested definition input
would be rejected. Omitting instead lets the server apply its own default. Nothing is lost: every
nullable field in this schema already defaults to null, so omitting and sending null mean the
same thing.
"""

from collections.abc import AsyncGenerator, Generator
from typing import Any

from koil import unkoil, unkoil_gen
from koil.composition import Composition
from pydantic import Field
from rath.origin import origin_context
from rath.task import TASK_HEADER, TaskLike, current_task, token_of
from rath.turms.funcs import TOperation

from kraph.api.schema import KraphApi
from kraph.datalayer import DataLayer
from kraph.rath import KraphRath




class Kraph(Composition, KraphApi):
    """The kraph client.

    Every kraph operation is a method of it (``kraph.acreate_graph(...)``), and what
    a call returns remembers it, so a follow-up call from a result
    (``graph.wait_until_projected(seq)``, ``store.download()``) goes through the
    same client. Actions ask for it by annotation (``kraph: Kraph``) and are handed
    their app's client.
    """

    rath: KraphRath
    datalayer: DataLayer


    @staticmethod
    def _serialize(operation: type[TOperation], variables: dict[str, Any]) -> dict[str, Any]:
        # exclude_none, not exclude_unset: see the module docstring.
        return operation.Arguments(**variables).model_dump(by_alias=True, exclude_none=True)

    def _origin(self) -> dict[str, Any]:
        """What the objects of a result should remember: the client that fetched them."""
        return origin_context(client=self, rath=self.rath, datalayer=self.datalayer)

    def _headers(self, task: "TaskLike | None" = None) -> dict[str, Any] | None:
        """The per-call headers: the provenance token of the task this call is for.

        ``task`` when the caller named one, else whichever task is running. There
        is no per-task copy of this client: one instance serves every task, and
        what a request is attributed to is decided per call.
        """
        token = token_of(task)
        return {TASK_HEADER: token} if token else None

    def execute(
        self,
        operation: type[TOperation],
        variables: dict[str, Any],
        task: "TaskLike | None" = None,
    ) -> TOperation:
        """Executes a query or mutation in a blocking way."""
        return unkoil(
            self.aexecute,
            operation,
            variables,
            task=task if task is not None else current_task.get(),
        )

    async def aexecute(
        self,
        operation: type[TOperation],
        variables: dict[str, Any],
        task: "TaskLike | None" = None,
    ) -> TOperation:
        """Executes a query or mutation in a non-blocking way."""
        x = await self.rath.aquery(
            operation.Meta.document,
            self._serialize(operation, variables),
            headers=self._headers(task),
        )
        return operation.model_validate(x.data, context=self._origin())

    def subscribe(
        self,
        operation: type[TOperation],
        variables: dict[str, Any],
        task: "TaskLike | None" = None,
    ) -> Generator[TOperation, None, None]:
        """Subscribes to an operation in a blocking way."""
        return unkoil_gen(
            self.asubscribe,
            operation,
            variables,
            task=task if task is not None else current_task.get(),
        )

    async def asubscribe(
        self,
        operation: type[TOperation],
        variables: dict[str, Any],
        task: "TaskLike | None" = None,
    ) -> AsyncGenerator[TOperation, None]:
        """Subscribes to an operation in a non-blocking way."""
        async for event in self.rath.asubscribe(
            operation.Meta.document,
            self._serialize(operation, variables),
            headers=self._headers(task),
        ):
            yield operation.model_validate(event.data, context=self._origin())
