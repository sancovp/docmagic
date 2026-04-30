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
        from docmagic.core import scan_repo
        print(scan_repo(args.path, args.backend))
    elif args.command == "hidden":
        from docmagic.core import find_hidden
        print(find_hidden(args.path))
    elif args.command == "annotate":
        from docmagic.core import gen_annotations
        print(gen_annotations(args.path, dry_run=not args.apply))

if __name__ == "__main__":
    main()
