"""A pinned datalayer's stores trust its hub's certificate themselves, not via SSL_CERT_FILE.

obstore >= 0.11 verifies with the platform's verifier, which on macOS and Windows never reads
SSL_CERT_FILE: the hub's certificate has to reach each store.
"""

import os
from types import SimpleNamespace

import pytest
from fakts import Alias

from kraph.datalayer import DataLayer
from kraph.io.obstore import create_s3_store

HUB_CERTIFICATE = """-----BEGIN CERTIFICATE-----
MIIBMzCB26ADAgECAgEBMAoGCCqGSM49BAMCMBcxFTATBgNVBAMMDEFya2l0ZWt0
IGh1YjAeFw0yNjAxMDEwMDAwMDBaFw0zNTEyMzAwMDAwMDBaMBcxFTATBgNVBAMM
DEFya2l0ZWt0IGh1YjBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABOipTSOE+oBd
xKJHSWVaGWLqUmf8wK9hqIwK53vQupHv4EY05DnvYatyVaWZNFSSABXJyjVkUnCL
BQNljdPSRdajGDAWMBQGA1UdEQQNMAuCCWxvY2FsaG9zdDAKBggqhkjOPQQDAgNH
ADBEAiB3vd12o38Qp39iZKng0rOWnZkuBcIJGbVQxjImnPeo5wIgSGM06akz+rlV
l0hiBf+cli9Wi5pinz2yRynHAGCXoE8=
-----END CERTIFICATE-----
"""
"""A self-signed hub certificate, public half only: what a pinned alias carries."""


def test_a_pinned_datalayer_hands_its_store_the_hub_certificate_alone(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The store trusts the alias's certificate alone, and the environment is left alone."""
    monkeypatch.delenv("SSL_CERT_FILE", raising=False)
    alias = Alias(
        id="s3", host="localhost", port=2577, ssl=True, certificates=[HUB_CERTIFICATE]
    )
    datalayer = DataLayer.from_alias(alias)
    grant = SimpleNamespace(
        access_key="a", secret_key="s", session_token="", bucket="b", key="k"
    )

    store = create_s3_store(
        datalayer.endpoint_url,
        grant,
        proxy=datalayer.proxy,
        certificates=datalayer.certificates,
    )

    assert store.client_options["root_certificate"] == HUB_CERTIFICATE.strip().encode()
    assert str(store.client_options["disable_system_certificates"]).lower() == "true"
    assert "SSL_CERT_FILE" not in os.environ
