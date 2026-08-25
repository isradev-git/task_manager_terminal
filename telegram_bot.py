"""
Módulo de Notificaciones por Telegram
Gestiona todas las notificaciones del gestor de tareas vía Telegram Bot.

Características:
- Notificación al completar tarea
- Avisos de tareas próximas (1 día antes)
- Avisos de tareas del día
- Avisos de tareas vencidas
- Verificación diaria automática
"""

import requests
import json
import os
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

# Configuración del Bot de Telegram
TELEGRAM_CONFIG_FILE = "telegram_config.json"

# Configuración por defecto.
# Las credenciales se dejan vacías a propósito: van en telegram_config.json,
# que está en .gitignore. Copia telegram_config.example.json para empezar.
DEFAULT_CONFIG = {
    "bot_token": "",
    "chat_id": "",
    "username": "",
    "first_name": "",
    "enabled": True,
    "notifications": {
        "task_completed": True,
        "task_tomorrow": True,
        "task_today": True,
        "task_overdue": True
    }
}


def load_telegram_config():
    """
    Carga la configuración de Telegram desde el archivo.
    Si no existe, crea uno con la configuración por defecto.
    """
    if os.path.exists(TELEGRAM_CONFIG_FILE):
        try:
            with open(TELEGRAM_CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            # Antes esto caia en silencio a la config por defecto y el usuario
            # veia "configuracion incompleta" sin saber que su fichero estaba roto.
            console.print(
                f"[red]❌ {TELEGRAM_CONFIG_FILE} no se pudo leer ({e}). "
                "Usando configuracion por defecto.[/red]"
            )
            return DEFAULT_CONFIG.copy()
    else:
        # Crear archivo con configuración por defecto
        save_telegram_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def save_telegram_config(config):
    """
    Guarda la configuración de Telegram en el archivo.
    """
    with open(TELEGRAM_CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def send_telegram_message(message, parse_mode="HTML"):
    """
    Envía un mensaje a través del bot de Telegram.
    
    Parámetros:
    - message: texto del mensaje (puede incluir HTML)
    - parse_mode: formato del mensaje ("HTML" o "Markdown")
    
    Retorna:
    - True si se envió correctamente, False si hubo error
    """
    config = load_telegram_config()
    
    # Verificar si las notificaciones están habilitadas
    if not config.get("enabled", True):
        return False
    
    bot_token = config.get("bot_token")
    chat_id = config.get("chat_id")
    
    if not bot_token or not chat_id:
        console.print(
            "[yellow]⚠️  Configuración de Telegram incompleta. "
            f"Rellena bot_token y chat_id en {TELEGRAM_CONFIG_FILE} "
            "(plantilla en telegram_config.example.json)[/yellow]"
        )
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        
        if response.status_code == 200:
            return True
        else:
            console.print(f"[red]Error al enviar mensaje: {response.status_code}[/red]")
            return False
            
    except requests.exceptions.Timeout:
        console.print("[yellow]⚠️  Timeout al conectar con Telegram[/yellow]")
        return False
    except requests.exceptions.ConnectionError:
        console.print("[yellow]⚠️  Sin conexión a Internet[/yellow]")
        return False
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return False


def notify_task_completed(task, pomodoros=0):
    """
    Notifica que una tarea ha sido completada.
    
    Parámetros:
    - task: diccionario con info de la tarea
    - pomodoros: número de pomodoros dedicados (opcional)
    """
    config = load_telegram_config()
    
    if not config["notifications"]["task_completed"]:
        return False
    
    description = task.get("description", "Sin descripción")
    priority = task.get("priority", "media")
    
    # Emoji según prioridad
    priority_emoji = {
        "alta": "🔴",
        "media": "🟡",
        "baja": "🟢"
    }
    emoji = priority_emoji.get(priority, "⚪")
    
    message = f"""
🎉 <b>¡Tarea Completada!</b> 🎉

{emoji} <b>{description}</b>

✅ Estado: <i>Completada</i>
📊 Prioridad: {priority.title()}
"""
    
    if pomodoros > 0:
        message += f"🍅 Pomodoros: {pomodoros}\n"
    
    message += f"\n⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    
    return send_telegram_message(message)


def notify_tasks_tomorrow(tasks):
    """
    Notifica sobre tareas que vencen mañana.
    
    Parámetros:
    - tasks: lista de tareas que vencen mañana
    """
    config = load_telegram_config()
    
    if not config["notifications"]["task_tomorrow"]:
        return False
    
    if not tasks:
        return False
    
    count = len(tasks)
    
    message = f"""
⏰ <b>Recordatorio: Tareas para Mañana</b>

📅 Tienes <b>{count}</b> tarea(s) que vencen mañana:

"""
    
    for i, task in enumerate(tasks[:5], 1):  # Máximo 5 tareas
        description = task.get("description", "")
        priority = task.get("priority", "media")
        
        priority_emoji = {
            "alta": "🔴",
            "media": "🟡",
            "baja": "🟢"
        }
        emoji = priority_emoji.get(priority, "⚪")
        
        message += f"{i}. {emoji} {description}\n"
    
    if count > 5:
        message += f"\n<i>... y {count - 5} más</i>\n"
    
    message += f"\n💡 ¡Planifica tu día!"
    
    return send_telegram_message(message)


def notify_tasks_today(tasks):
    """
    Notifica sobre tareas que vencen HOY.
    
    Parámetros:
    - tasks: lista de tareas que vencen hoy
    """
    config = load_telegram_config()
    
    if not config["notifications"]["task_today"]:
        return False
    
    if not tasks:
        return False
    
    count = len(tasks)
    
    message = f"""
🚨 <b>¡TAREAS PARA HOY!</b> 🚨

📅 Tienes <b>{count}</b> tarea(s) que vencen HOY:

"""
    
    for i, task in enumerate(tasks[:5], 1):  # Máximo 5 tareas
        description = task.get("description", "")
        priority = task.get("priority", "media")
        
        priority_emoji = {
            "alta": "🔴",
            "media": "🟡",
            "baja": "🟢"
        }
        emoji = priority_emoji.get(priority, "⚪")
        
        message += f"{i}. {emoji} <b>{description}</b>\n"
    
    if count > 5:
        message += f"\n<i>... y {count - 5} más</i>\n"
    
    message += f"\n⚡ ¡A trabajar!"
    
    return send_telegram_message(message)


def notify_tasks_overdue(tasks):
    """
    Notifica sobre tareas VENCIDAS.
    
    Parámetros:
    - tasks: lista de tareas vencidas
    """
    config = load_telegram_config()
    
    if not config["notifications"]["task_overdue"]:
        return False
    
    if not tasks:
        return False
    
    count = len(tasks)
    
    message = f"""
⚠️ <b>TAREAS VENCIDAS</b> ⚠️

📛 Tienes <b>{count}</b> tarea(s) que ya vencieron:

"""
    
    for i, task in enumerate(tasks[:5], 1):  # Máximo 5 tareas
        description = task.get("description", "")
        deadline = task.get("deadline", "")
        priority = task.get("priority", "media")
        
        priority_emoji = {
            "alta": "🔴",
            "media": "🟡",
            "baja": "🟢"
        }
        emoji = priority_emoji.get(priority, "⚪")
        
        # Calcular días de retraso
        if deadline:
            try:
                deadline_date = datetime.strptime(deadline, "%d/%m/%Y")
                days_overdue = (datetime.now().date() - deadline_date.date()).days
                message += f"{i}. {emoji} {description}\n   <i>Vencida hace {days_overdue} día(s)</i>\n\n"
            except (ValueError, TypeError):
                message += f"{i}. {emoji} {description}\n\n"
        else:
            message += f"{i}. {emoji} {description}\n\n"
    
    if count > 5:
        message += f"<i>... y {count - 5} más</i>\n\n"
    
    message += f"🔥 ¡Atención urgente!"
    
    return send_telegram_message(message)


def check_and_send_daily_notifications(tasks):
    """
    Verifica todas las tareas y envía notificaciones según las fechas.
    Esta función debe ejecutarse diariamente (o al iniciar la app).
    
    Parámetros:
    - tasks: lista completa de tareas
    """
    from datetime import date
    
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    tasks_tomorrow = []
    tasks_today = []
    tasks_overdue = []
    
    for task in tasks:
        # Solo tareas NO completadas
        if task.get("completed", False):
            continue
        
        deadline_str = task.get("deadline")
        if not deadline_str:
            continue
        
        try:
            deadline_date = datetime.strptime(deadline_str, "%d/%m/%Y").date()
            
            if deadline_date == tomorrow:
                tasks_tomorrow.append(task)
            elif deadline_date == today:
                tasks_today.append(task)
            elif deadline_date < today:
                tasks_overdue.append(task)
        except (ValueError, TypeError):
            continue
    
    # Enviar notificaciones
    sent_any = False
    
    if tasks_overdue:
        if notify_tasks_overdue(tasks_overdue):
            sent_any = True
    
    if tasks_today:
        if notify_tasks_today(tasks_today):
            sent_any = True
    
    if tasks_tomorrow:
        if notify_tasks_tomorrow(tasks_tomorrow):
            sent_any = True
    
    return sent_any


def test_telegram_connection():
    """
    Prueba la conexión con el bot de Telegram.
    Retorna True si funciona, False si hay error.
    """
    config = load_telegram_config()
    
    bot_token = config.get("bot_token")
    
    if not bot_token:
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                bot_info = data.get("result", {})
                console.print(f"\n[green]✅ Conexión exitosa con @{bot_info.get('username')}[/green]")
                return True
        
        console.print("[red]❌ Error al conectar con el bot[/red]")
        return False
        
    except requests.RequestException as e:
        console.print(f"[red]❌ No se pudo conectar con Telegram: {e}[/red]")
        return False


def configure_telegram():
    """
    Interfaz para configurar las notificaciones de Telegram.
    """
    console.clear()
    
    config_panel = Panel(
        "[bold cyan]⚙️  CONFIGURACIÓN DE TELEGRAM[/bold cyan]\n\n"
        "[dim]Configura las notificaciones de tu gestor de tareas[/dim]",
        title="🤖 Telegram Bot",
        border_style="cyan"
    )
    console.print(config_panel)
    console.print()
    
    config = load_telegram_config()
    
    # Mostrar configuración actual
    console.print("[bold]Configuración actual:[/bold]")
    console.print(f"Bot Token: [cyan]{config.get('bot_token', 'No configurado')[:20]}...[/cyan]")
    console.print(f"Chat ID: [cyan]{config.get('chat_id', 'No configurado')}[/cyan]")
    console.print(f"Usuario: [cyan]{config.get('username', 'No configurado')}[/cyan]")
    console.print(f"Estado: [{'green' if config.get('enabled') else 'red'}]{'Habilitado' if config.get('enabled') else 'Deshabilitado'}[/{'green' if config.get('enabled') else 'red'}]")
    console.print()
    
    # Menú de opciones
    console.print("[bold]Opciones:[/bold]")
    console.print("1. Probar conexión")
    console.print("2. Habilitar/Deshabilitar notificaciones")
    console.print("3. Configurar tipos de notificaciones")
    console.print("4. Enviar mensaje de prueba")
    console.print("5. Verificar tareas y enviar notificaciones ahora")
    console.print("0. Volver")
    
    choice = Prompt.ask("\nSeleccione una opción", choices=["0", "1", "2", "3", "4", "5"])
    
    if choice == "0":
        return
    
    elif choice == "1":
        console.print("\n[cyan]Probando conexión...[/cyan]")
        test_telegram_connection()
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")
    
    elif choice == "2":
        current = config.get("enabled", True)
        new_state = not current
        config["enabled"] = new_state
        save_telegram_config(config)
        
        state_text = "habilitadas" if new_state else "deshabilitadas"
        console.print(f"\n[green]✅ Notificaciones {state_text}[/green]")
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")
    
    elif choice == "3":
        console.clear()
        console.print("[bold cyan]Configurar Tipos de Notificaciones:[/bold cyan]\n")
        
        notif = config.get("notifications", DEFAULT_CONFIG["notifications"])
        
        # Tarea completada
        notif["task_completed"] = Confirm.ask(
            "¿Notificar al completar tarea?",
            default=notif.get("task_completed", True)
        )
        
        # Tarea mañana
        notif["task_tomorrow"] = Confirm.ask(
            "¿Notificar tareas que vencen mañana?",
            default=notif.get("task_tomorrow", True)
        )
        
        # Tarea hoy
        notif["task_today"] = Confirm.ask(
            "¿Notificar tareas que vencen hoy?",
            default=notif.get("task_today", True)
        )
        
        # Tarea vencida
        notif["task_overdue"] = Confirm.ask(
            "¿Notificar tareas vencidas?",
            default=notif.get("task_overdue", True)
        )
        
        config["notifications"] = notif
        save_telegram_config(config)
        
        console.print("\n[green]✅ Configuración guardada[/green]")
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")
    
    elif choice == "4":
        console.print("\n[cyan]Enviando mensaje de prueba...[/cyan]")
        
        test_message = f"""
🤖 <b>Mensaje de Prueba</b>

¡Hola {config.get('first_name', 'Usuario')}! 👋

Este es un mensaje de prueba de tu Gestor de Tareas.

✅ La configuración funciona correctamente.

🚀 ¡Ya puedes recibir notificaciones!
"""
        
        if send_telegram_message(test_message):
            console.print("\n[green]✅ Mensaje enviado correctamente[/green]")
            console.print("[dim]Revisa tu Telegram[/dim]")
        else:
            console.print("\n[red]❌ Error al enviar mensaje[/red]")
        
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")
    
    elif choice == "5":
        console.print("\n[cyan]Verificando tareas...[/cyan]")
        
        # Cargar tareas
        from task_manager import load_tasks
        tasks = load_tasks()
        
        if check_and_send_daily_notifications(tasks):
            console.print("\n[green]✅ Notificaciones enviadas[/green]")
            console.print("[dim]Revisa tu Telegram[/dim]")
        else:
            console.print("\n[yellow]No hay notificaciones que enviar en este momento[/yellow]")
        
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")


if __name__ == "__main__":
    # Prueba del módulo
    configure_telegram()