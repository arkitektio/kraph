from typing import Protocol
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kraph.api.schema import EntityCategory


class GraphProtocol(Protocol):
    def get_entity_category_for_labe(
        self,
        label: str,
    ) -> "EntityCategory": ...

    def register_instance(
        self,
        instance,
    ) -> None: ...

    def register_relation(
        self,
        instance,
    ) -> None: ...
