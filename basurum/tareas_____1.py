from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
import json
import os

# Inicializar la consola de Rich
console = Console()

# Nombre del archivo JSON para almacenar las tareas
TASKS_FILE = "tasks.json"

# Función para cargar las tareas desde el archivo JSON
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

# Función para guardar las tareas en el archivo JSON
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Función para mostrar las tareas en una tabla
def show_tasks(tasks):
    table = Table(title="Gestor de Tareas", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Tarea", style="cyan", width=50)
    table.add_column("Estado", justify="center", style="green")

    for idx, task in enumerate(tasks, start=1):
        status = "[✓]" if task["completed"] else "[ ]"
        table.add_row(str(idx), task["description"], status)

    console.print(table)

# Función para agregar una nueva tarea
def add_task(tasks):
    description = Prompt.ask("Ingrese la descripción de la tarea")
    tasks.append({"description": description, "completed": False})
    save_tasks(tasks)
    console.print(Panel("[bold green]Tarea agregada correctamente[/bold green]"))

# Función para marcar una tarea como completada
def complete_task(tasks):
    if not tasks:
        console.print(Panel("[bold yellow]No hay tareas disponibles[/bold yellow]"))
        return

    task_id = Prompt.ask("Ingrese el ID de la tarea a completar", choices=[str(i) for i in range(1, len(tasks) + 1)])
    task_id = int(task_id) - 1
    tasks[task_id]["completed"] = True
    save_tasks(tasks)
    console.print(Panel("[bold green]Tarea marcada como completada[/bold green]"))

# Función para eliminar una tarea
def delete_task(tasks):
    if not tasks:
        console.print(Panel("[bold yellow]No hay tareas disponibles[/bold yellow]"))
        return

    task_id = Prompt.ask("Ingrese el ID de la tarea a eliminar", choices=[str(i) for i in range(1, len(tasks) + 1)])
    task_id = int(task_id) - 1
    removed_task = tasks.pop(task_id)
    save_tasks(tasks)
    console.print(Panel(f"[bold red]Tarea eliminada: {removed_task['description']}[/bold red]"))

# Función principal del programa
def main():
    tasks = load_tasks()

    while True:
        console.clear()
        console.print(Panel("[bold blue]GESTOR DE TAREAS[/bold blue]", expand=False))

        show_tasks(tasks)

        console.print("\nOpciones:")
        console.print("1. Agregar tarea")
        console.print("2. Marcar tarea como completada")
        console.print("3. Eliminar tarea")
        console.print("4. Salir")

        choice = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4"])

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            complete_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            console.print(Panel("[bold cyan]Gracias por usar el Gestor de Tareas[/bold cyan]"))
            break

# Ejecutar el programa
if __name__ == "__main__":
    main()