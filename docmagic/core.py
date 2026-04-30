"""DocMagic core functions — called by both MCP server and CLI."""
from pathlib import Path


def scan_repo(path: str, backend: str = "networkx") -> str:
    from docmagic.scanner.hidden import detect_hidden_connections
    repo_path = Path(path)
    if not repo_path.is_dir():
        return f"ERROR: {path} is not a directory"
    result = detect_hidden_connections(repo_path)
    return (
        f"Scanned: {repo_path.name}\n"
        f"Files: {result.get('files_scanned', 0)}\n"
        f"Hidden connections: {result['total_connections']}\n"
        f"Categories: {', '.join(f'{k}:{v}' for k,v in result.get('by_type', {}).items() if v > 0)}\n"
        f"Annotated: {result.get('annotated', 0)}/{result['total_connections']} ({result.get('score', 0):.0%})"
    )


def find_hidden(path: str) -> str:
    from docmagic.scanner.hidden import detect_hidden_connections
    result = detect_hidden_connections(Path(path))
    lines = [f"Hidden connections in {path}: {result['total_connections']}"]
    for category, items in result.get("connections", {}).items():
        if items:
            lines.append(f"\n## {category} ({len(items)})")
            for item in items[:20]:
                lines.append(f"  {item['file']}:{item.get('line', '?')} -> {item.get('target', '?')}")
            if len(items) > 20:
                lines.append(f"  ... and {len(items) - 20} more")
    return "\n".join(lines)


def find_stale(path: str) -> str:
    return f"Stale surface detection not yet implemented for {path}"


def gen_annotations(path: str, dry_run: bool = True) -> str:
    from docmagic.repair.annotate import generate_annotations
    return generate_annotations(Path(path), dry_run=dry_run)


def exec_boundary(path: str, file: str, function: str = None) -> str:
    target = f"{file}:{function}" if function else file
    return f"Execution boundary tracing not yet implemented for {target}"
