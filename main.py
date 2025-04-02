from task_manager import load_tasks, save_tasks, add_task, complete_task, delete_task, filter_tasks, search_tasks, export_tasks_to_csv, import_tasks_from_csv
from ui import show_menu, show_tasks, show_welcome_panel
from rich.prompt import Prompt
from rich.console import Console  # Añadimos esta importación para usar Console

console = Console()  # Creamos una instancia de Console para usar print

def main():
    # Cargar tareas desde el archivo JSON
    tasks = load_tasks()
    
    # Mensaje de depuración para verificar que las tareas se cargaron
    if not tasks:
        print("No se encontraron tareas en tasks.json. La lista está vacía.")
    else:
        print(f"Se cargaron {len(tasks)} tareas desde tasks.json.")

    while True:
        # Mostrar el panel de bienvenida y el menú principal
        show_welcome_panel()
        
        # Mostrar las tareas antes de pedir una opción
        show_tasks(tasks)
        
        choice = show_menu()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            complete_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            # Pedir al usuario que elija el tipo de filtro
            filter_choice = Prompt.ask(
                "Filtrar tareas por estado (completadas, pendientes, todas)",
                choices=["completadas", "pendientes", "todas"],
                default="todas"
            )
            # Mapear la elección del usuario al valor esperado por filter_tasks
            status = None
            if filter_choice == "completadas":
                status = "completed"
            elif filter_choice == "pendientes":
                status = "pending"
            # Si elige "todas", status sigue siendo None, lo que mostrará todas las tareas
            filtered_tasks = filter_tasks(tasks, status)
            show_tasks(filtered_tasks)
            # Añadir una pausa para que el usuario pueda ver las tareas filtradas
            console.print("\n[bold cyan]Presione Enter para continuar...[/bold cyan]")
            Prompt.ask("")  # Esto espera a que el usuario presione Enter
        elif choice == "5":
            search_tasks(tasks)
        elif choice == "6":
            export_tasks_to_csv(tasks)
        elif choice == "7":
            import_tasks_from_csv(tasks)
        elif choice == "8":
            break

        # Guardar las tareas después de cada operación
        save_tasks(tasks)

if __name__ == "__main__":
    main()