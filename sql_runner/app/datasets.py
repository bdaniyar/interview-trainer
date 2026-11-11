"""Trusted, immutable resources; never accept a client-provided path."""
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path

RESOURCE_ROOT = Path(__file__).resolve().parents[1] / "resources"
TABLES = ("users", "orders", "products", "order_items")
PRIMARY_KEYS = {"users": ("id",), "orders": ("id",), "products": ("id",),
                "order_items": ("order_id", "product_id")}
# This code pin intentionally duplicates the manifest digest: editing both SQL
# and the manifest must still fail unless a new dataset revision is introduced.
SHOP_DIGEST = "a1de3973eb4a2febc818c026def43716109e7ffde6b0bc46721e11d1b2fa4b97"


@dataclass(frozen=True)
class Dataset:
    id: str
    checksum: str
    schema: str
    seed: str


def load_dataset(dataset_id: str = "shop-v1") -> Dataset:
    if dataset_id != "shop-v1":
        raise ValueError("Unknown dataset revision")
    root = RESOURCE_ROOT / "shop-v1"
    schema = (root / "schema.sql").read_bytes()
    seed = (root / "seed.sql").read_bytes()
    manifest = json.loads((root / "manifest.json").read_text())
    digest = sha256(schema + b"\x00" + seed).hexdigest()
    if (manifest.get("id") != "shop-v1" or manifest.get("revision") != 1
            or manifest.get("postgres_major") != 17
            or digest != SHOP_DIGEST or manifest["checksum"] != digest
            or manifest["schema_sha256"] != sha256(schema).hexdigest()
            or manifest["seed_sha256"] != sha256(seed).hexdigest()):
        raise ValueError("Dataset integrity check failed; publish a new revision")
    return Dataset("shop-v1", digest, schema.decode(), seed.decode())


def validate_bank(bank: dict) -> None:
    dataset = load_dataset()
    for task in bank.get("sql", []):
        if (task.get("solution_sql") or task.get("kind") == "graded_select") and (task["schema"] != dataset.schema
                                         or task["seed"] != dataset.seed):
            raise ValueError(f"shop-v1 differs from practice bank task {task['id']}")
    from .grading_content import validate_graded_bank
    validate_graded_bank(bank)
