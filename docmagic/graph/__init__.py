"""DocMagic graph backends — networkx (default) or Neo4j (optional)."""
from docmagic.graph.base import GraphBackend
from docmagic.graph.networkx_backend import NetworkXBackend

def get_backend(backend: str = "networkx", **kwargs) -> GraphBackend:
    if backend == "networkx":
        return NetworkXBackend()
    elif backend == "neo4j":
        from docmagic.graph.neo4j_backend import Neo4jBackend
        return Neo4jBackend(**kwargs)
    raise ValueError(f"Unknown backend: {backend}. Use 'networkx' or 'neo4j'.")
