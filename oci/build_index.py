"""Write the OCI client/operation index that find_oci_api and list_oci_clients read.

Upstream discovers clients by importing every module of the OCI SDK (about
17,500 of them), which leaves the process at roughly 530 MiB for good. This
runs that discovery once, at image build time, and stores what the two tools
need in SQLite: per client its operations, their one-line summary and the
compact signature upstream would show. The server streams rows from it per
query instead of holding the SDK in memory.

Usage: python build_index.py OUTPUT.sqlite
"""

import os
import sqlite3
import sys

# Upstream switches to its IDCS HTTP mode when these are set.
os.environ.pop("ORACLE_MCP_HOST", None)
os.environ.pop("ORACLE_MCP_PORT", None)

from oracle.oci_cloud_mcp_server import server as upstream  # noqa: E402


def main(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
    db = sqlite3.connect(path)
    db.executescript(
        """
        CREATE TABLE clients (client_fqn TEXT PRIMARY KEY, module TEXT NOT NULL, class TEXT NOT NULL);
        CREATE TABLE operations (
            client_fqn TEXT NOT NULL,
            operation TEXT NOT NULL,
            summary TEXT NOT NULL,
            params TEXT NOT NULL,
            PRIMARY KEY (client_fqn, operation)
        );
        CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        """
    )
    clients = operations = 0
    for client_fqn, cls in upstream._discover_client_classes():
        db.execute(
            "INSERT INTO clients VALUES (?, ?, ?)",
            (client_fqn, client_fqn.rsplit(".", 1)[0], getattr(cls, "__name__", client_fqn.rsplit(".", 1)[-1])),
        )
        clients += 1
        for name, member in upstream._get_public_client_methods(cls):
            signature, doc = upstream._inspect_method(member)
            summary = doc.strip().partition("\n")[0] if doc else ""
            params = upstream._signature_to_display(name, signature)
            db.execute("INSERT INTO operations VALUES (?, ?, ?, ?)", (client_fqn, name, summary, params))
            operations += 1
    import oci

    db.executemany(
        "INSERT INTO meta VALUES (?, ?)",
        [("oci_version", oci.__version__), ("clients", str(clients)), ("operations", str(operations))],
    )
    db.commit()
    db.execute("VACUUM")
    db.close()
    print(f"indexed {clients} clients, {operations} operations (oci {oci.__version__})")


if __name__ == "__main__":
    main(sys.argv[1])
