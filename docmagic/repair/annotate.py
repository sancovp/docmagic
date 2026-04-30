"""Generate DOCMAGIC annotations for hidden connections."""
from pathlib import Path

def generate_annotations(repo_path: Path, dry_run: bool = True) -> str:
    """Scan for hidden connections and generate # DOCMAGIC: comments.
    
    Args:
        repo_path: Path to repository root
        dry_run: If True, report without modifying files
    
    Returns:
        Summary of annotations generated
    """
    from docmagic.scanner.hidden import detect_hidden_connections
    from docmagic.graph import get_backend

    graph = get_backend("networkx")
    result = detect_hidden_connections(repo_path, graph)

    annotations = []
    for category, items in result.get("details", {}).items():
        for item in items:
            file_path = repo_path / item["file"]
            line = item.get("line", 1)
            target = item.get("target", "unknown")

            comment = f"# DOCMAGIC: {category.upper()} → {target}"
            annotations.append({
                "file": str(file_path),
                "line": line,
                "comment": comment,
            })

    if dry_run:
        lines = [f"DRY RUN: {len(annotations)} annotations would be added"]
        for a in annotations[:30]:
            lines.append(f"  {a['file']}:{a['line']} — {a['comment']}")
        if len(annotations) > 30:
            lines.append(f"  ... and {len(annotations) - 30} more")
        return "\n".join(lines)

    # Apply annotations
    applied = 0
    for a in annotations:
        try:
            fp = Path(a["file"])
            if not fp.exists():
                continue
            content = fp.read_text()
            file_lines = content.split("\n")
            idx = max(0, a["line"] - 1)
            if a["comment"] not in content:  # don't double-annotate
                file_lines.insert(idx, a["comment"])
                fp.write_text("\n".join(file_lines))
                applied += 1
        except Exception:
            continue

    return f"Applied {applied}/{len(annotations)} annotations"
