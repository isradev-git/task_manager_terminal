import time
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.table import Table
from rich.text import Text
import threading

console = Console()

# Configuración del Pomodoro (en minutos)
POMODORO_WORK_TIME = 25      # Tiempo de trabajo
POMODORO_SHORT_BREAK = 5     # Descanso corto
POMODORO_LONG_BREAK = 15     # Descanso largo
POMODOROS_UNTIL_LONG = 4     # Pomodoros antes de descanso largo

class PomodoroTimer:
    """
    Clase que gestiona el temporizador Pomodoro.
    
    Características:
    - Temporizador de 25 minutos de trabajo
    - Descansos cortos (5 min) y largos (15 min)
    - Pausar y reanudar
    - Registro de pomodoros completados
    - NUEVO: Finalización anticipada con Enter (cuenta como completado)
    - NUEVO: Registro de tiempo real trabajado
    """
    
    def __init__(self, task_description):
        self.task_description = task_description
        self.pomodoros_completed = 0
        self.is_paused = False
        self.should_stop = False
        self.last_session_time = 0  # Tiempo real del último pomodoro en segundos
        
    def start_work_session(self, minutes=POMODORO_WORK_TIME):
        """
        Inicia una sesión de trabajo de Pomodoro.
        
        Parámetros:
        - minutes: duración de la sesión (por defecto 25 min)
        
        Retorna:
        - True si se completó, False si se canceló
        
        NUEVO: Registra el tiempo real trabajado
        """
        console.clear()
        
        # Panel de inicio
        start_panel = Panel(
            f"🍅 [bold green]MODO POMODORO INICIADO[/bold green]\n\n"
            f"Tarea: [cyan]{self.task_description}[/cyan]\n"
            f"Duración: [yellow]{minutes} minutos[/yellow]\n\n"
            f"[dim]Mantente enfocado. Sin distracciones.[/dim]",
            title="🎯 Sesión de Trabajo",
            border_style="green"
        )
        console.print(start_panel)
        console.print()
        
        # Ejecutar el temporizador
        completed, elapsed_time = self._run_timer(minutes * 60, "TRABAJO")
        
        if completed:
            self.pomodoros_completed += 1
            self.last_session_time = elapsed_time  # Guardar tiempo real
            self._show_completion_message(elapsed_time, minutes * 60)
            return True
        else:
            console.print(f"\n[yellow]⏸️  Sesión cancelada (trabajaste {elapsed_time // 60} min {elapsed_time % 60} seg)[/yellow]")
            return False
    
    def start_break(self, is_long_break=False):
        """
        Inicia un descanso (corto o largo).
        
        Parámetros:
        - is_long_break: True para descanso largo (15 min), False para corto (5 min)
        """
        console.clear()
        
        duration = POMODORO_LONG_BREAK if is_long_break else POMODORO_SHORT_BREAK
        break_type = "LARGO" if is_long_break else "CORTO"
        
        break_panel = Panel(
            f"☕ [bold cyan]TIEMPO DE DESCANSO {break_type}[/bold cyan]\n\n"
            f"Duración: [yellow]{duration} minutos[/yellow]\n\n"
            f"[dim]Relájate, estira las piernas, hidrátate.[/dim]",
            title="🌟 Descanso",
            border_style="cyan"
        )
        console.print(break_panel)
        console.print()
        
        # Ejecutar el temporizador de descanso (ignora el tiempo retornado)
        completed, _ = self._run_timer(duration * 60, f"DESCANSO {break_type}")
    
    def _run_timer(self, total_seconds, session_type):
        """
        Ejecuta el temporizador con barra de progreso.
        
        Parámetros:
        - total_seconds: duración total en segundos
        - session_type: tipo de sesión ("TRABAJO" o "DESCANSO")
        
        Retorna:
        - (True, elapsed_time) si se completó (natural o anticipadamente)
        - (False, elapsed_time) si se canceló sin completar
        
        NUEVO: Permite finalizar anticipadamente con Enter (cuenta como completado)
        """
        start_time = time.time()
        self.is_paused = False
        self.should_stop = False
        early_finish = False  # Nueva variable para finalización anticipada
        
        # Función para capturar input del usuario en segundo plano
        def wait_for_input():
            nonlocal early_finish
            try:
                input()  # Espera a que el usuario presione Enter
                early_finish = True  # Marca finalización anticipada
            except:
                pass
        
        # Solo capturar input si es sesión de TRABAJO
        if "TRABAJO" in session_type:
            # Iniciar thread para capturar Enter en segundo plano
            input_thread = threading.Thread(target=wait_for_input, daemon=True)
            input_thread.start()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=50),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            
            task_id = progress.add_task(
                f"[cyan]⏱️  {session_type}",
                total=total_seconds
            )
            
            elapsed = 0
            
            # Mostrar instrucciones según el tipo de sesión
            if "TRABAJO" in session_type:
                console.print("[dim]💡 Presiona [bold]Enter[/bold] si terminas antes | Ctrl+C para cancelar[/dim]\n")
            else:
                console.print("[dim]Ctrl+C para saltar descanso[/dim]\n")
            
            while elapsed < total_seconds:
                # Verificar si se canceló
                if self.should_stop:
                    return (False, elapsed)
                
                # Verificar si se finalizó anticipadamente (solo en trabajo)
                if early_finish and "TRABAJO" in session_type:
                    console.print("\n[bold green]✅ ¡Tarea completada anticipadamente![/bold green]")
                    time.sleep(1)  # Pausa para que se vea el mensaje
                    # Completar la barra al 100%
                    progress.update(task_id, completed=total_seconds)
                    time.sleep(0.5)
                    return (True, elapsed)  # Retorna True con tiempo real
                
                if not self.is_paused:
                    current_time = time.time()
                    elapsed = int(current_time - start_time)
                    progress.update(task_id, completed=elapsed)
                
                time.sleep(1)
            
            # Completado naturalmente
            progress.update(task_id, completed=total_seconds)
        
        return (True, total_seconds)
    
    def _show_completion_message(self, elapsed_seconds, total_seconds):
        """
        Muestra un mensaje de felicitación al completar un pomodoro.
        
        Parámetros:
        - elapsed_seconds: tiempo real trabajado en segundos
        - total_seconds: tiempo total del pomodoro en segundos
        
        NUEVO: Muestra si se completó anticipadamente
        """
        console.clear()
        
        # Calcular tiempo trabajado
        minutes_worked = elapsed_seconds // 60
        seconds_worked = elapsed_seconds % 60
        
        # Determinar si fue anticipado
        early = elapsed_seconds < total_seconds
        
        # Mensaje principal
        if early:
            time_msg = f"Tiempo trabajado: [cyan]{minutes_worked} min {seconds_worked} seg[/cyan] ⚡\n"
            efficiency = f"[green]¡Completaste la tarea antes de tiempo![/green]"
        else:
            time_msg = f"Tiempo trabajado: [cyan]{minutes_worked} minutos[/cyan]\n"
            efficiency = ""
        
        completion_panel = Panel(
            f"🎉 [bold green]¡POMODORO COMPLETADO![/bold green] 🎉\n\n"
            f"Tarea: [cyan]{self.task_description}[/cyan]\n"
            f"{time_msg}"
            f"Pomodoros completados: [yellow]{self.pomodoros_completed}[/yellow]\n\n"
            f"{efficiency}\n"
            f"[green]✅ ¡Excelente trabajo! Mantén el enfoque.[/green]",
            title="🏆 ¡Felicitaciones!",
            border_style="green"
        )
        console.print(completion_panel)
        console.print()
        
        # Sonido visual (parpadeo)
        for _ in range(3):
            console.print("🔔 ", end="")
            time.sleep(0.3)
        
        console.print("\n")


def start_pomodoro_for_task(task):
    """
    Inicia el modo Pomodoro para una tarea específica.
    
    Parámetros:
    - task: diccionario con la información de la tarea
    
    Retorna:
    - Número de pomodoros completados en esta sesión
    """
    console.clear()
    
    # Mostrar información de la tarea
    task_info = Table(title="📋 Información de la Tarea", show_header=False)
    task_info.add_column("Campo", style="cyan")
    task_info.add_column("Valor", style="white")
    
    task_info.add_row("Descripción", task["description"])
    task_info.add_row("Prioridad", task.get("priority", "media"))
    
    deadline = task.get("deadline")
    if deadline:
        task_info.add_row("Fecha límite", deadline)
    
    pomodoros_previos = task.get("pomodoros_completed", 0)
    task_info.add_row("Pomodoros previos", str(pomodoros_previos))
    
    console.print(task_info)
    console.print()
    
    # Confirmar inicio
    if not Confirm.ask("¿Iniciar modo Pomodoro para esta tarea?", default=True):
        return 0
    
    # Crear el temporizador
    timer = PomodoroTimer(task["description"])
    timer.pomodoros_completed = pomodoros_previos
    
    session_pomodoros = 0  # Pomodoros completados en esta sesión
    
    try:
        while True:
            # Sesión de trabajo
            console.clear()
            console.print(f"\n[bold cyan]🍅 Pomodoro #{timer.pomodoros_completed + 1}[/bold cyan]\n")
            
            completed = timer.start_work_session()
            
            if not completed:
                break
            
            session_pomodoros += 1
            
            # Preguntar si quiere continuar
            console.print("\n[bold green]Pomodoro completado.[/bold green]")
            
            # Determinar tipo de descanso
            if timer.pomodoros_completed % POMODOROS_UNTIL_LONG == 0 and timer.pomodoros_completed > 0:
                console.print(f"[cyan]Has completado {POMODOROS_UNTIL_LONG} pomodoros. ¡Tiempo de descanso largo![/cyan]")
                is_long = True
            else:
                is_long = False
            
            # Preguntar si quiere tomar el descanso
            take_break = Confirm.ask("¿Tomar descanso ahora?", default=True)
            
            if take_break:
                timer.start_break(is_long_break=is_long)
            
            # Preguntar si quiere continuar con otro pomodoro
            continue_working = Confirm.ask("¿Continuar con otro pomodoro?", default=True)
            
            if not continue_working:
                break
    
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⏸️  Sesión interrumpida por el usuario[/yellow]")
    
    # Actualizar el contador de pomodoros de la tarea
    task["pomodoros_completed"] = timer.pomodoros_completed
    
    # Mostrar resumen
    if session_pomodoros > 0:
        show_session_summary(task, session_pomodoros, timer.pomodoros_completed)
    
    return session_pomodoros


def show_session_summary(task, session_pomodoros, total_pomodoros):
    """
    Muestra un resumen de la sesión de Pomodoro completada.
    
    Parámetros:
    - task: la tarea trabajada
    - session_pomodoros: pomodoros completados en esta sesión
    - total_pomodoros: total de pomodoros de la tarea
    """
    console.clear()
    
    # Calcular tiempo trabajado
    minutes_worked = session_pomodoros * POMODORO_WORK_TIME
    hours = minutes_worked // 60
    mins = minutes_worked % 60
    
    summary_panel = Panel(
        f"📊 [bold cyan]RESUMEN DE LA SESIÓN[/bold cyan]\n\n"
        f"Tarea: [white]{task['description']}[/white]\n"
        f"Pomodoros completados hoy: [green]{session_pomodoros}[/green] 🍅\n"
        f"Total de pomodoros: [yellow]{total_pomodoros}[/yellow]\n"
        f"Tiempo trabajado: [cyan]{hours}h {mins}min[/cyan]\n\n"
        f"[green]¡Excelente sesión de trabajo productivo![/green]",
        title="🎯 Resumen",
        border_style="green"
    )
    
    console.print(summary_panel)
    console.print("\n[dim]Presiona Enter para continuar...[/dim]")
    input()


def show_pomodoro_stats(tasks):
    """
    Muestra estadísticas generales de Pomodoro de todas las tareas.
    
    Parámetros:
    - tasks: lista de todas las tareas
    """
    console.clear()
    
    # Calcular estadísticas
    total_pomodoros = sum(task.get("pomodoros_completed", 0) for task in tasks)
    total_time_minutes = total_pomodoros * POMODORO_WORK_TIME
    total_hours = total_time_minutes // 60
    total_mins = total_time_minutes % 60
    
    # Tareas con más pomodoros
    tasks_with_pomodoros = [
        (task["description"], task.get("pomodoros_completed", 0))
        for task in tasks
        if task.get("pomodoros_completed", 0) > 0
    ]
    
    tasks_with_pomodoros.sort(key=lambda x: x[1], reverse=True)
    top_5 = tasks_with_pomodoros[:5]
    
    # Panel de estadísticas generales
    stats_panel = Panel(
        f"🍅 [bold cyan]ESTADÍSTICAS DE POMODORO[/bold cyan]\n\n"
        f"Total de pomodoros completados: [green]{total_pomodoros}[/green]\n"
        f"Tiempo total trabajado: [yellow]{total_hours}h {total_mins}min[/yellow]\n"
        f"Tareas con pomodoros: [cyan]{len(tasks_with_pomodoros)}[/cyan]",
        title="📊 Estadísticas Generales",
        border_style="cyan"
    )
    
    console.print(stats_panel)
    console.print()
    
    # Tabla de top tareas
    if top_5:
        table = Table(title="🏆 Top 5 Tareas Más Trabajadas", show_header=True)
        table.add_column("Pos", style="cyan", width=5)
        table.add_column("Tarea", style="white", width=40)
        table.add_column("Pomodoros", style="green", justify="center", width=12)
        table.add_column("Tiempo", style="yellow", justify="center", width=12)
        
        for i, (description, pomodoros) in enumerate(top_5, 1):
            time_mins = pomodoros * POMODORO_WORK_TIME
            hours = time_mins // 60
            mins = time_mins % 60
            time_str = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
            
            table.add_row(
                f"#{i}",
                description[:40],
                f"{pomodoros} 🍅",
                time_str
            )
        
        console.print(table)
    else:
        console.print("[dim]No hay datos de pomodoros aún. ¡Empieza a trabajar![/dim]")
    
    console.print("\n[dim]Presiona Enter para continuar...[/dim]")
    input()


def configure_pomodoro_times():
    """
    Permite al usuario personalizar los tiempos del Pomodoro.
    """
    global POMODORO_WORK_TIME, POMODORO_SHORT_BREAK, POMODORO_LONG_BREAK, POMODOROS_UNTIL_LONG
    
    console.clear()
    
    config_panel = Panel(
        f"⚙️  [bold cyan]CONFIGURACIÓN DE TIEMPOS[/bold cyan]\n\n"
        f"Configuración actual:\n"
        f"• Trabajo: [green]{POMODORO_WORK_TIME} minutos[/green]\n"
        f"• Descanso corto: [yellow]{POMODORO_SHORT_BREAK} minutos[/yellow]\n"
        f"• Descanso largo: [cyan]{POMODORO_LONG_BREAK} minutos[/cyan]\n"
        f"• Pomodoros hasta descanso largo: [magenta]{POMODOROS_UNTIL_LONG}[/magenta]",
        title="🍅 Configuración Pomodoro",
        border_style="cyan"
    )
    
    console.print(config_panel)
    console.print()
    
    if not Confirm.ask("¿Deseas cambiar la configuración?", default=False):
        return
    
    try:
        # Solicitar nuevos valores
        work = int(Prompt.ask(
            "Tiempo de trabajo (minutos)",
            default=str(POMODORO_WORK_TIME)
        ))
        
        short_break = int(Prompt.ask(
            "Descanso corto (minutos)",
            default=str(POMODORO_SHORT_BREAK)
        ))
        
        long_break = int(Prompt.ask(
            "Descanso largo (minutos)",
            default=str(POMODORO_LONG_BREAK)
        ))
        
        until_long = int(Prompt.ask(
            "Pomodoros hasta descanso largo",
            default=str(POMODOROS_UNTIL_LONG)
        ))
        
        # Actualizar valores globales
        POMODORO_WORK_TIME = work
        POMODORO_SHORT_BREAK = short_break
        POMODORO_LONG_BREAK = long_break
        POMODOROS_UNTIL_LONG = until_long
        
        console.print("\n[green]✅ Configuración actualizada correctamente[/green]")
        
    except ValueError:
        console.print("\n[red]❌ Error: Ingresa solo números enteros[/red]")
    
    console.print("\n[dim]Presiona Enter para continuar...[/dim]")
    input()