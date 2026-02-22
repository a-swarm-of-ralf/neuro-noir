from __future__ import annotations

import time
from typing import Tuple, Optional

from neo4j import GraphDatabase
from neo4j.exceptions import (
    AuthError,
    ServiceUnavailable,
    ConfigurationError,
    Neo4jError,
    ClientError,
    DatabaseError,
)
from functools import lru_cache

from neuro_noir.core.config import Settings
from neuro_noir.core.report import md_report


@lru_cache(maxsize=1)
def connect_neo4j_cached(uri: str, user: str, pwd: str):
    """
    Create and cache a Neo4j driver connection. The cache ensures that we reuse the same 
    connection across multiple calls, which is more efficient and avoids issues with too 
    many open connections.

    Args:
        uri (str): The Bolt URI for the Neo4j server (e.g., "bolt://localhost:7687").
        user (str): The username for Neo4j authentication.
        pwd (str): The password for Neo4j authentication.

    Returns:
        A Neo4j driver instance connected according to the provided parameters.
    """
    return GraphDatabase.driver(uri, auth=(user, pwd))


def connect_neo4j(cfg: Settings, cache: bool = True):
    """
    Connect to Neo4j using the provided configuration. This function is a simple wrapper 
    around the cached connection function, allowing you to pass a Settings object directly.

    Args:
        cfg (Settings): The configuration object containing Neo4j connection details.

    Returns:
        A Neo4j driver instance connected according to the provided configuration.
    """
    if cache:
        return connect_neo4j_cached(cfg.NEO4J_URI, cfg.NEO4J_USERNAME, cfg.NEO4J_PASSWORD)
    else:
        return GraphDatabase.driver(cfg.NEO4J_URI, auth=(cfg.NEO4J_USERNAME, cfg.NEO4J_PASSWORD))


def delete_neo4j(cfg: Settings, cache: bool = True) -> None:
    driver = connect_neo4j(cfg, cache=cache)
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n").consume()


def test_db(cfg) -> Tuple[bool, str, str]:
    """
    Test a Neo4j connection by opening a session and running a simple query.

    Returns:
        (ok, error_message, report_md)
        ok: True if a connection + query succeeds, else False
        error_message: A human-readable error message if the connection fails.
        report_md: Markdown with:
          1) what went wrong
          2) what could have caused it
          3) how to fix it
    """
    start = time.perf_counter()

    uri = cfg.NEO4J_URI
    user = cfg.NEO4J_USERNAME

    driver = None
    try:
        driver = connect_neo4j(cfg, cache=False)

        with driver.session() as session:
            record = session.run("RETURN 1 AS test").single()
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        if record and record.get("test") == 1:
            return True, "✅ Neo4j connection successful", md_report(
                title="✅ Neo4j connection successful",
                what_went_wrong="Nothing went wrong — the driver connected and the test query returned the expected result.",
                likely_causes=[],
                how_to_fix=[],
                details=[
                    f"URI: `{uri}`",
                    f"User: `{user}`",
                    f"Database: `(default)`",
                    f"Elapsed: {elapsed_ms} ms",
                ],
            )

        return False, "⚠️ Neo4j connection test returned an unexpected result", md_report(
            title="⚠️ Neo4j connection test returned an unexpected result",
            what_went_wrong="A connection was established, but the test query did not return the expected value.",
            likely_causes=[
                "A proxy or middleware is intercepting requests and returning unexpected responses.",
                "A custom Neo4j setup or plugin is altering behavior (uncommon for `RETURN 1`).",
            ],
            how_to_fix=[
                "Try running the same query in Neo4j Browser: `RETURN 1 AS test`.",
                "If you’re using a proxy/load balancer, try connecting directly to Neo4j.",
                "If you have a custom setup, try `RETURN 1` and compare outputs.",
            ],
            details=[
                    f"URI: `{uri}`",
                    f"User: `{user}`",
                    f"Database: `(default)`",
                    f"Elapsed: {elapsed_ms} ms",
                ],
        )

    except AuthError as e:
        return False, "❌ Authentication failed", md_report(
            title="❌ Authentication failed",
            what_went_wrong="Neo4j rejected the username/password (or the authentication method).",
            likely_causes=[
                "Wrong username or password.",
                "You’re connecting to the wrong Neo4j instance (URI points elsewhere).",
                "The user exists but does not have permission to access the target database.",
                "Neo4j is configured for a different auth mechanism (rare in typical setups).",
            ],
            how_to_fix=[
                "Double-check your credentials (copy/paste carefully, watch for spaces).",
                "Verify the URI points to the right server (host/port).",
                "Log into Neo4j Browser with the same credentials to confirm they work.",
                "If using multi-database, ensure the user has access to that database (or try without specifying `database`).",
            ],
            details=[
                    f"URI: `{uri}`",
                    f"User: `{user}`",
                    f"Database: `(default)`",
                    f"Error: `{e}`"
                ],
        )

    except ServiceUnavailable as e:
        return False, "❌ Cannot reach Neo4j server", md_report(
            title="❌ Cannot reach Neo4j server",
            what_went_wrong="The Neo4j driver could not connect to the server (network/server unavailable).",
            likely_causes=[
                "Neo4j is not running (server is stopped).",
                "Wrong host or port in the URI (common: using 7687 vs 7474).",
                "Firewall / security group blocks the Bolt port (usually 7687).",
                "DNS name does not resolve from where your code runs.",
                "You’re using a routing URI (`neo4j://`) but connecting to a single instance that doesn’t support routing, or routing is misconfigured.",
            ],
            how_to_fix=[
                "Confirm Neo4j is running and listening on the Bolt port (default: 7687).",
                "Check the URI: it should look like `bolt://host:7687` or `neo4j://host:7687`.",
                "From the same machine, test connectivity: `nc -vz host 7687` (mac/linux) or `Test-NetConnection host -Port 7687` (PowerShell).",
                "If you’re not using a cluster, try `bolt://...` instead of `neo4j://...`.",
            ],
            details=[
                    f"URI: `{uri}`",
                    f"User: `{user}`",
                    f"Database: `(default)`",
                    f"Error: `{e}`"
                ],
        )

    except ConfigurationError as e:
        return False, "❌ Driver/configuration error", md_report(
            title="❌ Driver/configuration error",
            what_went_wrong="The Neo4j driver configuration is invalid (URI format, encryption settings, etc.).",
            likely_causes=[
                "URI has an invalid scheme or typo (e.g. `boltt://` instead of `bolt://`).",
                "TLS/encryption settings mismatch the server (server expects TLS but client doesn’t, or vice versa).",
                "Certificate verification fails when using encrypted connections.",
            ],
            how_to_fix=[
                "Verify the URI scheme is correct: `bolt://` or `neo4j://` (and includes host + port).",
                "If using Neo4j Aura or TLS, ensure encryption is enabled and certificates are handled properly.",
                "If you’re local/dev and intentionally not using TLS, use `bolt://` with the correct port and disable TLS only if your environment allows it.",
            ],
            details=[
                    f"URI: `{uri}`",
                    f"User: `{user}`",
                    f"Database: `(default)`",
                    f"Error: `{e}`"
                ],
        )

    except ClientError as e:
        # Often covers: database not found, permission issues, query syntax, etc.
        code = getattr(e, "code", None)
        return False, "❌ Neo4j rejected the request (client error)", md_report(
            title="❌ Neo4j rejected the request (client error)",
            what_went_wrong="Neo4j received the request but rejected it (permissions, database selection, or request details).",
            likely_causes=[
                "The specified database name does not exist.",
                "The user does not have access rights to that database.",
                "The server is in a mode that restricts queries (rare for `RETURN 1`).",
            ],
            how_to_fix=[
                "If you set a database name, verify it exists and is spelled correctly.",
                "Try connecting without specifying a database to use the default database.",
                "Check user roles/permissions in Neo4j (does this user have access?).",
            ],
            details=[
                f"URI: `{uri}`",
                f"User: `{user}`",
                f"Database: `(default)`",
                f"Neo4j code: `{code}`" if code else "Neo4j code: (not provided)",
                f"Error: `{e}`"
            ],
        )

    except DatabaseError as e:
        return False, "❌ Neo4j database error", md_report(
            title="❌ Neo4j database error",
            what_went_wrong="Neo4j encountered an internal database-side problem while processing the request.",
            likely_causes=[
                "The database is starting up, recovering, or under heavy load.",
                "Server-side configuration issues.",
                "Resource limits (memory/disk) on the Neo4j server.",
            ],
            how_to_fix=[
                "Check Neo4j server logs for the real root cause.",
                "Ensure the server has enough disk space and memory.",
                "Retry after a short wait if the server is restarting or recovering.",
            ],
            details=[
                    f"URI: `{uri}`",
                    f"User: `{user}`",
                    f"Database: `(default)`",
                    f"Error: `{e}`"
                ],
        )

    except Neo4jError as e:
        # Catch-all for other Neo4j-specific errors
        code = getattr(e, "code", None)
        return False, "❌ Neo4j returned an error", md_report(
            title="❌ Neo4j returned an error",
            what_went_wrong="Neo4j returned an error that doesn’t fit the common categories above.",
            likely_causes=[
                "A server-side restriction or policy.",
                "A cluster/routing issue.",
                "A mismatch between driver version and server capabilities (less common, but possible).",
            ],
            how_to_fix=[
                "Inspect the error code and message in the details below.",
                "Check Neo4j server logs for additional context.",
                "Confirm your Neo4j Python driver version is compatible with your Neo4j server version.",
            ],
            details=[
                    f"URI: `{uri}`",
                    f"User: `{user}`",
                    f"Database: `(default)`",
                    f"Error: `{e}`"
                ],
        )

    except Exception as e:
        return False, "❌ Unexpected error while testing Neo4j connection", md_report(
            title="❌ Unexpected error while testing Neo4j connection",
            what_went_wrong="Your code hit an unexpected Python exception (not a standard Neo4j driver error).",
            likely_causes=[
                "A bug in `connect_neo4j(self.cfg)` (e.g., returns None, wrong object type).",
                "Missing environment variables or config fields.",
                "A dependency/version issue in your Python environment.",
            ],
            how_to_fix=[
                "Print/inspect what `connect_neo4j(self.cfg)` returns and ensure it’s a Neo4j `Driver`.",
                "Check your config values (URI/user/password) are present at runtime.",
                "Look at the full stack trace to find the exact failing line.",
            ],
            details=[
                    f"URI: `{uri}`",
                    f"User: `{user}`",
                    f"Database: `(default)`",
                    f"Error: `{e}`"
                ],
        )

    finally:
        if driver is not None:
            try:
                driver.close()
            except Exception:
                # Don't hide the original error if close fails.
                pass


def delete_db(cfg: Settings, cache: bool = True) -> Tuple[bool, str, str]:
    """
    Delete all nodes and relationships in the Neo4j database. Use with caution, as this 
    will irreversibly remove all data.

    Args:
        cfg (Settings): The configuration object containing Neo4j connection details.
    """
    feedback = test_db(cfg)
    if not feedback[0]:
        return False, "Cannot delete database because connection test failed: " + feedback[1], feedback[2]
    try:
        delete_neo4j(cfg, cache=cache)
        return True, "✅ Neo4j database cleared successfully", md_report(
            title="✅ Neo4j database cleared successfully",
            what_went_wrong="Nothing went wrong — the database was cleared.",
            likely_causes=[],
            how_to_fix=[],
        )
    except Exception as e:
        return False, f"❌ Failed to clear Neo4j database: {e}", md_report(
            title="❌ Failed to clear Neo4j database",
            what_went_wrong="An error occurred while trying to clear the database.",
            likely_causes=[
                "The connection was lost after the test but before deletion.",
                "There’s a permissions issue preventing deletion.",
                "The server is in an unstable state (e.g., out of memory).",
            ],
            how_to_fix=[
                "Check the error message for clues about the failure.",
                "Ensure your Neo4j user has permissions to delete data.",
                "Check Neo4j server logs for any critical errors or resource issues.",
            ],
            details=[
                    f"URI: `{cfg.NEO4J_URI}`",
                    f"User: `{cfg.NEO4J_USERNAME}`",
                    f"Database: `(default)`",
                    f"Error: `{e}`"
                ],
        )