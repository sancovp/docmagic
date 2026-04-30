"""Neo4j graph backend — optional power-user backend."""
from docmagic.graph.base import GraphBackend

class Neo4jBackend(GraphBackend):
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password"):
        try:
            from neo4j import GraphDatabase
        except ImportError:
            raise ImportError("Neo4j backend requires: pip install docmagic[neo4j]")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def add_node(self, name: str, label: str, **props) -> None:
        props_str = ", ".join(f"n.{k} = ${k}" for k in props)
        set_clause = f", {props_str}" if props_str else ""
        self.driver.execute_query(
            f"MERGE (n:{label} {{name: $name}}) SET n.name = $name{set_clause}",
            name=name, **props
        )

    def add_edge(self, source: str, target: str, rel_type: str, **props) -> None:
        self.driver.execute_query(
            f"MATCH (a {{name: $source}}) MATCH (b {{name: $target}}) MERGE (a)-[r:{rel_type}]->(b)",
            source=source, target=target
        )

    def get_node(self, name: str) -> dict | None:
        result = self.driver.execute_query(
            "MATCH (n {name: $name}) RETURN n", name=name
        )
        if result[0]:
            node = result[0][0]["n"]
            return dict(node)
        return None

    def get_edges(self, source: str = None, target: str = None, rel_type: str = None) -> list[dict]:
        where_parts = []
        params = {}
        if source:
            where_parts.append("a.name = $source")
            params["source"] = source
        if target:
            where_parts.append("b.name = $target")
            params["target"] = target
        where = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
        rel = f"[r:{rel_type}]" if rel_type else "[r]"
        result = self.driver.execute_query(
            f"MATCH (a)-{rel}->(b) {where} RETURN a.name AS source, type(r) AS rel_type, b.name AS target",
            **params
        )
        return [dict(r) for r in result[0]]

    def query(self, pattern: str, **params) -> list[dict]:
        result = self.driver.execute_query(pattern, **params)
        return [dict(r) for r in result[0]]

    def clear(self) -> None:
        self.driver.execute_query("MATCH (n) DETACH DELETE n")

    def node_count(self) -> int:
        result = self.driver.execute_query("MATCH (n) RETURN count(n) AS c")
        return result[0][0]["c"]

    def edge_count(self) -> int:
        result = self.driver.execute_query("MATCH ()-[r]->() RETURN count(r) AS c")
        return result[0][0]["c"]
