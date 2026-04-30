"""NetworkX graph backend — default, zero infrastructure needed."""
import networkx as nx
from docmagic.graph.base import GraphBackend

class NetworkXBackend(GraphBackend):
    def __init__(self):
        self.g = nx.DiGraph()

    def add_node(self, name: str, label: str, **props) -> None:
        self.g.add_node(name, label=label, **props)

    def add_edge(self, source: str, target: str, rel_type: str, **props) -> None:
        self.g.add_edge(source, target, rel_type=rel_type, **props)

    def get_node(self, name: str) -> dict | None:
        if name in self.g:
            return {"name": name, **self.g.nodes[name]}
        return None

    def get_edges(self, source: str = None, target: str = None, rel_type: str = None) -> list[dict]:
        edges = []
        for s, t, data in self.g.edges(data=True):
            if source and s != source:
                continue
            if target and t != target:
                continue
            if rel_type and data.get("rel_type") != rel_type:
                continue
            edges.append({"source": s, "target": t, **data})
        return edges

    def query(self, pattern: str, **params) -> list[dict]:
        """Simple pattern queries: 'callers_of:<name>', 'callees_of:<name>', 'hidden:<name>'."""
        if pattern.startswith("callers_of:"):
            name = pattern.split(":", 1)[1]
            return [{"source": s, "target": t, **d} for s, t, d in self.g.in_edges(name, data=True)]
        elif pattern.startswith("callees_of:"):
            name = pattern.split(":", 1)[1]
            return [{"source": s, "target": t, **d} for s, t, d in self.g.out_edges(name, data=True)]
        elif pattern.startswith("hidden:"):
            name = pattern.split(":", 1)[1]
            return [{"source": s, "target": t, **d}
                    for s, t, d in self.g.edges(data=True)
                    if d.get("rel_type") == "HIDDEN_CONNECTION" and (s == name or t == name)]
        return []

    def clear(self) -> None:
        self.g.clear()

    def node_count(self) -> int:
        return self.g.number_of_nodes()

    def edge_count(self) -> int:
        return self.g.number_of_edges()
