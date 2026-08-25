"""
Check de import/export CSV.

El tasks.csv que venía en el repositorio estaba en latin-1 mientras el código
lo leía como UTF-8: importarlo reventaba con UnicodeDecodeError y no se
importaba ni una tarea. Además no se validaba nada de lo que venía dentro.

Uso:  python test_csv.py
"""

import csv
import os
import tempfile

import task_manager


def _en_directorio_temporal(fn):
    """Ejecuta fn() en un directorio vacío: tasks.csv es una ruta relativa."""
    anterior = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            return fn()
        finally:
            os.chdir(anterior)


def escribir_csv(filas, encoding="utf-8"):
    with open("tasks.csv", "w", newline="", encoding=encoding) as f:
        csv.writer(f).writerows(filas)


CABECERA = ["ID", "Descripción", "Estado", "Prioridad", "Fecha Límite"]


def test_ida_y_vuelta():
    originales = [
        {"description": "Tarea con acento: ñ á é", "completed": True,
         "priority": "alta", "deadline": "31/12/2026"},
        {"description": "Tarea sin fecha", "completed": False,
         "priority": "baja", "deadline": None},
    ]
    task_manager.export_tasks_to_csv(originales)
    importadas = []
    task_manager.import_tasks_from_csv(importadas)

    assert len(importadas) == 2, f"esperaba 2 tareas, llegaron {len(importadas)}"
    assert importadas[0]["description"] == "Tarea con acento: ñ á é"
    assert importadas[0]["completed"] is True
    assert importadas[0]["deadline"] == "31/12/2026"
    assert importadas[1]["deadline"] is None, "«Sin fecha» debe volver como None"


def test_bom_de_excel():
    escribir_csv(
        [CABECERA, [1, "Guardado desde Excel", "False", "media", "Sin fecha"]],
        encoding="utf-8-sig",
    )
    importadas = []
    task_manager.import_tasks_from_csv(importadas)
    assert len(importadas) == 1, "el BOM de Excel rompe la primera columna"


def test_datos_invalidos_no_revientan():
    escribir_csv([
        CABECERA,
        [1, "Prioridad inventada", "False", "urgentísima", "Sin fecha"],
        [2, "Fecha imposible", "False", "alta", "31/02/2026"],
        [3, "", "False", "alta", "Sin fecha"],
    ])
    importadas = []
    task_manager.import_tasks_from_csv(importadas)

    assert len(importadas) == 2, "la fila sin descripción debía omitirse"
    assert importadas[0]["priority"] == "media", "prioridad inválida → 'media'"
    assert importadas[1]["deadline"] is None, "fecha inválida → sin fecha"


def test_faltan_columnas():
    escribir_csv([["Cosa", "Otra"], ["a", "b"]])
    importadas = []
    task_manager.import_tasks_from_csv(importadas)
    assert importadas == [], "sin las columnas obligatorias no debe importar nada"


if __name__ == "__main__":
    for test in (test_ida_y_vuelta, test_bom_de_excel,
                 test_datos_invalidos_no_revientan, test_faltan_columnas):
        _en_directorio_temporal(test)
    print("OK: import/export CSV (ida y vuelta, BOM, datos inválidos, columnas)")
