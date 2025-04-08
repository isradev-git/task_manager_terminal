from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.console import Console
from rich.style import Style

console = Console()

# Definir un tema de colores
THEME = {
    "title": Style(color="cyan", bold=True),
    "success": Style(color="green", bold=True),
    "error": Style(color="red", bold=True),
    "warning": Style(color="yellow", bold=True),
    "info": Style(color="blue", bold=True),
    "priority_high": Style(color="red", bold=True),
    "priority_medium": Style(color="yellow", bold=True),
    "priority_low": Style(color="green", bold=True),
}

# Mostrar el panel de bienvenida
def show_welcome_panel():
    console.clear()
    console.print(Panel("[bold cyan]GESTOR DE TAREAS[/bold cyan]", style=THEME["title"], expand=False))

# Mostrar el menú principal
def show_menu():
    console.print("\nOpciones:", style=THEME["info"])
    console.print("1. Agregar tarea", style=THEME["info"])
    console.print("2. Marcar tarea como completada", style=THEME["info"])
    console.print("3. Eliminar tarea", style=THEME["info"])
    console.print("4. Filtrar tareas", style=THEME["info"])
    console.print("5. Editar tarea", style=THEME["info"])
    console.print("6. Buscar tareas", style=THEME["info"])
    console.print("7. Exportar tareas a CSV", style=THEME["info"])
    console.print("8. Importar tareas desde CSV", style=THEME["info"])
    console.print("9. Salir", style=THEME["info"])
    return Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])

# Mostrar las tareas en una tabla (con soporte para ordenamiento por prioridad)
def show_tasks(tasks, sort_by=None):
    table = Table(title="Gestor de Tareas", show_header=True, header_style=THEME["title"])
    table.add_column("ID", style="dim", width=6)
    table.add_column("Tarea", style="cyan", width=50)
    table.add_column("Estado", justify="center", style="green")
    table.add_column("Prioridad", justify="center", style="yellow")

    # Diccionario para asignar colores y valores numéricos a las prioridades
    priority_styles = {
        "alta": THEME["priority_high"],
        "media": THEME["priority_medium"],
        "baja": THEME["priority_low"]
    }
    priority_order = {"alta": 1, "media": 2, "baja": 3}  # Menor número = mayor prioridad

    # Ordenar las tareas si se especifica un criterio
    if sort_by == "priority":
        tasks = sorted(tasks, key=lambda x: priority_order.get(x.get("priority", "baja"), 4))

    # Iterar sobre las tareas y agregarlas a la tabla
    for idx, task in enumerate(tasks, start=1):
        status = "[✓]" if task["completed"] else "[ ]"
        priority = task.get("priority", "baja")
        row_style = priority_styles.get(priority, "white")
        table.add_row(str(idx), task["description"], status, priority, style=row_style)

    console.print(table)