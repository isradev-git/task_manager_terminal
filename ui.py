from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.console import Console
from rich.style import Style
from rich.rule import Rule
from rich.columns import Columns
from rich.text import Text
from rich.layout import Layout
from rich.progress import Progress, BarColumn, TextColumn
from rich.align import Align
from datetime import datetime
import time

console = Console()

# Tema de colores moderno con gradientes
THEME = {
    "title": Style(color="bright_cyan", bold=True),
    "success": Style(color="bright_green", bold=True),
    "error": Style(color="bright_red", bold=True),
    "warning": Style(color="bright_yellow", bold=True),
    "info": Style(color="bright_blue", bold=True),
    "priority_high": Style(color="red", bold=True),
    "priority_medium": Style(color="yellow", bold=True),
    "priority_low": Style(color="green", bold=True),
    "overdue": Style(color="red", bold=True),
    "deadline_soon": Style(color="yellow", bold=True),
    "accent": Style(color="magenta", bold=True),
    "gradient_1": Style(color="cyan"),
    "gradient_2": Style(color="blue"),
    "gradient_3": Style(color="magenta"),
}

def create_gradient_text(text, colors=["cyan", "blue", "magenta"]):
    """
    Crea texto con efecto de gradiente usando Rich.
    """
    result = Text()
    length = len(text)
    
    for i, char in enumerate(text):
        # Calcular el color basado en la posición
        color_index = int((i / length) * (len(colors) - 1))
        color_index = min(color_index, len(colors) - 1)
        result.append(char, style=colors[color_index])
    
    return result


def show_welcome_panel():
    """
    Panel de bienvenida moderno con animación y diseño atractivo.
    """
    console.clear()
    
    # Arte ASCII del logo
    logo = """
    ╔════════════════════════════════════════════════╗
    ║                                                ║
    ║   ████████╗ █████╗ ███████╗██╗  ██╗███████╗   ║
    ║   ╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝██╔════╝   ║
    ║      ██║   ███████║███████╗█████╔╝ ███████╗   ║
    ║      ██║   ██╔══██║╚════██║██╔═██╗ ╚════██║   ║
    ║      ██║   ██║  ██║███████║██║  ██╗███████║   ║
    ║      ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝   ║
    ║                                                ║
    ║         🚀 Gestor de Tareas Pro v3.0 🚀        ║
    ║                                                ║
    ╚════════════════════════════════════════════════╝
    """
    
    # Panel principal con gradiente
    welcome_panel = Panel(
        Align.center(Text(logo, style="bright_cyan")),
        border_style="bright_cyan",
        padding=(0, 2)
    )
    
    console.print(welcome_panel)
    
    # Información adicional
    current_time = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    info_text = Text()
    info_text.append("📅 ", style="bright_yellow")
    info_text.append(current_time, style="dim")
    info_text.append("  |  ", style="dim")
    info_text.append("👤 ", style="bright_green")
    info_text.append("@glitchbane", style="bright_cyan")
    
    console.print(Align.center(info_text))
    console.print()


def show_dashboard(tasks):
    """
    Muestra un dashboard visual con estadísticas y resumen.
    """
    # Calcular estadísticas
    total_tasks = len(tasks)
    completed = len([t for t in tasks if t.get("completed", False)])
    pending = total_tasks - completed
    
    # Contar por prioridad
    high_priority = len([t for t in tasks if t.get("priority") == "alta" and not t.get("completed")])
    medium_priority = len([t for t in tasks if t.get("priority") == "media" and not t.get("completed")])
    low_priority = len([t for t in tasks if t.get("priority") == "baja" and not t.get("completed")])
    
    # Tareas urgentes (vencidas o próximas)
    from datetime import date, timedelta
    today = date.today()
    urgent_count = 0
    
    for task in tasks:
        if task.get("completed"):
            continue
        deadline = task.get("deadline")
        if deadline:
            try:
                deadline_date = datetime.strptime(deadline, "%d/%m/%Y").date()
                days_until = (deadline_date - today).days
                if days_until <= 3:
                    urgent_count += 1
            except:
                pass
    
    # Crear tarjetas de estadísticas
    cards = []
    
    # Card 1: Total
    card1 = Panel(
        Align.center(
            f"[bold bright_cyan]{total_tasks}[/bold bright_cyan]\n"
            f"[dim]Total Tareas[/dim]"
        ),
        border_style="bright_cyan",
        width=20
    )
    cards.append(card1)
    
    # Card 2: Pendientes
    card2 = Panel(
        Align.center(
            f"[bold bright_yellow]{pending}[/bold bright_yellow]\n"
            f"[dim]Pendientes[/dim]"
        ),
        border_style="bright_yellow",
        width=20
    )
    cards.append(card2)
    
    # Card 3: Completadas
    card3 = Panel(
        Align.center(
            f"[bold bright_green]{completed}[/bold bright_green]\n"
            f"[dim]Completadas[/dim]"
        ),
        border_style="bright_green",
        width=20
    )
    cards.append(card3)
    
    # Card 4: Urgentes
    card4 = Panel(
        Align.center(
            f"[bold bright_red]{urgent_count}[/bold bright_red]\n"
            f"[dim]Urgentes[/dim]"
        ),
        border_style="bright_red",
        width=20
    )
    cards.append(card4)
    
    # Mostrar tarjetas en columnas
    console.print(Columns(cards, equal=True, expand=True))
    console.print()
    
    # Barra de progreso
    if total_tasks > 0:
        percentage = int((completed / total_tasks) * 100)
        
        progress_panel = Panel(
            f"[bold]Progreso General:[/bold]\n\n"
            f"{'█' * (percentage // 2)}{'░' * (50 - percentage // 2)} {percentage}%\n\n"
            f"[dim]{completed} de {total_tasks} tareas completadas[/dim]",
            title="📊 Estadísticas",
            border_style="bright_magenta",
            padding=(1, 2)
        )
        console.print(progress_panel)
        console.print()


def show_menu():
    """
    Menú principal con diseño moderno y organizado.
    """
    # Crear tabla para el menú
    menu_table = Table.grid(padding=(0, 2))
    menu_table.add_column(style="dim", justify="right")
    menu_table.add_column(style="bold")
    
    # Sección: Gestión de Tareas
    console.print(Panel(
        "[bold bright_cyan]📋 GESTIÓN DE TAREAS[/bold bright_cyan]",
        border_style="bright_cyan"
    ))
    
    menu_table.add_row("1", "➕ Agregar tarea")
    menu_table.add_row("2", "✅ Marcar como completada")
    menu_table.add_row("3", "🗑️  Eliminar tarea")
    menu_table.add_row("4", "🔍 Filtrar tareas")
    menu_table.add_row("5", "✏️  Editar tarea")
    menu_table.add_row("6", "🔎 Buscar tareas")
    
    console.print(menu_table)
    console.print()
    
    # Sección: Importar/Exportar
    console.print(Panel(
        "[bold bright_yellow]💾 IMPORTAR / EXPORTAR[/bold bright_yellow]",
        border_style="bright_yellow"
    ))
    
    import_export_table = Table.grid(padding=(0, 2))
    import_export_table.add_column(style="dim", justify="right")
    import_export_table.add_column(style="bold")
    import_export_table.add_row("7", "📤 Exportar a CSV")
    import_export_table.add_row("8", "📥 Importar desde CSV")
    
    console.print(import_export_table)
    console.print()
    
    # Sección: Productividad
    console.print(Panel(
        "[bold bright_green]🍅 PRODUCTIVIDAD[/bold bright_green]",
        border_style="bright_green"
    ))
    
    productivity_table = Table.grid(padding=(0, 2))
    productivity_table.add_column(style="dim", justify="right")
    productivity_table.add_column(style="bold")
    productivity_table.add_row("9", "👁️  Mostrar/Ocultar completadas")
    productivity_table.add_row("10", "🍅 Iniciar Pomodoro")
    productivity_table.add_row("11", "📊 Estadísticas Pomodoro")
    
    console.print(productivity_table)
    console.print()
    
    # Sección: Configuración
    console.print(Panel(
        "[bold bright_magenta]⚙️  CONFIGURACIÓN[/bold bright_magenta]",
        border_style="bright_magenta"
    ))
    
    config_table = Table.grid(padding=(0, 2))
    config_table.add_column(style="dim", justify="right")
    config_table.add_column(style="bold")
    config_table.add_row("12", "⏱️  Configurar tiempos Pomodoro")
    config_table.add_row("13", "📱 Configurar Telegram")
    
    console.print(config_table)
    console.print()
    
    # Salir
    console.print(Rule(style="dim"))
    exit_table = Table.grid(padding=(0, 2))
    exit_table.add_column(style="dim", justify="right")
    exit_table.add_column(style="bold red")
    exit_table.add_row("14", "🚪 Salir")
    console.print(exit_table)
    
    console.print()
    
    return Prompt.ask(
        "[bold bright_cyan]➤[/bold bright_cyan] Seleccione una opción",
        choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
    )


def show_tasks(tasks, sort_by=None, show_completed=False):
    """
    Muestra las tareas con diseño moderno tipo tarjetas.
    """
    # Primero mostramos el panel de tareas urgentes (si las hay)
    show_urgent_tasks_panel(tasks)
    
    # Ordenamos las tareas
    sorted_tasks = sort_tasks_by_priority_and_deadline(tasks)
    
    # Si no hay tareas
    if not sorted_tasks:
        empty_panel = Panel(
            Align.center(
                "[dim]📭 No hay tareas para mostrar[/dim]\n\n"
                "[bright_cyan]¡Comienza agregando una nueva tarea![/bright_cyan]"
            ),
            border_style="dim",
            padding=(2, 4)
        )
        console.print(empty_panel)
        return
    
    # Crear tabla moderna
    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="bright_blue",
        row_styles=["", "dim"],
        padding=(0, 1)
    )
    
    # Solo "Tarea" es flexible. Las demas llevan ancho fijo y no_wrap para que
    # Rich, cuando la tabla no cabe, recorte la descripcion en vez de comerse
    # columnas enteras (el icono de estado desaparecia por debajo de 120 cols).
    table.add_column("ID", style="dim", width=4, justify="center", no_wrap=True)
    table.add_column("", width=2, justify="center", no_wrap=True)  # Icono estado
    table.add_column("Tarea", style="bold", min_width=14)
    table.add_column("Prioridad", justify="center", width=10, no_wrap=True)
    table.add_column("Fecha Límite", justify="center", width=14, no_wrap=True)
    table.add_column("🍅", justify="center", width=5, no_wrap=True)
    
    # Variables para separadores
    last_priority = None
    
    for idx, task in enumerate(sorted_tasks, start=1):
        description = task.get("description", "Sin descripción")
        completed = task.get("completed", False)
        priority = task.get("priority", "baja")
        deadline = task.get("deadline")
        pomodoros = task.get("pomodoros_completed", 0)
        
        # Añadir separador visual entre prioridades
        if last_priority and last_priority != priority:
            table.add_row("", "", "", "", "", "", end_section=True)
        last_priority = priority
        
        # Icono de estado
        status_icon = "✅" if completed else "⭕"
        
        # Color según prioridad
        priority_colors = {
            "alta": "[bold red]",
            "media": "[bold yellow]",
            "baja": "[bold green]"
        }
        priority_color = priority_colors.get(priority, "[white]")
        
        # Formato de prioridad con icono
        priority_icons = {
            "alta": "🔴",
            "media": "🟡",
            "baja": "🟢"
        }
        priority_icon = priority_icons.get(priority, "⚪")
        priority_text = f"{priority_icon} {priority.upper()}"
        
        # Formatear fecha
        formatted_deadline = format_deadline(deadline, completed)
        
        # Pomodoros
        pomodoros_text = f"{pomodoros}" if pomodoros > 0 else "[dim]-[/dim]"
        
        # Estilo de la descripción
        if completed:
            description = f"[dim strikethrough]{description}[/dim strikethrough]"
        else:
            description = f"{priority_color}{description}[/{priority_color.strip('[]')}]"
        
        # Añadir fila
        table.add_row(
            str(idx),
            status_icon,
            description,
            priority_text,
            formatted_deadline,
            pomodoros_text
        )
    
    # Panel contenedor para la tabla
    table_panel = Panel(
        table,
        title="[bold bright_cyan]📋 Tus Tareas[/bold bright_cyan]",
        border_style="bright_cyan",
        padding=(1, 2)
    )
    
    console.print(table_panel)
    console.print()
    
    # Leyenda
    legend = (
        "[dim]Leyenda:[/dim] "
        "⚠️ Vencida | "
        "⏰ Vence pronto | "
        "🍅 Pomodoros completados"
    )
    console.print(Align.center(legend))
    
    # Indicador de completadas ocultas
    if not show_completed:
        completed_count = len([t for t in tasks if t.get("completed", False)])
        if completed_count > 0:
            console.print()
            info_panel = Panel(
                f"[dim]💡 Hay [bold]{completed_count}[/bold] tarea(s) completada(s) oculta(s).[/dim]\n"
                f"[bright_cyan]→ Usa la opción 9 para verlas[/bright_cyan]",
                border_style="dim",
                padding=(0, 2)
            )
            console.print(info_panel)
    else:
        console.print()
        console.print(Align.center("[bright_green]✅ Mostrando tareas completadas[/bright_green]"))
    
    console.print()


def show_urgent_tasks_panel(tasks):
    """
    Panel destacado para tareas urgentes.
    """
    from datetime import date, timedelta
    
    today = date.today()
    urgent_tasks = []
    overdue_tasks = []
    
    for task in tasks:
        if task.get("completed"):
            continue
        
        deadline = task.get("deadline")
        if not deadline:
            continue
        
        try:
            deadline_date = datetime.strptime(deadline, "%d/%m/%Y").date()
            days_until = (deadline_date - today).days
            
            if days_until < 0:
                overdue_tasks.append(task)
            elif days_until <= 3:
                urgent_tasks.append(task)
        except:
            continue
    
    if overdue_tasks or urgent_tasks:
        # Construir mensaje
        message = Text()
        
        if overdue_tasks:
            message.append("⚠️  ", style="bold red")
            message.append(f"{len(overdue_tasks)} tarea(s) vencida(s)", style="bold red")
        
        if overdue_tasks and urgent_tasks:
            message.append(" | ", style="dim")
        
        if urgent_tasks:
            message.append("⏰ ", style="bold yellow")
            message.append(f"{len(urgent_tasks)} tarea(s) próxima(s) a vencer", style="bold yellow")
        
        # Panel de alerta
        alert_panel = Panel(
            Align.center(message),
            title="[bold red blink]🚨 ATENCIÓN 🚨[/bold red blink]",
            border_style="bold red",
            padding=(1, 2)
        )
        
        console.print(alert_panel)
        console.print()


def format_deadline(deadline, completed=False):
    """
    Formatea la fecha límite con días restantes.
    """
    if not deadline:
        return "[dim]Sin fecha[/dim]"
    
    if completed:
        return f"[dim]{deadline}[/dim]"
    
    try:
        from datetime import date
        deadline_date = datetime.strptime(deadline, "%d/%m/%Y").date()
        today = date.today()
        days_until = (deadline_date - today).days
        
        if days_until < 0:
            return f"[bold red]⚠️  {deadline}\n(Vencida hace {abs(days_until)} día(s))[/bold red]"
        elif days_until == 0:
            return f"[bold yellow]⏰ {deadline}\n(¡Hoy!)[/bold yellow]"
        elif days_until == 1:
            return f"[bold yellow]⏰ {deadline}\n(Mañana)[/bold yellow]"
        elif days_until <= 3:
            return f"[yellow]⏰ {deadline}\n(En {days_until} días)[/yellow]"
        else:
            return f"[bright_cyan]{deadline}\n(En {days_until} días)[/bright_cyan]"
    except:
        return deadline


def sort_tasks_by_priority_and_deadline(tasks):
    """
    Ordena las tareas por prioridad y fecha límite.
    """
    priority_order = {"alta": 1, "media": 2, "baja": 3}
    
    def sort_key(task):
        priority = task.get("priority", "baja")
        priority_value = priority_order.get(priority, 4)
        
        deadline = task.get("deadline")
        if deadline:
            try:
                deadline_date = datetime.strptime(deadline, "%d/%m/%Y")
                return (priority_value, deadline_date)
            except:
                return (priority_value, datetime.max)
        else:
            return (priority_value, datetime.max)
    
    return sorted(tasks, key=sort_key)


def is_overdue(deadline):
    """
    Verifica si una fecha límite está vencida.
    """
    if not deadline:
        return False
    
    try:
        from datetime import date
        deadline_date = datetime.strptime(deadline, "%d/%m/%Y").date()
        return deadline_date < date.today()
    except:
        return False


def show_success_message(message):
    """
    Muestra un mensaje de éxito con estilo.
    """
    success_panel = Panel(
        Align.center(f"[bold bright_green]✅ {message}[/bold bright_green]"),
        border_style="bright_green",
        padding=(1, 4)
    )
    console.print(success_panel)


def show_error_message(message):
    """
    Muestra un mensaje de error con estilo.
    """
    error_panel = Panel(
        Align.center(f"[bold bright_red]❌ {message}[/bold bright_red]"),
        border_style="bright_red",
        padding=(1, 4)
    )
    console.print(error_panel)


def show_info_message(message):
    """
    Muestra un mensaje informativo con estilo.
    """
    info_panel = Panel(
        Align.center(f"[bold bright_cyan]ℹ️  {message}[/bold bright_cyan]"),
        border_style="bright_cyan",
        padding=(1, 4)
    )
    console.print(info_panel)