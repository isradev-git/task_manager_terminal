from task_manager import load_tasks, save_tasks, add_task, complete_task, delete_task, filter_tasks, search_tasks, export_tasks_to_csv, import_tasks_from_csv
from ui import show_menu, show_tasks, show_welcome_panel

def main():
    # Cargar tareas desde el archivo JSON
    tasks = load_tasks()

    while True:
        # Mostrar el panel de bienvenida y el menú principal
        show_welcome_panel()
        choice = show_menu()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            complete_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            filtered_tasks = filter_tasks(tasks)
            show_tasks(filtered_tasks)
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