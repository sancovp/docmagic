#!/usr/bin/env python3
"""DocMagic scan — full repo scan for hidden connections."""
import sys
from docmagic.core import scan_repo
print(scan_repo(sys.argv[1] if len(sys.argv) > 1 else "."))
