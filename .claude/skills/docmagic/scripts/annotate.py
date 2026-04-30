#!/usr/bin/env python3
"""DocMagic annotate — generate # DOCMAGIC: breadcrumbs."""
import sys
dry_run = "--apply" not in sys.argv
path = next((a for a in sys.argv[1:] if not a.startswith("--")), ".")
from docmagic.core import gen_annotations
print(gen_annotations(path, dry_run=dry_run))
