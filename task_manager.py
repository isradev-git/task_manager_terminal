import json
import os
from rich.prompt import Prompt
from rich.console import Console
from ui import show_tasks, show_welcome_panel  # Añadimos show_welcome_panel aquí

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

    # Limpiar la pantalla para que la selección sea más clara
    console.clear()
    show_welcome_panel()
    
    # Ordenar las tareas por prioridad para que coincidan con la visualización
    priority_order = {"alta": 1, "media": 2, "baja": 3}  # Menor número = mayor prioridad
    sorted_tasks = sorted(tasks, key=lambda x: priority_order.get(x.get("priority", "baja"), 4))

    # Mostrar las tareas ordenadas solo para selección
    console.print("\n[bold cyan]Seleccione una tarea para completar:[/bold cyan]")
    show_tasks(sorted_tasks, sort_by="priority")

    # Pedir el ID de la tarea a completar (basado en la lista ordenada)
    task_id = int(Prompt.ask("Ingrese el ID de la tarea a completar", choices=[str(i) for i in range(1, len(sorted_tasks) + 1)])) - 1

    # Encontrar el índice de la tarea en la lista original
    task_to_complete = sorted_tasks[task_id]
    original_index = tasks.index(task_to_complete)

    # Marcar la tarea como completada en la lista original
    tasks[original_index]["completed"] = True
    
    # Limpiar la pantalla y mostrar solo el mensaje de éxito
    console.clear()
    show_welcome_panel()
    console.print("[bold green]Tarea marcada como completada[/bold green]")

# Eliminar una tarea
def delete_task(tasks):
    if not tasks:
        console.print("[bold yellow]No hay tareas disponibles[/bold yellow]")
        return

    # Limpiar la pantalla para que la selección sea más clara
    console.clear()
    show_welcome_panel()
    
    # Ordenar las tareas por prioridad para que coincidan con la visualización
    priority_order = {"alta": 1, "media": 2, "baja": 3}  # Menor número = mayor prioridad
    sorted_tasks = sorted(tasks, key=lambda x: priority_order.get(x.get("priority", "baja"), 4))

    # Mostrar las tareas ordenadas solo para selección
    console.print("\n[bold cyan]Seleccione una tarea para eliminar:[/bold cyan]")
    show_tasks(sorted_tasks, sort_by="priority")

    # Pedir el ID de la tarea a eliminar (basado en la lista ordenada)
    task_id = int(Prompt.ask("Ingrese el ID de la tarea a eliminar", choices=[str(i) for i in range(1, len(sorted_tasks) + 1)])) - 1

    # Encontrar el índice de la tarea en la lista original
    task_to_remove = sorted_tasks[task_id]
    original_index = tasks.index(task_to_remove)

    # Eliminar la tarea de la lista original
    removed_task = tasks.pop(original_index)
    
    # Limpiar la pantalla y mostrar solo el mensaje de éxito
    console.clear()
    show_welcome_panel()
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

    # Ordenar las tareas por prioridad para que coincidan con la visualización
    priority_order = {"alta": 1, "media": 2, "baja": 3}  # Menor número = mayor prioridad
    sorted_tasks = sorted(tasks, key=lambda x: priority_order.get(x.get("priority", "baja"), 4))

    # Mostrar las tareas ordenadas
    show_tasks(sorted_tasks, sort_by="priority")
    
    # Pedir el ID de la tarea a editar (basado en la lista ordenada)
    task_id = int(Prompt.ask("Ingrese el ID de la tarea a editar", choices=[str(i) for i in range(1, len(sorted_tasks) + 1)])) - 1
    
    # Encontrar el índice de la tarea en la lista original
    task_to_edit = sorted_tasks[task_id]
    original_index = tasks.index(task_to_edit)

    # Mostrar las opciones de edición
    console.print("\n¿Qué desea editar?")
    console.print("1. Descripción")
    console.print("2. Prioridad")
    console.print("3. Estado (completada/pendiente)")
    edit_choice = Prompt.ask("Seleccione una opción", choices=["1", "2", "3"])
    
    # Editar el campo seleccionado
    if edit_choice == "1":
        new_description = Prompt.ask("Ingrese la nueva descripción", default=tasks[original_index]["description"])
        tasks[original_index]["description"] = new_description
        console.print("[bold green]Descripción actualizada correctamente[/bold green]")
    elif edit_choice == "2":
        new_priority = Prompt.ask("Ingrese la nueva prioridad (alta, media, baja)", choices=["alta", "media", "baja"], default=tasks[original_index]["priority"])
        tasks[original_index]["priority"] = new_priority
        console.print("[bold green]Prioridad actualizada correctamente[/bold green]")
    elif edit_choice == "3":
        new_status = Prompt.ask("¿Marcar como completada? (s/n)", choices=["s", "n"], default="n")
        tasks[original_index]["completed"] = (new_status == "s")
        console.print("[bold green]Estado actualizado correctamente[/bold green]")