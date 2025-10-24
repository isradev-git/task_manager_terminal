# 🎯 NUEVO SISTEMA DE ORDENAMIENTO INTELIGENTE

## ✨ ¿Qué Cambió?

Ahora tu Gestor de Tareas ordena **AUTOMÁTICAMENTE** todas las tareas usando un sistema de doble criterio:

### 📊 Criterio de Ordenamiento:

1. **Primer criterio: PRIORIDAD**
   - Alta → Media → Baja

2. **Segundo criterio: FECHA LÍMITE** (dentro de cada prioridad)
   - Más cercanas primero → Más lejanas después → Sin fecha al final

---

## 🔍 Ejemplo Visual

### **Antes (solo por prioridad):**
```
┌──────────────────────────────────────────────┐
│ 1. [Alta] Tarea sin fecha                    │
│ 2. [Alta] Tarea vence en 30 días             │
│ 3. [Alta] Tarea vence mañana ⚠️              │
│ 4. [Media] Tarea vence en 2 días             │
│ 5. [Baja] Tarea vence hoy ⚠️                 │
└──────────────────────────────────────────────┘
```
❌ Problema: Las tareas urgentes de baja prioridad quedan al final

### **Ahora (prioridad + fecha límite):**
```
┌──────────────────────────────────────────────┐
│ 1. [Alta] Tarea vence mañana ⚠️              │ ← ¡Urgente!
│ 2. [Alta] Tarea vence en 30 días             │
│ 3. [Alta] Tarea sin fecha                    │
│ 4. [Media] Tarea vence en 2 días ⏰          │
│ 5. [Baja] Tarea vence hoy ⚠️                 │ ← Baja prioridad pero urgente
└──────────────────────────────────────────────┘
```
✅ Mejor: Dentro de cada prioridad, las más urgentes aparecen primero

---

## 🧠 ¿Cómo Funciona el Código?

### **Nueva Función: `get_days_until_deadline()`**

```python
def get_days_until_deadline(deadline_str):
    if not deadline_str:
        return float('inf')  # Infinito = va al final
    
    deadline = datetime.strptime(deadline_str, "%d/%m/%Y")
    today = datetime.now()
    days_difference = (deadline.date() - today.date()).days
    return days_difference
```

**¿Qué hace esta función?**

Convierte cada fecha en un número que representa los días hasta la fecha límite:

| Fecha Límite | Días hasta la fecha | Resultado |
|--------------|---------------------|-----------|
| 20/10/2024 (vencida) | -3 días | `-3` (número negativo) |
| Hoy | 0 días | `0` |
| 25/10/2024 | +2 días | `+2` |
| 30/12/2024 | +68 días | `+68` |
| Sin fecha | N/A | `infinito` |

**¿Por qué usar `float('inf')` (infinito)?**
- Cuando ordenamos números, los más pequeños van primero
- Al poner `infinito` para las tareas sin fecha, garantizamos que vayan al final
- Ejemplo: `-3 < 0 < 2 < 68 < infinito`

---

### **Nueva Función: `sort_tasks_by_priority_and_deadline()`**

```python
def sort_tasks_by_priority_and_deadline(tasks):
    priority_order = {"alta": 1, "media": 2, "baja": 3}
    
    sorted_tasks = sorted(
        tasks,
        key=lambda task: (
            priority_order.get(task.get("priority", "baja"), 4),
            get_days_until_deadline(task.get("deadline"))
        )
    )
    
    return sorted_tasks
```

**Explicación detallada:**

#### 1. **Diccionario de prioridades:**
```python
priority_order = {"alta": 1, "media": 2, "baja": 3}
```
- Convierte las prioridades en números
- Menor número = mayor prioridad

#### 2. **La función `sorted()`:**
```python
sorted_tasks = sorted(tasks, key=...)
```
- `sorted()` ordena una lista
- `key=` especifica CÓMO ordenar

#### 3. **La función lambda:**
```python
key=lambda task: (prioridad, días)
```
- `lambda` es una función anónima pequeña
- `task` es cada tarea de la lista
- Retorna una **tupla** `(prioridad, días)`

#### 4. **Ordenamiento por tupla:**
Python ordena tuplas comparando elemento por elemento:
```python
(1, -3) < (1, 5) < (1, 68) < (2, 0) < (3, 10)
 ↑       ↑        ↑         ↑        ↑
Alta    Alta     Alta      Media    Baja
-3 días 5 días   68 días   hoy      10 días
```

**Proceso paso a paso:**
1. Compara el primer elemento (prioridad): `1 < 2 < 3`
2. Si son iguales, compara el segundo elemento (días): `-3 < 0 < 5 < 68`

---

## 📝 Ejemplo Práctico Completo

### **Tareas de entrada (sin ordenar):**

```python
tasks = [
    {"description": "Limpiar casa", "priority": "baja", "deadline": "24/10/2024"},
    {"description": "Entregar proyecto", "priority": "alta", "deadline": "22/10/2024"},
    {"description": "Comprar comida", "priority": "media", "deadline": None},
    {"description": "Llamar cliente", "priority": "alta", "deadline": "30/12/2024"},
    {"description": "Revisar email", "priority": "media", "deadline": "23/10/2024"},
]
```

### **Procesamiento:**

Supongamos que hoy es **23/10/2024**

| Tarea | Prioridad | Prioridad (num) | Fecha | Días | Tupla resultante |
|-------|-----------|-----------------|-------|------|------------------|
| Entregar proyecto | alta | 1 | 22/10/2024 | -1 | `(1, -1)` |
| Llamar cliente | alta | 1 | 30/12/2024 | 68 | `(1, 68)` |
| Revisar email | media | 2 | 23/10/2024 | 0 | `(2, 0)` |
| Comprar comida | media | 2 | Sin fecha | ∞ | `(2, ∞)` |
| Limpiar casa | baja | 3 | 24/10/2024 | 1 | `(3, 1)` |

### **Orden final:**

```
1. (1, -1)  → [Alta] Entregar proyecto - 22/10/2024 ⚠️ (VENCIDA)
2. (1, 68)  → [Alta] Llamar cliente - 30/12/2024
3. (2, 0)   → [Media] Revisar email - 23/10/2024 ⏰ (HOY)
4. (2, ∞)   → [Media] Comprar comida - Sin fecha
5. (3, 1)   → [Baja] Limpiar casa - 24/10/2024 ⏰ (MAÑANA)
```

---

## 🔄 Cambios en las Funciones

### **Función `show_tasks()` - Ahora más simple:**

**Antes:**
```python
def show_tasks(tasks, sort_by=None):
    if sort_by == "priority":
        priority_order = {"alta": 1, "media": 2, "baja": 3}
        tasks = sorted(tasks, key=lambda x: priority_order.get(...))
    # ... mostrar tabla
```

**Ahora:**
```python
def show_tasks(tasks, sort_by=None):
    # SIEMPRE usa el ordenamiento inteligente
    sorted_tasks = sort_tasks_by_priority_and_deadline(tasks)
    # ... mostrar tabla
```

**¿Qué cambió?**
- Ya no necesitamos el parámetro `sort_by`
- Siempre se ordena de la misma manera inteligente
- El código es más simple y consistente

---

### **Funciones Actualizadas en `task_manager.py`:**

Todas estas funciones ahora usan el ordenamiento inteligente:

#### **1. `complete_task()`**
```python
# Importamos la función de ordenamiento
from ui import sort_tasks_by_priority_and_deadline

# Mostramos las tareas (ya ordenadas automáticamente)
show_tasks(tasks)

# Obtenemos la lista ordenada para saber qué tarea eligió el usuario
sorted_tasks = sort_tasks_by_priority_and_deadline(tasks)
```

#### **2. `delete_task()`**
```python
# Mismo proceso
show_tasks(tasks)
sorted_tasks = sort_tasks_by_priority_and_deadline(tasks)
```

#### **3. `edit_task()`**
```python
# Mismo proceso
show_tasks(tasks)
sorted_tasks = sort_tasks_by_priority_and_deadline(tasks)
```

**¿Por qué necesitamos `sorted_tasks`?**
- Cuando el usuario selecciona "ID 1", necesitamos saber qué tarea es
- El ID mostrado corresponde a la posición en la lista **ordenada**
- Pero necesitamos modificar la lista **original** (no ordenada)
- Por eso usamos `tasks.index(task_to_edit)` para encontrarla

---

## 🎯 Ventajas del Nuevo Sistema

### ✅ **Siempre Consistente**
- Las tareas siempre aparecen en el mismo orden lógico
- No importa cuándo las agregaste

### ✅ **Visualmente Intuitivo**
- Las tareas más urgentes de cada prioridad están arriba
- Las que vencen pronto están destacadas con ⏰
- Las vencidas parpadean en rojo ⚠️

### ✅ **Automático**
- No necesitas seleccionar cómo ordenar
- El sistema elige el mejor orden por ti

### ✅ **Flexible**
- Si una tarea no tiene fecha, va al final de su prioridad
- Si todas tienen la misma prioridad, se ordenan solo por fecha

---

## 📚 Conceptos de Python Que Aprendiste

### 1. **Función `sorted()` con key**
```python
sorted(lista, key=funcion)
```
- Ordena una lista según una función
- La función `key` decide CÓMO comparar elementos

### 2. **Funciones Lambda**
```python
lambda x: x.get("priority")
```
- Función anónima de una sola línea
- Útil para operaciones simples

### 3. **Tuplas para Ordenamiento Múltiple**
```python
key=lambda x: (criterio1, criterio2)
```
- Python compara elemento por elemento
- Perfecto para ordenar por múltiples criterios

### 4. **`float('inf')` (Infinito)**
```python
float('inf') > cualquier_numero
```
- Representa infinito matemático
- Útil para forzar elementos al final

### 5. **Método `.index()`**
```python
original_index = tasks.index(elemento)
```
- Encuentra la posición de un elemento en una lista
- Retorna el primer índice donde aparece

### 6. **Import Selectivo**
```python
from ui import sort_tasks_by_priority_and_deadline
```
- Importa solo una función específica de un módulo
- Evita importar todo el módulo

---

## 🧪 Prueba el Nuevo Ordenamiento

### **Escenario de Prueba:**

1. **Crea estas tareas:**
   ```
   - "Proyecto urgente" - Alta - 25/10/2024
   - "Comprar leche" - Baja - 24/10/2024
   - "Reunión equipo" - Media - 26/10/2024
   - "Leer libro" - Alta - Sin fecha
   - "Pagar facturas" - Alta - 23/10/2024
   ```

2. **Orden esperado (hoy: 23/10/2024):**
   ```
   1. [Alta] Pagar facturas - 23/10/2024 ⏰ (Hoy)
   2. [Alta] Proyecto urgente - 25/10/2024 ⏰ (2 días)
   3. [Alta] Leer libro - Sin fecha
   4. [Media] Reunión equipo - 26/10/2024 ⏰ (3 días)
   5. [Baja] Comprar leche - 24/10/2024 ⏰ (Mañana)
   ```

---

## 📊 Comparación: Antes vs Ahora

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Criterio principal** | Solo prioridad | Prioridad + Fecha |
| **Tareas sin fecha** | Mezcladas | Al final de cada prioridad |
| **Tareas urgentes** | Podían quedar abajo | Siempre destacadas |
| **Consistencia** | Variable según filtro | Siempre igual |
| **Código** | Duplicado en varias funciones | Centralizado en 1 función |

---

## 🎉 Resumen

Has implementado un **sistema de ordenamiento inteligente** que:

1. ✅ Ordena por **prioridad** primero (alta → baja)
2. ✅ Dentro de cada prioridad, ordena por **fecha límite** (cercanas → lejanas)
3. ✅ Tareas sin fecha van al **final** de cada prioridad
4. ✅ Es **automático** y **consistente** en toda la aplicación
5. ✅ Usa conceptos avanzados de Python como tuplas, lambda, e infinito

**¡Tu gestor de tareas ahora es mucho más inteligente!** 🚀

---

## 💡 Próximos Pasos Sugeridos

1. **Agregar contador de días**: Mostrar "Vence en 5 días" en lugar de solo la fecha
2. **Separadores visuales**: Líneas entre prioridades diferentes
3. **Resaltar grupo actual**: Mostrar claramente qué prioridad estás viendo
4. **Ordenamiento alternativo**: Opción para ordenar solo por fecha (todas las prioridades juntas)

¿Te gustaría implementar alguna de estas? 😊