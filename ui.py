from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.console import Console

console = Console()

# Mostrar el panel de bienvenida
def show_welcome_panel():
    console.clear()
    console.print(Panel("[bold blue]GESTOR DE TAREAS[/bold blue]", expand=False))

# Mostrar el menú principal
def show_menu():
    console.print("\nOpciones:")
    console.print("1. Agregar tarea")
    console.print("2. Marcar tarea como completada")
    console.print("3. Eliminar tarea")
    console.print("4. Filtrar tareas")
    console.print("5. Buscar tareas")
    console.print("6. Exportar tareas a CSV")
    console.print("7. Importar tareas desde CSV")
    console.print("8. Salir")
    return Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "6", "7", "8"])

# Mostrar las tareas en una tabla
def show_tasks(tasks):
    table = Table(title="Gestor de Tareas", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Tarea", style="cyan", width=50)
    table.add_column("Estado", justify="center", style="green")
    table.add_column("Prioridad", justify="center", style="yellow")

    for idx, task in enumerate(tasks, start=1):
        status = "[✓]" if task["completed"] else "[ ]"
        table.add_row(str(idx), task["description"], status, task.get("priority", "N/A"))

    console.print(table)