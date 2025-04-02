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
    console.print("5. Editar tarea")
    console.print("6. Buscar tareas")
    console.print("7. Exportar tareas a CSV")
    console.print("8. Importar tareas desde CSV")
    console.print("9. Salir")
    return Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])

# Mostrar las tareas en una tabla (con soporte para ordenamiento por prioridad)
def show_tasks(tasks, sort_by=None):
    table = Table(title="Gestor de Tareas", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Tarea", style="cyan", width=50)
    table.add_column("Estado", justify="center", style="green")
    table.add_column("Prioridad", justify="center", style="yellow")

    # Diccionario para asignar colores y valores numéricos a las prioridades
    priority_colors = {"alta": "red", "media": "blue", "baja": "green"}
    priority_order = {"alta": 1, "media": 2, "baja": 3}  # Menor número = mayor prioridad

    # Ordenar las tareas si se especifica un criterio
    if sort_by == "priority":
        tasks = sorted(tasks, key=lambda x: priority_order.get(x.get("priority", "baja"), 4))
    # Si no se especifica sort_by o es None, mostramos las tareas sin ordenar

    # Iterar sobre las tareas y agregarlas a la tabla
    for idx, task in enumerate(tasks, start=1):
        status = "[✓]" if task["completed"] else "[ ]"
        row_style = priority_colors.get(task.get("priority", "N/A"), "white")
        table.add_row(str(idx), task["description"], status, task.get("priority", "N/A"), style=row_style)

    console.print(table)