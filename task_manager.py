import json
import os
from rich.prompt import Prompt
from rich.console import Console
from ui import show_tasks

console = Console()

TASKS_FILE = "tasks.json"

# Cargar tareas desde el archivo JSON
def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            console.print("[bold red]Error: El archivo tasks.json tiene un formato inválido.[/bold red]")
            return []
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
        return [task for task in tasks if task.get("completed", False)]
    elif status == "pending":
        return [task for task in tasks if not task.get("completed", False)]
    return tasks

# Buscar tareas por palabra clave
def search_tasks(tasks):
    query = Prompt.ask("Ingrese una palabra clave para buscar")
    results = [task for task in tasks if query.lower() in task["description"].lower()]
    if results:
        show_tasks(results)
        console.print("\n[bold cyan]Presione Enter para continuar...[/bold cyan]")
        Prompt.ask("")  # Pausa para que el usuario pueda ver los resultados
    else:
        console.print("[bold yellow]No se encontraron tareas[/bold yellow]")
        console.print("\n[bold cyan]Presione Enter para continuar...[/bold cyan]")
        Prompt.ask("")  # Pausa incluso si no hay resultados

# Exportar tareas a CSV
def export_tasks_to_csv(tasks):
    if not tasks:
        console.print("[bold yellow]No hay tareas para exportar.[/bold yellow]")
        return  # Salimos de la función si no hay tareas

    try:
        import csv
        with open("tasks.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Descripción", "Estado", "Prioridad"])
            for idx, task in enumerate(tasks, start=1):
                writer.writerow([idx, task["description"], task["completed"], task.get("priority", "N/A")])
        console.print("[bold green]Tareas exportadas a tasks.csv[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error al exportar tareas: {str(e)}[/bold red]")

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

# Editar una tarea existente
def edit_task(tasks):
    if not tasks:
        console.print("[bold yellow]No hay tareas disponibles para editar[/bold yellow]")
        return

    # Mostrar las tareas para que el usuario elija cuál editar
    show_tasks(tasks, sort_by="priority")
    
    # Pedir el ID de la tarea a editar
    task_id = int(Prompt.ask("Ingrese el ID de la tarea a editar", choices=[str(i) for i in range(1, len(tasks) + 1)])) - 1
    
    # Mostrar las opciones de edición
    console.print("\n¿Qué desea editar?")
    console.print("1. Descripción")
    console.print("2. Prioridad")
    console.print("3. Estado (completada/pendiente)")
    edit_choice = Prompt.ask("Seleccione una opción", choices=["1", "2", "3"])
    
    # Editar el campo seleccionado
    if edit_choice == "1":
        new_description = Prompt.ask("Ingrese la nueva descripción", default=tasks[task_id]["description"])
        tasks[task_id]["description"] = new_description
        console.print("[bold green]Descripción actualizada correctamente[/bold green]")
    elif edit_choice == "2":
        new_priority = Prompt.ask("Ingrese la nueva prioridad (alta, media, baja)", choices=["alta", "media", "baja"], default=tasks[task_id]["priority"])
        tasks[task_id]["priority"] = new_priority
        console.print("[bold green]Prioridad actualizada correctamente[/bold green]")
    elif edit_choice == "3":
        new_status = Prompt.ask("¿Marcar como completada? (s/n)", choices=["s", "n"], default="n")
        tasks[task_id]["completed"] = (new_status == "s")
        console.print("[bold green]Estado actualizado correctamente[/bold green]")