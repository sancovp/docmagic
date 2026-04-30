"""DocMagic MCP server — exposes scanning and repair tools to Claude."""
from fastmcp import FastMCP
from docmagic.core import scan_repo, find_hidden, find_stale, gen_annotations, exec_boundary

mcp = FastMCP("docmagic", instructions="Repo-level causality scanner for AI-coded systems")

@mcp.tool()
def docmagic_scan(path: str, backend: str = "networkx") -> str:
    """Scan a repository: parse AST, build call graph, detect hidden connections."""
    return scan_repo(path, backend)

@mcp.tool()
def docmagic_hidden(path: str) -> str:
    """Find invisible coupling: HTTP calls, file triggers, hook bridges, MCP refs, cross-imports, state files, multi-write drift."""
    return find_hidden(path)

@mcp.tool()
def docmagic_stale(path: str) -> str:
    """Find stale explanatory surfaces: docstrings and comments that lie about code behavior."""
    return find_stale(path)

@mcp.tool()
def docmagic_annotate(path: str, dry_run: bool = True) -> str:
    """Generate # DOCMAGIC: annotations for hidden connections."""
    return gen_annotations(path, dry_run)

@mcp.tool()
def docmagic_boundary(path: str, file: str, function: str = None) -> str:
    """Trace complete execution boundary for a file or function."""
    return exec_boundary(path, file, function)

if __name__ == "__main__":
    mcp.run()
