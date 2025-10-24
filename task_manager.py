import json
import os
from datetime import datetime
from rich.prompt import Prompt
from rich.console import Console
from ui import show_tasks, show_welcome_panel

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

# Validar formato de fecha
def validate_date(date_string):
    """
    Valida que la fecha tenga el formato DD/MM/YYYY y sea válida.
    Retorna True si es válida, False si no lo es.
    """
    try:
        # Intentamos convertir la cadena a un objeto datetime
        datetime.strptime(date_string, "%d/%m/%Y")
        return True
    except ValueError:
        # Si hay un error, la fecha no es válida
        return False

# Agregar una nueva tarea
def add_task(tasks):
    """
    Agrega una nueva tarea a la lista.
    Ahora incluye la funcionalidad de añadir una fecha límite opcional.
    """
    # Solicitar la descripción de la tarea
    description = Prompt.ask("Ingrese la descripción de la tarea")
    
    # Solicitar la prioridad
    priority = Prompt.ask("Ingrese la prioridad (alta, media, baja)", choices=["alta", "media", "baja"])
    
    # Preguntar si desea añadir una fecha límite
    add_deadline = Prompt.ask("¿Desea añadir una fecha límite? (s/n)", choices=["s", "n"], default="n")
    
    deadline = None  # Por defecto, no hay fecha límite
    
    if add_deadline == "s":
        # Bucle para asegurar que se ingrese una fecha válida
        while True:
            deadline_input = Prompt.ask("Ingrese la fecha límite (DD/MM/YYYY)")
            
            # Validamos el formato de la fecha
            if validate_date(deadline_input):
                deadline = deadline_input
                break
            else:
                console.print("[bold red]Formato de fecha inválido. Use DD/MM/YYYY (ejemplo: 25/12/2024)[/bold red]")
    
    # Creamos el diccionario de la tarea con todos sus campos
    tasks.append({
        "description": description,
        "completed": False,
        "priority": priority,
        "deadline": deadline  # Puede ser None si no se añadió fecha
    })
    
    console.print("[bold green]Tarea agregada correctamente[/bold green]")

# Marcar una tarea como completada
def complete_task(tasks):
    """
    Marca una tarea como completada.
    
    Mejoras:
    - Muestra solo tareas PENDIENTES (no completadas)
    - Permite cancelar con opción 0
    """
    # Filtrar solo tareas PENDIENTES (no completadas)
    pending_tasks = [task for task in tasks if not task.get("completed", False)]
    
    if not pending_tasks:
        console.print("[bold yellow]No hay tareas pendientes para completar[/bold yellow]")
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")
        return

    # Limpiar la pantalla para que la selección sea más clara
    console.clear()
    show_welcome_panel()

    # Mostrar solo las tareas PENDIENTES
    console.print("\n[bold cyan]Seleccione una tarea para completar:[/bold cyan]")
    show_tasks(pending_tasks, show_completed=False)

    # Importamos la función de ordenamiento
    from ui import sort_tasks_by_priority_and_deadline
    sorted_pending = sort_tasks_by_priority_and_deadline(pending_tasks)

    # Pedir el ID con opción de cancelar
    console.print("\n[dim]💡 Escribe '0' para cancelar y volver al menú[/dim]")
    
    try:
        task_input = Prompt.ask(
            "Ingrese el ID de la tarea",
            choices=["0"] + [str(i) for i in range(1, len(sorted_pending) + 1)]
        )
        
        # Permitir cancelar con 0
        if task_input == "0":
            console.print("\n[yellow]⏮️  Operación cancelada[/yellow]")
            console.print("\n[dim]Presiona Enter para continuar...[/dim]")
            Prompt.ask("")
            return
        
        task_id = int(task_input) - 1
        
        # Encontrar la tarea en la lista original de TODAS las tareas
        task_to_complete = sorted_pending[task_id]
        original_index = tasks.index(task_to_complete)
        
        # Marcar como completada
        tasks[original_index]["completed"] = True
        
        # NUEVO: Enviar notificación por Telegram
        try:
            from telegram_bot import notify_task_completed
            pomodoros = task_to_complete.get("pomodoros_completed", 0)
            notify_task_completed(task_to_complete, pomodoros)
        except:
            pass  # Si falla, continuar normalmente
        
        # Mensaje de éxito
        console.clear()
        show_welcome_panel()
        console.print(f"[bold green]✅ Tarea completada: {task_to_complete['description']}[/bold green]")
        console.print("[dim]📱 Notificación enviada a Telegram[/dim]")
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")
        
    except (ValueError, KeyboardInterrupt):
        console.print("\n[yellow]⏮️  Operación cancelada[/yellow]")
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")

# Eliminar una tarea
def delete_task(tasks):
    """
    Elimina una tarea de la lista.
    
    Mejoras:
    - Permite cancelar con opción 0
    - Pausa después del mensaje
    """
    if not tasks:
        console.print("[bold yellow]No hay tareas disponibles[/bold yellow]")
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")
        return

    # Limpiar la pantalla para que la selección sea más clara
    console.clear()
    show_welcome_panel()

    # Mostrar las tareas ordenadas solo para selección
    console.print("\n[bold cyan]Seleccione una tarea para eliminar:[/bold cyan]")
    show_tasks(tasks)

    # Importamos la función de ordenamiento para mantener consistencia
    from ui import sort_tasks_by_priority_and_deadline
    sorted_tasks = sort_tasks_by_priority_and_deadline(tasks)

    # Pedir el ID con opción de cancelar
    console.print("\n[dim]💡 Escribe '0' para cancelar y volver al menú[/dim]")
    
    try:
        task_input = Prompt.ask(
            "Ingrese el ID de la tarea",
            choices=["0"] + [str(i) for i in range(1, len(sorted_tasks) + 1)]
        )
        
        # Permitir cancelar con 0
        if task_input == "0":
            console.print("\n[yellow]⏮️  Operación cancelada[/yellow]")
            console.print("\n[dim]Presiona Enter para continuar...[/dim]")
            Prompt.ask("")
            return
        
        task_id = int(task_input) - 1

        # Encontrar el índice de la tarea en la lista original
        task_to_remove = sorted_tasks[task_id]
        original_index = tasks.index(task_to_remove)

        # Eliminar la tarea de la lista original
        removed_task = tasks.pop(original_index)
        
        # Limpiar la pantalla y mostrar solo el mensaje de éxito
        console.clear()
        show_welcome_panel()
        console.print(f"[bold red]🗑️  Tarea eliminada: {removed_task['description']}[/bold red]")
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")
        
    except (ValueError, KeyboardInterrupt):
        console.print("\n[yellow]⏮️  Operación cancelada[/yellow]")
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")

# Filtrar tareas por estado
def filter_tasks(tasks, status=None):
    if status == "completed":
        return [task for task in tasks if task.get("completed", False)]
    elif status == "pending":
        return [task for task in tasks if not task.get("completed", False)]
    return tasks

# Nueva función: Filtrar solo tareas urgentes
def filter_urgent_tasks(tasks):
    """
    Filtra las tareas para mostrar solo las URGENTES.
    
    Una tarea es urgente si:
    1. Está vencida (fecha límite < hoy)
    2. Está próxima a vencer (fecha límite <= hoy + 3 días)
    3. NO está completada
    
    Retorna:
    - Lista de tareas urgentes ordenadas por fecha (más urgentes primero)
    """
    from datetime import datetime
    
    urgent_tasks = []
    today = datetime.now()
    
    for task in tasks:
        # Solo consideramos tareas NO completadas
        if task.get("completed", False):
            continue
        
        deadline_str = task.get("deadline")
        
        # Si no tiene fecha límite, no es urgente
        if not deadline_str:
            continue
        
        try:
            # Convertimos la fecha límite a objeto datetime
            deadline = datetime.strptime(deadline_str, "%d/%m/%Y")
            
            # Calculamos los días hasta la fecha límite
            days_until = (deadline.date() - today.date()).days
            
            # Es urgente si está vencida o vence en 3 días o menos
            if days_until <= 3:
                urgent_tasks.append(task)
        
        except ValueError:
            # Si hay error al parsear la fecha, la ignoramos
            continue
    
    return urgent_tasks

# Buscar tareas por palabra clave
def search_tasks(tasks):
    query = Prompt.ask("Ingrese una palabra clave para buscar")
    results = [task for task in tasks if query.lower() in task["description"].lower()]
    if results:
        show_tasks(results)
        console.print("\n[bold cyan]Presione Enter para continuar...[/bold cyan]")
        Prompt.ask("")
    else:
        console.print("[bold yellow]No se encontraron tareas[/bold yellow]")
        console.print("\n[bold cyan]Presione Enter para continuar...[/bold cyan]")
        Prompt.ask("")

# Exportar tareas a CSV
def export_tasks_to_csv(tasks):
    if not tasks:
        console.print("[bold yellow]No hay tareas para exportar.[/bold yellow]")
        return

    try:
        import csv
        with open("tasks.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Actualizamos el encabezado para incluir la fecha límite
            writer.writerow(["ID", "Descripción", "Estado", "Prioridad", "Fecha Límite"])
            for idx, task in enumerate(tasks, start=1):
                writer.writerow([
                    idx,
                    task["description"],
                    task["completed"],
                    task.get("priority", "N/A"),
                    task.get("deadline", "Sin fecha")  # Incluimos la fecha límite
                ])
        console.print("[bold green]Tareas exportadas a tasks.csv[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error al exportar tareas: {str(e)}[/bold red]")

# Importar tareas desde CSV
def import_tasks_from_csv(tasks):
    import csv
    if not os.path.exists("tasks.csv"):
        console.print("[bold red]El archivo tasks.csv no existe[/bold red]")
        return

    try:
        with open("tasks.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Manejamos la fecha límite al importar
                deadline = row.get("Fecha Límite", "Sin fecha")
                if deadline == "Sin fecha":
                    deadline = None
                
                imported_task = {
                    "description": row["Descripción"],
                    "completed": row["Estado"] == "True",
                    "priority": row["Prioridad"],
                    "deadline": deadline
                }
                tasks.append(imported_task)
        console.print("[bold green]Tareas importadas desde tasks.csv[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error al importar tareas: {str(e)}[/bold red]")

# Editar una tarea existente
def edit_task(tasks):
    """
    Permite editar una tarea existente.
    Ahora incluye la opción de editar la fecha límite.
    
    Mejoras:
    - Permite cancelar con opción 0
    """
    if not tasks:
        console.print("[bold yellow]No hay tareas disponibles para editar[/bold yellow]")
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")
        return

    # Mostrar las tareas ordenadas
    show_tasks(tasks)
    
    # Importamos la función de ordenamiento para mantener consistencia
    from ui import sort_tasks_by_priority_and_deadline
    sorted_tasks = sort_tasks_by_priority_and_deadline(tasks)
    
    # Pedir el ID con opción de cancelar
    console.print("\n[dim]💡 Escribe '0' para cancelar y volver al menú[/dim]")
    
    try:
        task_input = Prompt.ask(
            "Ingrese el ID de la tarea",
            choices=["0"] + [str(i) for i in range(1, len(sorted_tasks) + 1)]
        )
        
        # Permitir cancelar con 0
        if task_input == "0":
            console.print("\n[yellow]⏮️  Operación cancelada[/yellow]")
            console.print("\n[dim]Presiona Enter para continuar...[/dim]")
            Prompt.ask("")
            return
        
        task_id = int(task_input) - 1
        
        # Encontrar el índice de la tarea en la lista original
        task_to_edit = sorted_tasks[task_id]
        original_index = tasks.index(task_to_edit)

        # Mostrar las opciones de edición (ahora incluye fecha límite)
        console.print("\n¿Qué desea editar?")
        console.print("1. Descripción")
        console.print("2. Prioridad")
        console.print("3. Estado (completada/pendiente)")
        console.print("4. Fecha límite")
        console.print("0. Cancelar")
        edit_choice = Prompt.ask("Seleccione una opción", choices=["0", "1", "2", "3", "4"])
        
        # Permitir cancelar
        if edit_choice == "0":
            console.print("\n[yellow]⏮️  Edición cancelada[/yellow]")
            console.print("\n[dim]Presiona Enter para continuar...[/dim]")
            Prompt.ask("")
            return
        
        # Editar el campo seleccionado
        if edit_choice == "1":
            new_description = Prompt.ask("Ingrese la nueva descripción", default=tasks[original_index]["description"])
            tasks[original_index]["description"] = new_description
            console.print("[bold green]✅ Descripción actualizada correctamente[/bold green]")
        
        elif edit_choice == "2":
            new_priority = Prompt.ask("Ingrese la nueva prioridad (alta, media, baja)", choices=["alta", "media", "baja"], default=tasks[original_index]["priority"])
            tasks[original_index]["priority"] = new_priority
            console.print("[bold green]✅ Prioridad actualizada correctamente[/bold green]")
        
        elif edit_choice == "3":
            new_status = Prompt.ask("¿Marcar como completada? (s/n)", choices=["s", "n"], default="n")
            tasks[original_index]["completed"] = (new_status == "s")
            console.print("[bold green]✅ Estado actualizado correctamente[/bold green]")
        
        elif edit_choice == "4":
            # Nueva opción para editar la fecha límite
            current_deadline = tasks[original_index].get("deadline", "Sin fecha")
            console.print(f"\nFecha límite actual: [cyan]{current_deadline}[/cyan]")
            
            # Preguntar si quiere eliminar, modificar o añadir la fecha
            if current_deadline and current_deadline != "Sin fecha":
                action = Prompt.ask(
                    "¿Qué desea hacer?",
                    choices=["modificar", "eliminar", "cancelar"],
                    default="modificar"
                )
                
                if action == "cancelar":
                    console.print("\n[yellow]⏮️  Edición cancelada[/yellow]")
                elif action == "eliminar":
                    tasks[original_index]["deadline"] = None
                    console.print("[bold green]✅ Fecha límite eliminada[/bold green]")
                else:
                    # Modificar la fecha
                    while True:
                        new_deadline = Prompt.ask("Ingrese la nueva fecha límite (DD/MM/YYYY)")
                        if validate_date(new_deadline):
                            tasks[original_index]["deadline"] = new_deadline
                            console.print("[bold green]✅ Fecha límite actualizada correctamente[/bold green]")
                            break
                        else:
                            console.print("[bold red]Formato de fecha inválido. Use DD/MM/YYYY[/bold red]")
            else:
                # Añadir una nueva fecha límite
                while True:
                    new_deadline = Prompt.ask("Ingrese la fecha límite (DD/MM/YYYY o '0' para cancelar)")
                    if new_deadline == "0":
                        console.print("\n[yellow]⏮️  Edición cancelada[/yellow]")
                        break
                    if validate_date(new_deadline):
                        tasks[original_index]["deadline"] = new_deadline
                        console.print("[bold green]✅ Fecha límite añadida correctamente[/bold green]")
                        break
                    else:
                        console.print("[bold red]Formato de fecha inválido. Use DD/MM/YYYY[/bold red]")
        
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")
        
    except (ValueError, KeyboardInterrupt):
        console.print("\n[yellow]⏮️  Operación cancelada[/yellow]")
        console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        Prompt.ask("")