import pytest
from dokker import local, Deployment
from dokker.log_watcher import LogWatcher
import os
from typing import Generator
from kraph.kraph import Kraph
from rath.links.auth import ComposedAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.graphql_ws import GraphQLWSLink
from rath.links.timeout import TimeoutLink
from rath.links.compose import compose
from kraph.rath import (
    KraphRath,
    UploadLink,
    SplitLink,
)
from kraph.api.schema import create_graph
from kraph.datalayer import DataLayer
from graphql import OperationType
from dataclasses import dataclass


async def token_loader() -> str:
    return "test"


minio_url = f"http://localhost:6889"
http_url = f"http://localhost:6888/graphql"
ws_url = f"ws://localhost:6888/graphql"

datalayer = DataLayer(
    endpoint_url=minio_url,
)

print(f"Minio URL: {minio_url}")
print(f"HTTP URL: {http_url}")
print(f"WS URL: {ws_url}")

y = KraphRath(
    link=compose(
        TimeoutLink(timeout=12),
        ComposedAuthLink(token_loader=token_loader, token_refresher=token_loader),
        UploadLink(datalayer=datalayer),
        SplitLink(
            left=AIOHttpLink(endpoint_url=http_url),
            right=GraphQLWSLink(ws_endpoint_url=ws_url),
            split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
        ),
    ),
)

kraph = Kraph(
    datalayer=datalayer,
    rath=y,
)

with kraph:
    print(
        create_graph(name="Christians GOLD GRAPH", description="A graph for Christians masterlist")
    )
