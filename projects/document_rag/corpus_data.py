"""Frozen local corpus loading and synthetic actor directory."""
import json
from pathlib import Path

from projects.vector_search.contracts import Actor, Space

from .chunking import prepare
from .scripted import batch


HERE = Path(__file__).parent
DATA = HERE / "data"
SPACE = Space()
LOCAL_DSN = "postgresql://vector_app:local_vector_app@127.0.0.1:15438/vector_lab"
SCOPES = frozenset({"read", "ingest", "delete", "share"})
ACTORS = {"north-alice": Actor("north", "alice", SCOPES),
          "north-bob": Actor("north", "bob", SCOPES),
          "south-alice": Actor("south", "alice", SCOPES),
          "north-reader": Actor("north", "reader", frozenset({"read"})),
          "north-observer": Actor("north", "observer", frozenset())}


def catalog():
    return json.loads((DATA / "catalog.json").read_text())


def cases():
    return [json.loads(line) for line in (DATA / "questions.jsonl").read_text().splitlines()]


def seed(store):
    for row in catalog():
        actor = ACTORS[f"{row['tenant']}-{row['owner']}"]
        body = (HERE / "corpus" / row["file"]).read_text()
        pieces = prepare(row["id"], row["version"], body, batch)
        store.ingest(actor, row["id"], row["version"], body, SPACE, pieces, expected_count=len(pieces))
        for subject in row["grants"]:
            store.grant(actor, row["id"], subject, True)
        for subject in row["revoke"]:
            store.grant(actor, row["id"], subject, False)
        if row["deleted"]:
            store.delete(actor, row["id"])
