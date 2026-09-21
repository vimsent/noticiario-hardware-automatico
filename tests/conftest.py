import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
for ruta in (RAIZ, RAIZ / "scripts"):
    if str(ruta) not in sys.path:
        sys.path.insert(0, str(ruta))
