"""
Guard: todos los enlaces relativos del README y de docs/ tienen que apuntar a
un fichero que existe y que no esté vacío.

Este repositorio ya tuvo un docs/DOC_COMPLETA.md de 0 bytes (#2). Un enlace
roto en el README es lo primero que ve quien llega.

Uso:  python test_enlaces_docs.py
"""

import pathlib
import re

# [texto](destino) — se ignoran http(s), mailto y anclas.
ENLACE = re.compile(r"\[[^\]]*\]\((?!https?://|mailto:|#)([^)#\s]+)")

MARKDOWN = [pathlib.Path("README.md"), *sorted(pathlib.Path("docs").glob("*.md"))]


def enlaces_rotos(path):
    roto = []
    for destino in ENLACE.findall(path.read_text(encoding="utf-8")):
        objetivo = (path.parent / destino).resolve()
        if not objetivo.exists():
            roto.append(f"{path}: '{destino}' no existe")
        elif objetivo.is_file() and objetivo.stat().st_size == 0:
            roto.append(f"{path}: '{destino}' está vacío (0 bytes)")
    return roto


if __name__ == "__main__":
    # El detector tiene que detectar.
    assert ENLACE.findall("ver [guía](docs/X.md)") == ["docs/X.md"], "regex rota"
    assert not ENLACE.findall("[web](https://example.com)"), "no debe mirar URLs"

    rotos = []
    for md in MARKDOWN:
        rotos += enlaces_rotos(md)

    assert not rotos, "enlaces rotos:\n  " + "\n  ".join(rotos)
    print(f"OK: enlaces relativos correctos en {len(MARKDOWN)} ficheros markdown")
