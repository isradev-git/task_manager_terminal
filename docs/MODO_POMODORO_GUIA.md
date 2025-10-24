from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.console import Console
from rich.style import Style
from rich.rule import Rule
from datetime import datetime

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
    "overdue": Style(color="red", bold=True, blink=True),
    "deadline_soon": Style(color="yellow", bold=True),
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
    console.print("9. Mostrar/Ocultar completadas", style=THEME["info"])
    console.print("─" * 40, style="dim")
    console.print("10. 🍅 Iniciar Pomodoro", style="bold green")
    console.print("11. 📊 Estadísticas Pomodoro", style="bold cyan")
    console.print("12. ⚙️  Configurar tiempos", style="bold yellow")
    console.print("─" * 40, style="dim")
    console.print("13. Salir", style=THEME["info"])
    return Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"])

# Función para verificar si una tarea está vencida
def is_overdue(deadline_str):
    """
    Verifica si una fecha límite ya pasó.
    Retorna True si la fecha ya pasó, False en caso contrario.
    """
    if not deadline_str:
        return False
    
    try:
        deadline = datetime.strptime(deadline_str, "%d/%m/%Y")
        today = datetime.now()
        return deadline.date() < today.date()
    except ValueError:
        return False

# Función para verificar si una tarea está próxima a vencer (3 días o menos)
def is_deadline_soon(deadline_str):
    """
    Verifica si una fecha límite está próxima (dentro de 3 días).
    Retorna True si faltan 3 días o menos, False en caso contrario.
    """
    if not deadline_str:
        return False
    
    try:
        deadline = datetime.strptime(deadline_str, "%d/%m/%Y")
        today = datetime.now()
        days_until_deadline = (deadline.date() - today.date()).days
        return 0 <= days_until_deadline <= 3
    except ValueError:
        return False

# Nueva función: Obtener texto descriptivo de los días restantes
def get_days_remaining_text(deadline_str):
    """
    Convierte los días hasta la fecha límite en un texto legible.
    
    Ejemplos de salida:
    - "Vencida hace 3 días" (si pasó hace 3 días)
    - "¡Hoy!" (si vence hoy)
    - "Mañana" (si vence mañana)
    - "En 5 días" (si faltan 5 días)
    - "" (si no hay fecha)
    
    Este texto se mostrará junto a la fecha para mayor claridad.
    """
    if not deadline_str:
        return ""
    
    try:
        deadline = datetime.strptime(deadline_str, "%d/%m/%Y")
        today = datetime.now()
        days_difference = (deadline.date() - today.date()).days
        
        # Casos especiales con texto más descriptivo
        if days_difference < 0:
            # Tarea vencida
            days_overdue = abs(days_difference)
            if days_overdue == 1:
                return "Vencida ayer"
            else:
                return f"Vencida hace {days_overdue} días"
        elif days_difference == 0:
            return "¡Hoy!"
        elif days_difference == 1:
            return "Mañana"
        elif days_difference == 2:
            return "Pasado mañana"
        else:
            # Fecha futura normal
            return f"En {days_difference} días"
    
    except ValueError:
        return ""

# Función para formatear la fecha con indicadores visuales Y días restantes
def format_deadline(deadline_str, completed):
    """
    Formatea la fecha límite con colores, iconos Y días restantes.
    
    Formato: [Icono] Fecha (Días restantes)
    Ejemplo: "⚠ 22/10/2024 (Vencida hace 1 día)"
    """
    if not deadline_str:
        return "[dim]Sin fecha[/dim]"
    
    # Obtenemos el texto de días restantes
    days_text = get_days_remaining_text(deadline_str)
    
    # Si la tarea está completada, mostramos en verde con días
    if completed:
        if days_text:
            return f"[green]{deadline_str} ({days_text})[/green]"
        return f"[green]{deadline_str}[/green]"
    
    # Si está vencida, mostramos en rojo parpadeante
    if is_overdue(deadline_str):
        return f"[red bold blink]⚠ {deadline_str} ({days_text})[/red bold blink]"
    
    # Si está próxima a vencer (3 días o menos)
    if is_deadline_soon(deadline_str):
        return f"[yellow bold]⏰ {deadline_str} ({days_text})[/yellow bold]"
    
    # Fecha normal - mostramos con días restantes
    return f"[white]{deadline_str} ({days_text})[/white]"

# Función auxiliar para obtener días hasta la fecha límite
def get_days_until_deadline(deadline_str):
    """
    Calcula cuántos días faltan hasta la fecha límite.
    Retorna un número (negativo si está vencida, infinito si no hay fecha).
    """
    if not deadline_str:
        return float('inf')
    
    try:
        deadline = datetime.strptime(deadline_str, "%d/%m/%Y")
        today = datetime.now()
        days_difference = (deadline.date() - today.date()).days
        return days_difference
    except ValueError:
        return float('inf')

# Función para ordenar tareas por prioridad y fecha límite
def sort_tasks_by_priority_and_deadline(tasks):
    """
    Ordena las tareas por prioridad primero, luego por fecha límite.
    """
    priority_order = {"alta": 1, "media": 2, "baja": 3}
    
    sorted_tasks = sorted(
        tasks,
        key=lambda task: (
            priority_order.get(task.get("priority", "baja"), 4),
            get_days_until_deadline(task.get("deadline"))
        )
    )
    
    return sorted_tasks

# Nueva función: Contar tareas urgentes
def count_urgent_tasks(tasks):
    """
    Cuenta cuántas tareas urgentes hay (vencidas o por vencer en 3 días).
    Solo cuenta las tareas NO completadas.
    
    Retorna una tupla: (tareas_vencidas, tareas_proximas, total_urgentes)
    """
    overdue_count = 0
    soon_count = 0
    
    for task in tasks:
        # Solo contamos tareas no completadas
        if not task.get("completed", False):
            deadline = task.get("deadline")
            
            if is_overdue(deadline):
                overdue_count += 1
            elif is_deadline_soon(deadline):
                soon_count += 1
    
    total_urgent = overdue_count + soon_count
    return overdue_count, soon_count, total_urgent

# Nueva función: Mostrar panel de estadísticas urgentes
def show_urgent_tasks_panel(tasks):
    """
    Muestra un panel con el contador de tareas urgentes.
    Solo se muestra si hay tareas urgentes.
    
    Ejemplo:
    ╭─────────────────────────────────────╮
    │ ⚠️  TIENES 5 TAREAS URGENTES        │
    │ • 2 tareas vencidas                 │
    │ • 3 tareas próximas a vencer        │
    ╰─────────────────────────────────────╯
    """
    overdue, soon, total = count_urgent_tasks(tasks)
    
    # Solo mostramos el panel si hay tareas urgentes
    if total > 0:
        # Construimos el mensaje
        if total == 1:
            message = "⚠️  TIENES 1 TAREA URGENTE\n"
        else:
            message = f"⚠️  TIENES {total} TAREAS URGENTES\n"
        
        # Añadimos detalles
        if overdue > 0:
            if overdue == 1:
                message += "• 1 tarea vencida\n"
            else:
                message += f"• {overdue} tareas vencidas\n"
        
        if soon > 0:
            if soon == 1:
                message += "• 1 tarea próxima a vencer"
            else:
                message += f"• {soon} tareas próximas a vencer"
        
        # Mostramos el panel en rojo si hay vencidas, amarillo si solo hay próximas
        panel_style = "bold red" if overdue > 0 else "bold yellow"
        console.print(Panel(message, style=panel_style, expand=False))
        console.print()  # Espacio después del panel

# Mostrar las tareas en una tabla con separadores visuales
def show_tasks(tasks, sort_by=None, show_completed=False):
    """
    Muestra las tareas en una tabla con formato rico.
    
    CARACTERÍSTICAS:
    1. Muestra días restantes junto a cada fecha
    2. Añade separadores visuales entre diferentes prioridades
    3. Muestra panel de contador de tareas urgentes al inicio
    4. NUEVO: Indica si las tareas completadas están ocultas
    
    Parámetros:
    - tasks: lista de tareas a mostrar
    - sort_by: mantenido por compatibilidad (ya no se usa)
    - show_completed: True si se están mostrando completadas, False si están ocultas
    """
    # Primero mostramos el panel de tareas urgentes (si las hay)
    show_urgent_tasks_panel(tasks)
    
    # Ordenamos las tareas por prioridad y fecha límite
    sorted_tasks = sort_tasks_by_priority_and_deadline(tasks)
    
    # Si no hay tareas, mostramos un mensaje
    if not sorted_tasks:
        console.print("[dim]No hay tareas para mostrar[/dim]")
        return
    
    # Diccionario para asignar colores a las prioridades
    priority_styles = {
        "alta": THEME["priority_high"],
        "media": THEME["priority_medium"],
        "baja": THEME["priority_low"]
    }
    
    # Variable para rastrear la prioridad anterior (para separadores)
    previous_priority = None
    
    # Creamos la tabla inicial
    table = Table(title="Gestor de Tareas", show_header=True, header_style=THEME["title"])
    table.add_column("ID", style="dim", width=6)
    table.add_column("Tarea", style="cyan", width=25)
    table.add_column("Estado", justify="center", style="green", width=8)
    table.add_column("Prioridad", justify="center", style="yellow", width=10)
    table.add_column("Fecha Límite", justify="left", style="white", width=30)
    table.add_column("🍅", justify="center", style="green", width=5)  # Nueva columna de pomodoros
    
    # Iteramos sobre las tareas ordenadas
    for idx, task in enumerate(sorted_tasks, start=1):
        current_priority = task.get("priority", "baja")
        
        # SEPARADOR VISUAL: Si cambió la prioridad, añadimos una línea separadora
        if previous_priority is not None and previous_priority != current_priority:
            # Añadimos una fila vacía como separador
            table.add_row("", "", "", "", "", end_section=True)
        
        # Actualizamos la prioridad anterior
        previous_priority = current_priority
        
        # Preparamos los datos de la fila
        status = "[✓]" if task["completed"] else "[ ]"
        priority = task.get("priority", "baja")
        deadline = task.get("deadline")
        
        # Formateamos la fecha con días restantes
        formatted_deadline = format_deadline(deadline, task["completed"])
        
        # Obtener número de pomodoros completados
        pomodoros = task.get("pomodoros_completed", 0)
        pomodoros_text = str(pomodoros) if pomodoros > 0 else "[dim]-[/dim]"
        
        # Estilo de la fila según prioridad
        row_style = priority_styles.get(priority, "white")
        
        # Si la tarea está vencida y no completada, usamos estilo de advertencia
        if is_overdue(deadline) and not task["completed"]:
            row_style = THEME["overdue"]
        
        # Añadimos la fila a la tabla (ahora con pomodoros)
        table.add_row(
            str(idx),
            task["description"],
            status,
            priority,
            formatted_deadline,
            pomodoros_text,  # Nueva columna
            style=row_style
        )
    
    # Mostramos la tabla
    console.print(table)
    
    # Leyenda actualizada
    console.print("\n[dim]Leyenda:[/dim]")
    console.print("[dim]⚠ = Tarea vencida | ⏰ = Vence pronto (3 días o menos)[/dim]")
    console.print("[dim]Las líneas separan diferentes niveles de prioridad[/dim]")
    
    # NUEVO: Indicador de estado de tareas completadas
    if not show_completed:
        # Contamos cuántas completadas hay en total
        completed_count = len([t for t in tasks if t.get("completed", False)])
        if completed_count > 0:
            console.print(f"\n[dim]💡 Hay {completed_count} tarea(s) completada(s) oculta(s). Usa la opción 9 para verlas.[/dim]")
    else:
        console.print("\n[dim]✅ Mostrando tareas completadas[/dim]")