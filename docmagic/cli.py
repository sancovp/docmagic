"""DocMagic CLI — scan, detect, repair."""
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        prog="docmagic",
        description="Repo-level causality scanner for AI-coded systems"
    )
    sub = parser.add_subparsers(dest="command")

    scan = sub.add_parser("scan", help="Scan a repository")
    scan.add_argument("path", help="Path to repository")
    scan.add_argument("--backend", default="networkx", choices=["networkx", "neo4j"])

    hidden = sub.add_parser("hidden", help="Find hidden connections")
    hidden.add_argument("path", help="Path to repository")

    annotate = sub.add_parser("annotate", help="Generate DOCMAGIC annotations")
    annotate.add_argument("path", help="Path to repository")
    annotate.add_argument("--apply", action="store_true", help="Apply changes (default: dry run)")

    serve = sub.add_parser("serve", help="Start MCP server")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "serve":
        from docmagic.server import mcp
        mcp.run()
    elif args.command == "scan":
        from docmagic.server import scan_repo
        print(scan_repo(args.path, args.backend))
    elif args.command == "hidden":
        from docmagic.server import find_hidden_connections
        print(find_hidden_connections(args.path))
    elif args.command == "annotate":
        from docmagic.repair.annotate import generate_annotations
        from pathlib import Path
        print(generate_annotations(Path(args.path), dry_run=not args.apply))

if __name__ == "__main__":
    main()
