"""Neo4j connection helper."""
import os

try:  # use the Windows certificate store (fixes SSL interception errors)
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(override=True)

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            os.environ["NEO4J_URI"],
            auth=(os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"]),
        )
    return _driver


def run_query(cypher: str, params: dict | None = None) -> list[dict]:
    """Run a READ query and return rows as a list of dicts."""
    driver = get_driver()
    records, _, _ = driver.execute_query(
        cypher,
        parameters_=params or {},
        database_=os.getenv("NEO4J_DATABASE", "neo4j"),
        routing_="r",
    )
    return [r.data() for r in records]