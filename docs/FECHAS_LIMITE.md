# 📅 GUÍA: Nueva Funcionalidad de Fechas Límite

## ✨ Cambios Implementados

### 1. **Estructura de Datos Actualizada**

Antes, cada tarea tenía:
```python
{
    "description": "Descripción de la tarea",
    "completed": False,
    "priority": "alta"
}
```

Ahora incluye la fecha límite:
```python
{
    "description": "Descripción de la tarea",
    "completed": False,
    "priority": "alta",
    "deadline": "25/12/2024"  # Nuevo campo (puede ser None)
}
```

---

## 📝 Explicación de los Cambios en `task_manager.py`

### **Nueva Función: `validate_date()`**

```python
def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%d/%m/%Y")
        return True
    except ValueError:
        return False
```

**¿Qué hace?**
- Verifica que la fecha ingresada tenga el formato correcto: DD/MM/YYYY
- Usa `datetime.strptime()` para convertir el texto en una fecha
- Si la conversión falla (fecha inválida), retorna False
- Ejemplo: "25/12/2024" → ✅ Válida | "32/13/2024" → ❌ Inválida

**¿Por qué es importante?**
Evita que el usuario ingrese fechas incorrectas como "99/99/9999" o "abc/def/ghij"

---

### **Función Modificada: `add_task()`**

**Cambios principales:**

1. **Pregunta si quiere añadir fecha límite:**
```python
add_deadline = Prompt.ask("¿Desea añadir una fecha límite? (s/n)", choices=["s", "n"], default="n")
```

2. **Bucle de validación:**
```python
while True:
    deadline_input = Prompt.ask("Ingrese la fecha límite (DD/MM/YYYY)")
    if validate_date(deadline_input):
        deadline = deadline_input
        break  # Sale del bucle si la fecha es válida
    else:
        console.print("[bold red]Formato de fecha inválido...[/bold red]")
```

**¿Cómo funciona el bucle?**
- Sigue pidiendo la fecha hasta que el usuario ingrese una válida
- No permite continuar con fechas incorrectas
- Esto garantiza la integridad de los datos

3. **Guarda la fecha en la tarea:**
```python
tasks.append({
    "description": description,
    "completed": False,
    "priority": priority,
    "deadline": deadline  # Puede ser None si no añadió fecha
})
```

---

### **Función Modificada: `edit_task()`**

**Nueva opción en el menú de edición:**
```
¿Qué desea editar?
1. Descripción
2. Prioridad
3. Estado (completada/pendiente)
4. Fecha límite  ← NUEVO
```

**Lógica para editar fecha límite:**

```python
elif edit_choice == "4":
    current_deadline = tasks[original_index].get("deadline", "Sin fecha")
    
    if current_deadline and current_deadline != "Sin fecha":
        # Si ya tiene fecha, puede modificar o eliminar
        action = Prompt.ask("¿Qué desea hacer?", choices=["modificar", "eliminar"])
    else:
        # Si no tiene fecha, permite añadir una nueva
```

**¿Qué hace `.get("deadline", "Sin fecha")`?**
- Busca el campo "deadline" en la tarea
- Si no existe, retorna "Sin fecha" como valor por defecto
- Evita errores si la tarea no tiene el campo

---

### **Funciones Actualizadas: Exportar/Importar CSV**

**En `export_tasks_to_csv()`:**
```python
writer.writerow(["ID", "Descripción", "Estado", "Prioridad", "Fecha Límite"])
for idx, task in enumerate(tasks, start=1):
    writer.writerow([
        idx,
        task["description"],
        task["completed"],
        task.get("priority", "N/A"),
        task.get("deadline", "Sin fecha")  # Nueva columna
    ])
```

**En `import_tasks_from_csv()`:**
```python
deadline = row.get("Fecha Límite", "Sin fecha")
if deadline == "Sin fecha":
    deadline = None  # Convertimos a None para mantener consistencia
```

---

## 🎨 Explicación de los Cambios en `ui.py`

### **Nueva Función: `is_overdue()`**

```python
def is_overdue(deadline_str):
    if not deadline_str:
        return False  # Si no hay fecha, no está vencida
    
    deadline = datetime.strptime(deadline_str, "%d/%m/%Y")
    today = datetime.now()
    return deadline.date() < today.date()  # Compara solo fechas, sin hora
```

**¿Cómo funciona?**
1. Convierte el string "25/12/2024" a un objeto fecha
2. Obtiene la fecha actual
3. Compara: si la fecha límite es menor que hoy → está vencida

**Ejemplo:**
- Hoy: 23/10/2024
- Fecha límite: 20/10/2024 → `is_overdue()` retorna True ⚠️
- Fecha límite: 30/10/2024 → `is_overdue()` retorna False ✅

---

### **Nueva Función: `is_deadline_soon()`**

```python
def is_deadline_soon(deadline_str):
    deadline = datetime.strptime(deadline_str, "%d/%m/%Y")
    today = datetime.now()
    days_until_deadline = (deadline.date() - today.date()).days
    return 0 <= days_until_deadline <= 3
```

**¿Qué calcula?**
- Resta la fecha actual de la fecha límite
- Obtiene el número de días que faltan
- Si faltan entre 0 y 3 días → está próxima a vencer

**Ejemplo:**
- Hoy: 23/10/2024
- Fecha límite: 25/10/2024 → Faltan 2 días → `is_deadline_soon()` = True ⏰
- Fecha límite: 30/10/2024 → Faltan 7 días → `is_deadline_soon()` = False

---

### **Nueva Función: `format_deadline()`**

```python
def format_deadline(deadline_str, completed):
    if not deadline_str:
        return "[dim]Sin fecha[/dim]"  # Gris y tenue
    
    if completed:
        return f"[green]{deadline_str}[/green]"  # Verde si está completada
    
    if is_overdue(deadline_str):
        return f"[red bold blink]⚠ {deadline_str} ⚠[/red bold blink]"  # ¡ALERTA!
    
    if is_deadline_soon(deadline_str):
        return f"[yellow bold]⏰ {deadline_str}[/yellow bold]"  # Advertencia
    
    return f"[white]{deadline_str}[/white]"  # Normal
```

**Sistema de colores y símbolos:**
- 🔴 Rojo parpadeante + ⚠️ = Tarea vencida (urgente)
- 🟡 Amarillo + ⏰ = Vence pronto (3 días o menos)
- 🟢 Verde = Tarea completada (tranquilo)
- ⚪ Blanco = Fecha normal
- Gris = Sin fecha límite

---

### **Función Modificada: `show_tasks()`**

**Nueva columna en la tabla:**
```python
table.add_column("Fecha Límite", justify="center", style="white", width=20)
```

**Aplicación de estilos según estado:**
```python
# Si la tarea está vencida y no completada, usamos estilo de advertencia
if is_overdue(deadline) and not task["completed"]:
    row_style = THEME["overdue"]  # Toda la fila en rojo
```

**Leyenda al final de la tabla:**
```python
console.print("\n[dim]Leyenda:[/dim]")
console.print("[dim]⚠ = Tarea vencida | ⏰ = Vence pronto (3 días o menos)[/dim]")
```

---

## 🚀 Cómo Usar la Nueva Funcionalidad

### **1. Agregar una tarea con fecha límite:**

```
Opciones:
1. Agregar tarea

> Ingrese la descripción de la tarea: Entregar proyecto final
> Ingrese la prioridad (alta, media, baja): alta
> ¿Desea añadir una fecha límite? (s/n): s
> Ingrese la fecha límite (DD/MM/YYYY): 30/12/2024

✅ Tarea agregada correctamente
```

### **2. Agregar tarea sin fecha límite:**

```
> ¿Desea añadir una fecha límite? (s/n): n

✅ Tarea agregada correctamente
```

### **3. Editar fecha límite de una tarea:**

```
Opciones:
5. Editar tarea

> Ingrese el ID de la tarea a editar: 1

¿Qué desea editar?
1. Descripción
2. Prioridad
3. Estado (completada/pendiente)
4. Fecha límite

> Seleccione una opción: 4

Fecha límite actual: 30/12/2024

> ¿Qué desea hacer? (modificar/eliminar): modificar
> Ingrese la nueva fecha límite (DD/MM/YYYY): 15/01/2025

✅ Fecha límite actualizada correctamente
```

---

## 📊 Visualización de Tareas

### **Ejemplo de tabla con fechas límite:**

```
╭─────────────────── Gestor de Tareas ───────────────────╮
│ ID │ Tarea                │ Estado │ Prioridad │ Fecha Límite        │
├────┼──────────────────────┼────────┼───────────┼─────────────────────┤
│ 1  │ Entregar proyecto    │ [ ]    │ alta      │ ⚠ 20/10/2024 ⚠     │  ← VENCIDA
│ 2  │ Reunión con cliente  │ [ ]    │ media     │ ⏰ 25/10/2024       │  ← VENCE PRONTO
│ 3  │ Revisar código       │ [ ]    │ baja      │ 30/11/2024          │  ← FECHA NORMAL
│ 4  │ Documentar API       │ [✓]    │ media     │ 15/10/2024          │  ← COMPLETADA
│ 5  │ Pruebas unitarias    │ [ ]    │ alta      │ Sin fecha           │  ← SIN FECHA
╰────┴──────────────────────┴────────┴───────────┴─────────────────────╯

Leyenda:
⚠ = Tarea vencida | ⏰ = Vence pronto (3 días o menos)
```

---

## 🔧 Conceptos de Programación Utilizados

### **1. Validación de Entrada**
- Se asegura de que los datos sean correctos antes de guardarlos
- Evita errores futuros en el programa

### **2. Manejo de Excepciones**
- `try/except` para capturar errores de conversión de fechas
- El programa no se rompe si hay un error

### **3. Valores por Defecto**
- `.get("deadline", "Sin fecha")` proporciona un valor si no existe el campo
- Hace el código más robusto

### **4. Lógica Condicional**
- Múltiples `if/elif/else` para decidir el formato de la fecha
- Prioriza los casos más urgentes (vencida > próxima > normal)

### **5. Comparación de Fechas**
- Uso de `datetime` para operaciones matemáticas con fechas
- `.days` obtiene la diferencia en días entre dos fechas

### **6. Formato Rico de Texto**
- Colores, negritas, parpadeo usando markup de Rich
- Mejora la experiencia visual del usuario

---

## ✅ Compatibilidad con Datos Antiguos

**¿Qué pasa con las tareas que ya existían?**

Las tareas antiguas (sin fecha límite) seguirán funcionando porque:

1. Usamos `.get("deadline", "Sin fecha")` en lugar de `task["deadline"]`
2. Si el campo no existe, se muestra como "Sin fecha"
3. No genera errores

**Ejemplo:**
```python
# Tarea antigua (sin deadline)
{
    "description": "Tarea vieja",
    "completed": False,
    "priority": "media"
}

# Al leerla, la función .get() retorna "Sin fecha" automáticamente
```

---

## 🎯 Próximas Mejoras Sugeridas

1. **Ordenar por fecha límite:** Mostrar primero las tareas más urgentes
2. **Notificaciones:** Alertar cuando una tarea esté por vencer
3. **Estadísticas:** Cuántas tareas vencidas, completadas a tiempo, etc.
4. **Filtrar por rango de fechas:** Ver tareas de esta semana, este mes, etc.
5. **Fechas de creación:** Saber cuándo se creó cada tarea
6. **Tiempo estimado:** Añadir cuánto tiempo tomará cada tarea

---

## 📦 Archivos Modificados

- ✅ `task_manager.py` - Lógica de fechas límite
- ✅ `ui.py` - Visualización con indicadores
- ✅ Los archivos `main.py` y `__init__.py` no necesitan cambios

---

## 🧪 Cómo Probar

1. **Reemplaza** los archivos `task_manager.py` y `ui.py` con las nuevas versiones
2. **Ejecuta** `python main.py`
3. **Prueba** estas acciones:
   - Agregar tarea con fecha
   - Agregar tarea sin fecha
   - Editar fecha de una tarea existente
   - Ver cómo se muestran las fechas vencidas
   - Exportar/importar tareas con fechas

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo usar otro formato de fecha?**
R: Sí, pero deberás cambiar `"%d/%m/%Y"` en todas las funciones por el formato deseado.

**P: ¿Las tareas antiguas funcionarán?**
R: Sí, totalmente compatible. Se mostrarán como "Sin fecha".

**P: ¿Puedo poner fechas en el pasado?**
R: Sí, el sistema lo permite. Se marcarán como vencidas automáticamente.

**P: ¿Qué pasa si completo una tarea vencida?**
R: Se marcará como completada y la fecha se mostrará en verde (ya no parpadeará en rojo).

---

¡Disfruta de la nueva funcionalidad! 🎉