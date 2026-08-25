"""
Check de la tabla de tareas: el icono de estado (✅/⭕) tiene que verse en
cualquier terminal razonable, y la tabla no puede salirse del ancho.

Antes de este check, los anchos fijos de las columnas sumaban más de lo que
cabe en un terminal de 80 columnas y Rich sacrificaba la columna del icono:
no había forma de ver qué tareas estaban completadas.

Uso:  python test_tabla_tareas.py
"""

import io

from rich.console import Console

import ui

TASKS = [
    {
        "description": "Entregar informe trimestral al cliente",
        "completed": True,
        "priority": "alta",
        "deadline": "25/08/2026",
        "pomodoros_completed": 3,
    },
    {
        "description": "Actualizar dependencias",
        "completed": False,
        "priority": "baja",
        "deadline": None,
        "pomodoros_completed": 0,
    },
]


def render(width):
    buf = io.StringIO()
    original = ui.console
    ui.console = Console(file=buf, width=width, force_terminal=False, no_color=True)
    try:
        ui.show_tasks(TASKS, show_completed=True)
    finally:
        ui.console = original
    return buf.getvalue()


if __name__ == "__main__":
    # ponytail: 70 es el suelo razonable de un terminal. Por debajo, Rich
    # recorta y no merece la pena defenderlo.
    for width in (70, 80, 100, 120, 200):
        out = render(width)

        assert "✅" in out, f"falta el icono de completada a {width} columnas"
        assert "⭕" in out, f"falta el icono de pendiente a {width} columnas"

        too_wide = [line for line in out.splitlines() if len(line) > width]
        assert not too_wide, (
            f"la tabla se sale de {width} columnas:\n  " + "\n  ".join(too_wide[:3])
        )

    print("OK: icono de estado visible y tabla dentro del ancho en 70-200 columnas")
