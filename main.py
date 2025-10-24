from task_manager import load_tasks, save_tasks, add_task, complete_task, delete_task, filter_tasks, search_tasks, edit_task, export_tasks_to_csv, import_tasks_from_csv, filter_urgent_tasks
from ui import show_menu, show_tasks, show_welcome_panel
from pomodoro import start_pomodoro_for_task, show_pomodoro_stats, configure_pomodoro_times
from telegram_bot import notify_task_completed, check_and_send_daily_notifications, configure_telegram
from rich.prompt import Prompt
from rich.console import Console

console = Console()

def main():
    # Cargar tareas desde el archivo JSON
    tasks = load_tasks()
    
    # Variable para controlar si mostramos tareas completadas
    # Por defecto: NO mostrar completadas (solo pendientes)
    show_completed = False
    
    # Mensaje de depuración para verificar que las tareas se cargaron
    if not tasks:
        print("No se encontraron tareas en tasks.json. La lista está vacía.")
    else:
        print(f"Se cargaron {len(tasks)} tareas desde tasks.json.")
    
    # NUEVO: Verificar y enviar notificaciones de tareas pendientes al iniciar
    try:
        check_and_send_daily_notifications(tasks)
    except:
        pass  # Si falla, continuar normalmente

    while True:
        # Mostrar el panel de bienvenida
        show_welcome_panel()
        
        # Filtrar tareas según la configuración actual
        # Por defecto mostramos solo pendientes (no completadas)
        if show_completed:
            # Mostrar TODAS las tareas (pendientes + completadas)
            tasks_to_show = tasks
        else:
            # Mostrar solo tareas PENDIENTES (ocultar completadas)
            tasks_to_show = filter_tasks(tasks, "pending")
        
        # Mostramos las tareas filtradas
        show_tasks(tasks_to_show, show_completed=show_completed)
        
        # Mostrar el menú y obtener la opción del usuario
        choice = show_menu()

        if choice == "1":
            # Agregar tarea
            add_task(tasks)
            
        elif choice == "2":
            # Marcar tarea como completada
            # Mostramos todas las tareas para poder seleccionar cualquiera
            complete_task(tasks)
            # Después de completar, mantenemos la vista actual
            
        elif choice == "3":
            # Eliminar tarea
            delete_task(tasks)
            
        elif choice == "4":
            # Filtrar tareas - AHORA INCLUYE "SOLO URGENTES"
            filter_choice = Prompt.ask(
                "Filtrar tareas",
                choices=["pendientes", "completadas", "urgentes", "todas"],
                default="pendientes"
            )
            
            # Limpiar pantalla para mostrar el filtro
            console.clear()
            show_welcome_panel()
            
            # Aplicar el filtro seleccionado
            if filter_choice == "completadas":
                filtered_tasks = filter_tasks(tasks, "completed")
                show_tasks(filtered_tasks, show_completed=True)
                
            elif filter_choice == "pendientes":
                filtered_tasks = filter_tasks(tasks, "pending")
                show_tasks(filtered_tasks, show_completed=False)
                
            elif filter_choice == "urgentes":
                # NUEVA FUNCIONALIDAD: Filtro de urgentes
                filtered_tasks = filter_urgent_tasks(tasks)
                
                if filtered_tasks:
                    console.print("\n[bold yellow]📌 Mostrando solo tareas URGENTES (vencidas o próximas a vencer)[/bold yellow]\n")
                    show_tasks(filtered_tasks, show_completed=False)
                else:
                    console.print("\n[bold green]✅ ¡Excelente! No tienes tareas urgentes[/bold green]\n")
                
            elif filter_choice == "todas":
                show_tasks(tasks, show_completed=True)
            
            console.print("\n[bold cyan]Presione Enter para continuar...[/bold cyan]")
            Prompt.ask("")
            
        elif choice == "5":
            # Editar tarea
            edit_task(tasks)
            
        elif choice == "6":
            # Buscar tareas
            search_tasks(tasks)
            
        elif choice == "7":
            # Exportar tareas a CSV
            export_tasks_to_csv(tasks)
            console.print("\n[bold cyan]Presione Enter para continuar...[/bold cyan]")
            Prompt.ask("")
            
        elif choice == "8":
            # Importar tareas desde CSV
            import_tasks_from_csv(tasks)
            
        elif choice == "9":
            # NUEVA OPCIÓN: Alternar vista de completadas
            show_completed = not show_completed
            
            if show_completed:
                console.print("\n[bold green]✅ Ahora mostrando tareas completadas[/bold green]")
            else:
                console.print("\n[bold cyan]📋 Ocultando tareas completadas[/bold cyan]")
            
            console.print("[dim]Presione Enter para continuar...[/dim]")
            Prompt.ask("")
            
        elif choice == "10":
            # NUEVA OPCIÓN: Iniciar Pomodoro
            # Mostrar tareas pendientes para seleccionar
            pending_tasks = filter_tasks(tasks, "pending")
            
            if not pending_tasks:
                console.print("\n[yellow]No hay tareas pendientes para trabajar[/yellow]")
                console.print("[dim]Presione Enter para continuar...[/dim]")
                Prompt.ask("")
                continue
            
            console.clear()
            show_welcome_panel()
            console.print("\n[bold cyan]🍅 Selecciona una tarea para trabajar con Pomodoro:[/bold cyan]\n")
            show_tasks(pending_tasks, show_completed=False)
            
            # Obtener lista ordenada para selección
            from ui import sort_tasks_by_priority_and_deadline
            sorted_pending = sort_tasks_by_priority_and_deadline(pending_tasks)
            
            try:
                task_id = int(Prompt.ask(
                    "Ingrese el ID de la tarea",
                    choices=[str(i) for i in range(1, len(sorted_pending) + 1)]
                )) - 1
                
                # Encontrar la tarea en la lista original
                selected_task = sorted_pending[task_id]
                original_index = tasks.index(selected_task)
                
                # Iniciar Pomodoro
                start_pomodoro_for_task(tasks[original_index])
                
            except (ValueError, KeyboardInterrupt):
                console.print("\n[yellow]Operación cancelada[/yellow]")
            
            console.print("\n[dim]Presione Enter para continuar...[/dim]")
            Prompt.ask("")
            
        elif choice == "11":
            # NUEVA OPCIÓN: Estadísticas de Pomodoro
            show_pomodoro_stats(tasks)
            
        elif choice == "12":
            # NUEVA OPCIÓN: Configurar tiempos de Pomodoro
            configure_pomodoro_times()
            
        elif choice == "13":
            # NUEVA OPCIÓN: Configurar Telegram
            configure_telegram()
            
        elif choice == "14":
            # Salir
            break

        # Guardar las tareas después de cada operación
        save_tasks(tasks)

if __name__ == "__main__":
    main()