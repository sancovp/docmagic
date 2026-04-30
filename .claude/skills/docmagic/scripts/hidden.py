#!/usr/bin/env python3
"""DocMagic hidden — detailed hidden connection breakdown."""
import sys
from docmagic.core import find_hidden
print(find_hidden(sys.argv[1] if len(sys.argv) > 1 else "."))
