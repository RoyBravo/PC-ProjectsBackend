import sys
import json
import os
from datetime import datetime

# Nombre del archivo donde guardaremos las tareas
FILE_NAME = "tasks.json"

def load_tasks():
    """Carga las tareas desde el archivo JSON. Retorna una lista vacía si no existe."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return [] # Retorna lista vacía si el archivo está corrupto o vacío

def save_tasks(tasks):
    """Guarda la lista de tareas en el archivo JSON."""
    try:
        with open(FILE_NAME, 'w') as file:
            json.dump(tasks, file, indent=4)
    except IOError as e:
        print(f"Error al guardar las tareas: {e}")
def add_task(description):
    tasks = load_tasks()
    
    # Generar ID: si hay tareas, toma el ID más alto y suma 1, si no, es 1.
    new_id = tasks[-1]['id'] + 1 if tasks else 1
    
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    
    if not tasks:
        print("No hay tareas registradas.")
        return

    for task in tasks:
        if filter_status and task['status'] != filter_status:
            continue # Saltar si no coincide con el filtro
            
        print(f"[ID: {task['id']}] {task['description']} - [{task['status']}]")
        print(f"   Creado: {task['createdAt']}")


def update_task(task_id, new_description):
    tasks = load_tasks()
    task_found = False
    
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            task_found = True
            break
            
    if task_found:
        save_tasks(tasks)
        print(f"Task {task_id} updated successfully.")
    else:
        print(f"Task con ID {task_id} no encontrada.")

def delete_task(task_id):
    tasks = load_tasks()
    # Filtramos la lista manteniendo solo las tareas que NO tienen ese ID
    new_tasks = [t for t in tasks if t['id'] != task_id]
    
    if len(tasks) != len(new_tasks):
        save_tasks(new_tasks)
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Task con ID {task_id} no encontrada.")

def mark_task(task_id, new_status):
    tasks = load_tasks()
    task_found = False
    
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status
            task['updatedAt'] = datetime.now().isoformat()
            task_found = True
            break
            
    if task_found:
        save_tasks(tasks)
        print(f"Task {task_id} marked as {new_status}.")
    else:
        print(f"Task con ID {task_id} no encontrada.")

def main():
    if len(sys.argv) < 2:
        print("Uso: task-cli <command> [arguments]")
        return

    command = sys.argv[1]

    # Manejo de comandos
    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Debes proporcionar una descripción.")
        else:
            add_task(sys.argv[2])

    elif command == "update":
        if len(sys.argv) < 4:
            print("Error: Uso 'update <id> <nueva descripcion>'")
        else:
            # Convertimos el ID a entero
            try:
                update_task(int(sys.argv[2]), sys.argv[3])
            except ValueError:
                print("Error: El ID debe ser un número.")

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Uso 'delete <id>'")
        else:
            try:
                delete_task(int(sys.argv[2]))
            except ValueError:
                print("Error: El ID debe ser un número.")

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Error: Uso 'mark-in-progress <id>'")
        else:
            try:
                mark_task(int(sys.argv[2]), "in-progress")
            except ValueError:
                print("Error: El ID debe ser un número.")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Error: Uso 'mark-done <id>'")
        else:
            try:
                mark_task(int(sys.argv[2]), "done")
            except ValueError:
                print("Error: El ID debe ser un número.")

    elif command == "list":
        # Revisamos si hay un tercer argumento para filtrar
        if len(sys.argv) == 3:
            status = sys.argv[2]
            if status in ["done", "todo", "in-progress"]:
                list_tasks(status)
            else:
                print("Error: Estado inválido. Use 'done', 'todo', o 'in-progress'.")
        else:
            list_tasks()

    else:
        print(f"Comando desconocido: {command}")

if __name__ == "__main__":
    main()