import json
import os
from rich.prompt import Prompt
from rich.console import Console

console = Console()

TASKS_FILE = "tasks.json"

# Cargar tareas desde el archivo JSON
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

# Guardar tareas en el archivo JSON
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Agregar una nueva tarea
def add_task(tasks):
    description = Prompt.ask("Ingrese la descripción de la tarea")
    priority = Prompt.ask("Ingrese la prioridad (alta, media, baja)", choices=["alta", "media", "baja"])
    tasks.append({"description": description, "completed": False, "priority": priority})
    console.print("[bold green]Tarea agregada correctamente[/bold green]")

# Marcar una tarea como completada
def complete_task(tasks):
    if not tasks:
        console.print("[bold yellow]No hay tareas disponibles[/bold yellow]")
        return

    task_id = int(Prompt.ask("Ingrese el ID de la tarea a completar", choices=[str(i) for i in range(1, len(tasks) + 1)])) - 1
    tasks[task_id]["completed"] = True
    console.print("[bold green]Tarea marcada como completada[/bold green]")

# Eliminar una tarea
def delete_task(tasks):
    if not tasks:
        console.print("[bold yellow]No hay tareas disponibles[/bold yellow]")
        return

    task_id = int(Prompt.ask("Ingrese el ID de la tarea a eliminar", choices=[str(i) for i in range(1, len(tasks) + 1)])) - 1
    removed_task = tasks.pop(task_id)
    console.print(f"[bold red]Tarea eliminada: {removed_task['description']}[/bold red]")

# Filtrar tareas por estado
def filter_tasks(tasks, status=None):
    if status == "completed":
        return [task for task in tasks if task["completed"]]
    elif status == "pending":
        return [task for task in tasks if not task["completed"]]
    return tasks

# Buscar tareas por palabra clave
def search_tasks(tasks):
    query = Prompt.ask("Ingrese una palabra clave para buscar")
    results = [task for task in tasks if query.lower() in task["description"].lower()]
    if results:
        show_tasks(results)
    else:
        console.print("[bold yellow]No se encontraron tareas[/bold yellow]")

# Exportar tareas a CSV
def export_tasks_to_csv(tasks):
    import csv
    with open("tasks.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Descripción", "Estado", "Prioridad"])
        for idx, task in enumerate(tasks, start=1):
            writer.writerow([idx, task["description"], task["completed"], task.get("priority", "N/A")])
    console.print("[bold green]Tareas exportadas a tasks.csv[/bold green]")

# Importar tareas desde CSV
def import_tasks_from_csv(tasks):
    import csv
    if not os.path.exists("tasks.csv"):
        console.print("[bold red]El archivo tasks.csv no existe[/bold red]")
        return

    with open("tasks.csv", "r") as file:
        reader = csv.DictReader(file)
        imported_tasks = [{"description": row["Descripción"], "completed": row["Estado"] == "True", "priority": row["Prioridad"]} for row in reader]
    tasks.extend(imported_tasks)
    console.print("[bold green]Tareas importadas desde tasks.csv[/bold green]")