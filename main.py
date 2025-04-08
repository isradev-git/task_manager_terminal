from task_manager import load_tasks, save_tasks, add_task, complete_task, delete_task, filter_tasks, search_tasks, edit_task, export_tasks_to_csv, import_tasks_from_csv
from ui import show_menu, show_tasks, show_welcome_panel
from rich.prompt import Prompt
from rich.console import Console

console = Console()

def main():
    # Cargar tareas desde el archivo JSON
    tasks = load_tasks()
    
    # Mensaje de depuración para verificar que las tareas se cargaron
    if not tasks:
        print("No se encontraron tareas en tasks.json. La lista está vacía.")
    else:
        print(f"Se cargaron {len(tasks)} tareas desde tasks.json.")

    while True:
        # Mostrar el panel de bienvenida
        show_welcome_panel()
        
        # Siempre mostramos las tareas al inicio del bucle
        show_tasks(tasks, sort_by="priority")
        
        # Mostrar el menú y obtener la opción del usuario
        choice = show_menu()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            complete_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            # Pedir al usuario que elija el tipo de filtro o ordenamiento
            filter_choice = Prompt.ask(
                "Filtrar u ordenar tareas (completadas, pendientes, todas, prioridad)",
                choices=["completadas", "pendientes", "todas", "prioridad"],
                default="todas"
            )
            # Mapear la elección del usuario al valor esperado
            if filter_choice == "completadas":
                filtered_tasks = filter_tasks(tasks, "completed")
                show_tasks(filtered_tasks, sort_by="priority")
            elif filter_choice == "pendientes":
                filtered_tasks = filter_tasks(tasks, "pending")
                show_tasks(filtered_tasks, sort_by="priority")
            elif filter_choice == "todas":
                show_tasks(tasks, sort_by="priority")
            elif filter_choice == "prioridad":
                show_tasks(tasks, sort_by="priority")
            console.print("\n[bold cyan]Presione Enter para continuar...[/bold cyan]")
            Prompt.ask("")  # Esto espera a que el usuario presione Enter
        elif choice == "5":
            edit_task(tasks)
        elif choice == "6":
            search_tasks(tasks)
        elif choice == "7":
            export_tasks_to_csv(tasks)
            console.print("\n[bold cyan]Presione Enter para continuar...[/bold cyan]")
            Prompt.ask("")
        elif choice == "8":
            import_tasks_from_csv(tasks)
        elif choice == "9":
            break

        # Guardar las tareas después de cada operación
        save_tasks(tasks)

if __name__ == "__main__":
    main()