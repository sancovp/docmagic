"""DocMagic MCP server — exposes scanning and repair tools to Claude."""
from fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("docmagic", description="Repo-level causality scanner for AI-coded systems")

@mcp.tool()
def scan_repo(path: str, backend: str = "networkx") -> str:
    """Scan a repository: parse AST, build call graph, detect hidden connections.
    
    Args:
        path: Absolute path to the repository root
        backend: Graph backend — 'networkx' (default, in-memory) or 'neo4j'
    
    Returns:
        Scan summary with node/edge counts and hidden connection categories
    """
    from docmagic.scanner.ast_parser import parse_directory
    from docmagic.scanner.hidden import detect_hidden_connections
    from docmagic.graph import get_backend

    repo_path = Path(path)
    if not repo_path.is_dir():
        return f"ERROR: {path} is not a directory"

    graph = get_backend(backend)
    stats = parse_directory(repo_path, graph)
    hidden = detect_hidden_connections(repo_path, graph)

    return (
        f"Scanned: {repo_path.name}\n"
        f"Nodes: {graph.node_count()} | Edges: {graph.edge_count()}\n"
        f"Hidden connections: {hidden['total']}\n"
        f"Categories: {', '.join(f'{k}:{v}' for k,v in hidden['by_category'].items() if v > 0)}\n"
        f"Annotation score: {hidden.get('annotation_score', 0):.0%}"
    )

@mcp.tool()
def find_hidden_connections(path: str) -> str:
    """Find invisible coupling in a repo: HTTP calls, file triggers, hook bridges,
    MCP refs, cross-imports, state files, multi-write drift.
    
    Args:
        path: Absolute path to the repository root
    
    Returns:
        Categorized list of hidden connections with file locations
    """
    from docmagic.scanner.hidden import detect_hidden_connections
    from docmagic.graph import get_backend

    graph = get_backend("networkx")
    result = detect_hidden_connections(Path(path), graph)

    lines = [f"Hidden connections in {path}: {result['total']}"]
    for category, items in result.get("details", {}).items():
        if items:
            lines.append(f"\n## {category} ({len(items)})")
            for item in items[:20]:  # cap per category
                lines.append(f"  {item['file']}:{item.get('line', '?')} → {item.get('target', '?')}")
            if len(items) > 20:
                lines.append(f"  ... and {len(items) - 20} more")
    return "\n".join(lines)

@mcp.tool()
def find_stale_surfaces(path: str) -> str:
    """Find stale explanatory surfaces: docstrings, comments, and docs that
    describe behavior the code no longer performs.
    
    Args:
        path: Absolute path to the repository root
    
    Returns:
        List of stale surfaces with what they claim vs what the code does
    """
    # TODO: implement stale surface detection
    return f"Stale surface detection not yet implemented for {path}"

@mcp.tool()
def generate_annotations(path: str, dry_run: bool = True) -> str:
    """Generate DOCMAGIC annotations for hidden connections.
    Adds # DOCMAGIC: HIDDEN-CALL comments to source files.
    
    Args:
        path: Absolute path to the repository root
        dry_run: If True, show what would be added without modifying files
    
    Returns:
        List of annotations that would be (or were) added
    """
    from docmagic.repair.annotate import generate_annotations as _gen
    return _gen(Path(path), dry_run=dry_run)

@mcp.tool()
def get_execution_boundary(path: str, file: str, function: str = None) -> str:
    """Trace the complete execution boundary for a file or function.
    Shows all callers, callees, hidden connections, and side effects.
    
    Args:
        path: Absolute path to the repository root
        file: Relative path to the file within the repo
        function: Optional function name to trace (traces whole file if omitted)
    
    Returns:
        Complete execution boundary map
    """
    # TODO: implement execution boundary tracing
    target = f"{file}:{function}" if function else file
    return f"Execution boundary tracing not yet implemented for {target}"

if __name__ == "__main__":
    mcp.run()
