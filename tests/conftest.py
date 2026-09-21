import pytest
from dokker import Deployment, testing
from dokker.log_watcher import LogWatcher
import os
import socket
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


def _reserve_free_ports(count: int) -> list[int]:
    """Ask the OS for `count` distinct free TCP ports.

    All sockets are held open until every port has been assigned, so the kernel
    cannot hand out the same port twice within one call. They are released
    before compose binds them -- a race in theory, but the ephemeral range is
    large and this is what keeps concurrent runs (and the leftovers of a crashed
    one) from colliding on a fixed port.
    """
    sockets: list[socket.socket] = []
    try:
        for _ in range(count):
            sock = socket.socket()
            sock.bind(("127.0.0.1", 0))
            sockets.append(sock)
        return [int(sock.getsockname()[1]) for sock in sockets]
    finally:
        for sock in sockets:
            sock.close()


@pytest.fixture(scope="session")
def integration_ports() -> Generator[dict[str, int], None, None]:
    """Pick this run's host ports and point compose at them.

    Reserved rather than left to docker (`ports: - "80"`) because
    `Deployment.spec` is rendered by `docker compose config`, which is static:
    an unpublished port reads back as ``None`` and the test URLs would quietly
    become ``http://localhost:None`` instead of failing loudly.
    """
    kraph_port, rustfs_port = _reserve_free_ports(2)
    env = {"KRAPH_HOST_PORT": str(kraph_port), "RUSTFS_HOST_PORT": str(rustfs_port)}
    previous = {key: os.environ.get(key) for key in env}
    os.environ.update(env)
    try:
        yield {"kraph": kraph_port, "rustfs": rustfs_port}
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


async def token_loader() -> str:
    """Load the token from the private key file."""
    return "test"


@dataclass
class DeployedKraph:
    """Deployed Kraph instance."""

    deployment: Deployment
    kraph_watcher: LogWatcher
    rustfs_watcher: LogWatcher
    kraph: Kraph


@pytest.fixture(scope="session")
def deployed_app(integration_ports: dict[str, int]) -> Generator[DeployedKraph, None, None]:
    """Fixture to deploy the Kraph application using Docker Compose."""
    # testing(): a per-run `dokker-test-<hash>` project that is torn down on
    # exit, so concurrent or crashed runs (and sibling repos, which all name
    # their stack `integration`) never share containers.
    setup = testing(docker_compose_file)
    setup.add_health_check(
        url=lambda spec: f"http://localhost:{spec.find_service('kraph').get_port_for_internal(80).published}/graphql",
        service="kraph",
        timeout=5,
        # dokker sleeps `timeout` seconds between attempts: 20 x 5 s covers a
        # cold backend on a two-core runner, where 10 did not.
        max_retries=20,
    )

    watcher = setup.create_watcher("kraph")
    rustfs_watcher = setup.create_watcher("rustfs")

    with setup:
        setup.down()
        setup.pull()
        setup.inspect()

        rustfs_url = f"http://localhost:{setup.spec.find_service('rustfs').get_port_for_internal(9000).published}"
        http_url = f"http://localhost:{setup.spec.find_service('kraph').get_port_for_internal(80).published}/graphql"
        ws_url = f"ws://localhost:{setup.spec.find_service('kraph').get_port_for_internal(80).published}/graphql"

        datalayer = DataLayer(
            endpoint_url=rustfs_url,
        )

        print(f"RustFS URL: {rustfs_url}")
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
                rustfs_watcher=rustfs_watcher,
                kraph=kraph,
            )

            yield deployed


@pytest.fixture(scope="session")
def kraph(deployed_app: DeployedKraph) -> Kraph:
    """The deployment's client: every call in a test goes through it explicitly."""
    return deployed_app.kraph
