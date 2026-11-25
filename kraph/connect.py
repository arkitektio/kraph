"""How ``Kraph`` reaches a resolved deployment: its links and upload middleware."""

from arkitekt_spec.declare.wiring import Alias, TokenLoader
from fakts.contrib.rath.auth import FaktsAuthLink
from rath.links import compose
from rath.links.aiohttp import AIOHttpLink
from rath.links.dictinglink import DictingLink
from rath.links.graphql_ws import GraphQLWSLink
from rath.links.shrink import ShrinkingLink
from rath.links.split import SplitLink

from graphql import OperationType
from kraph.datalayer import DataLayer
from kraph.links.upload import UploadLink
from kraph.middleware.upload import UploadMiddleware
from kraph.rath import KraphRath


def kraph_rath(kraph: Alias, datalayer: DataLayer, tokens: TokenLoader) -> KraphRath:
    """The rath over http and ws, uploading files to ``datalayer`` first."""
    return KraphRath(
        # Files in a request (a model's weights) go to the datalayer first, as every service's do.
        middlewares=[UploadMiddleware(datalayer=datalayer)],
        link=compose(
            ShrinkingLink(),
            DictingLink(),
            FaktsAuthLink(token_loader=tokens),
            UploadLink(datalayer=datalayer),
            SplitLink(
                left=AIOHttpLink(
                    endpoint_url=kraph.to_http_path("graphql"),
                    proxy=kraph.proxy,
                    ssl_context=kraph.ssl_context(),
                ),
                right=GraphQLWSLink(
                    ws_endpoint_url=kraph.to_ws_path("graphql"),
                    proxy=kraph.proxy,
                    ssl_context=kraph.ssl_context(),
                ),
                split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
            ),
        ),
    )


__all__ = ["kraph_rath"]
