# kraph

[![PyPI version](https://badge.fury.io/py/kraph.svg)](https://pypi.org/project/kraph/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/kraph.svg)](https://pypi.python.org/pypi/kraph/)

The python client for kraph, the [Arkitekt](https://arkitekt.live) knowledge graph service built
around Apache AGE: recording claims about entities, events, measurements and metrics, backed by the
structures (images, tables, …) that are evidence for them, and drawing them into graphs.

## Installation

```bash
pip install kraph
```

With arkitekt, `pip install "arkitekt[rekuest,kraph]"` brings it in.

## Concepts

- **Claims** — an entity exists, a structure measures it, two things are related — are recorded
  under a *term*, a word your organization owns, never under a graph. Retracting a claim records a
  position rather than deleting anything.
- **Graphs** are views. A graph declares *categories* (entity, relation, measurement, event, …)
  that say what its words mean, and draws the claims made under those words.

## Usage

Every kraph operation is a method of the `Kraph` client, in a blocking and an `a`-prefixed async
flavour (`kraph.create_graph(...)`, `await kraph.acreate_graph(...)`). What a call returns remembers
the client, so follow-ups from a result go through the same client.

### In an arkitekt app

Add the service to your app and ask for `kraph: Kraph`; the client is injected by annotation.
Graphs, categories, structures, metrics, terms and more travel between actions by id
(`@kraph/graph`, `@kraph/entitycategory`, `@kraph/structure`, `@kraph/term`, …), so an action can
take and return them directly:

```python
from arkitekt import App, run
from kraph import Kraph, kraph_service

app = App("neuron-claims", "0.1.0", services=[kraph_service])


@app.action
def claim_neuron(kraph: Kraph) -> str:
    """Claim Neuron

    Records that a neuron exists.
    """
    asserted = kraph.assert_entity_exists(
        term="Neuron", supporting_evidence=[], derived_from=[], same_as=[]
    )
    return asserted.instance.id


if __name__ == "__main__":
    run(app)
```

### From a script

```python
from arkitekt import easy
from kraph import kraph_service

with easy("my-script", kraph_service) as kraph:
    graph = kraph.create_graph(name="Neurons", backfill=False)
    kraph.create_entity_category(
        key="Neuron",
        ontology_references=[],
        property_definitions=[],
        graph=graph.id,
        backfill=True,
    )

    asserted = kraph.assert_entity_exists(
        term="Neuron", supporting_evidence=[], derived_from=[], same_as=[]
    )
    print(asserted.is_drawn)  # True: the graph declares "Neuron", so it draws the claim
```

## Testing

```bash
uv run pytest -m "not integration"   # no server needed
uv run pytest -m integration          # a real kraph via dokker
```

See [RELEASING.md](RELEASING.md) for how versions are cut.
