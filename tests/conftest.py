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
from kraph.datalayer import DataLayer
from graphql import OperationType
from dataclasses import dataclass

project_path = os.path.join(os.path.dirname(__file__), "integration")
docker_compose_file = os.path.join(project_path, "docker-compose.yml")


async def token_loader() -> str:
    """Load the token from the private key file."""
    return "test"


@dataclass
class DeployedKraph:
    """Deployed Kraph instance."""

    deployment: Deployment
    kraph_watcher: LogWatcher
    minio_watcher: LogWatcher
    kraph: Kraph


@pytest.fixture(scope="session")
def deployed_app() -> Generator[DeployedKraph, None, None]:
    """Fixture to deploy the Kraph application using Docker Compose."""
    setup = local(docker_compose_file)
    setup.add_health_check(
        url=lambda spec: f"http://localhost:{spec.find_service('kraph').get_port_for_internal(80).published}/graphql",
        service="kraph",
        timeout=5,
        max_retries=10,
    )

    watcher = setup.create_watcher("kraph")
    minio_watcher = setup.create_watcher("minio")

    with setup:
        minio_url = f"http://localhost:{setup.spec.find_service('minio').get_port_for_internal(9000).published}"
        http_url = f"http://localhost:{setup.spec.find_service('kraph').get_port_for_internal(80).published}/graphql"
        ws_url = f"ws://localhost:{setup.spec.find_service('kraph').get_port_for_internal(80).published}/graphql"

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

        setup.up()

        setup.check_health()

        with kraph as kraph:
            deployed = DeployedKraph(
                deployment=setup,
                kraph_watcher=watcher,
                minio_watcher=minio_watcher,
                kraph=kraph,
            )

            yield deployed
