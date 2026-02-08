from pathlib import Path
import sys

# Project root = directory containing this file
ROOT = Path(__file__).resolve().parent

# Make root importable everywhere
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
