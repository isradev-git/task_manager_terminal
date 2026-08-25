"""
Guard: ningún módulo puede usar `except:` desnudo.

Un `except:` atrapa también KeyboardInterrupt y SystemExit, así que se come
el Ctrl+C del usuario y esconde errores reales detrás de un `pass`. Se usa
AST y no grep porque los comentarios mencionan la cadena "except:".

Uso:  python test_no_bare_except.py
"""

import ast
import pathlib

MODULES = sorted(pathlib.Path(".").glob("*.py"))


def bare_handlers(path):
    """Devuelve las lineas con `except:` sin tipo de excepcion."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.ExceptHandler) and node.type is None
    ]


if __name__ == "__main__":
    # El detector tiene que detectar.
    assert bare_handlers.__doc__, "sin docstring"
    probe = ast.parse("try:\n    pass\nexcept:\n    pass\n")
    assert any(
        isinstance(n, ast.ExceptHandler) and n.type is None for n in ast.walk(probe)
    ), "el detector no reconoce un except desnudo"
    probe_ok = ast.parse("try:\n    pass\nexcept ValueError:\n    pass\n")
    assert not any(
        isinstance(n, ast.ExceptHandler) and n.type is None for n in ast.walk(probe_ok)
    ), "falso positivo sobre un except con tipo"

    offenders = []
    for module in MODULES:
        offenders += [f"{module}:{line}" for line in bare_handlers(module)]

    assert not offenders, "except: desnudo en:\n  " + "\n  ".join(offenders)
    print(f"OK: sin except: desnudo en {len(MODULES)} módulos")
