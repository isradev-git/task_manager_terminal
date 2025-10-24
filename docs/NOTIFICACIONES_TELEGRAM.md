# 📱 NOTIFICACIONES POR TELEGRAM - Guía Completa

## 🎯 Sistema de Notificaciones Implementado

Has añadido un **sistema profesional de notificaciones** vía Telegram que te mantiene informado sobre todas tus tareas en tiempo real.

---

## ✨ Tipos de Notificaciones

### **1️⃣ Tarea Completada** 🎉
```
Cuándo: Al marcar una tarea como completada
Mensaje:
┌─────────────────────────────┐
│ 🎉 ¡Tarea Completada! 🎉    │
│                             │
│ 🔴 Proyecto Python          │
│                             │
│ ✅ Estado: Completada        │
│ 📊 Prioridad: Alta          │
│ 🍅 Pomodoros: 8             │
│                             │
│ ⏰ 24/10/2024 15:30         │
└─────────────────────────────┘
```

### **2️⃣ Tareas para Mañana** ⏰
```
Cuándo: Al iniciar la app (si hay tareas para mañana)
Mensaje:
┌─────────────────────────────┐
│ ⏰ Recordatorio: Tareas      │
│    para Mañana              │
│                             │
│ 📅 Tienes 3 tareas que      │
│    vencen mañana:           │
│                             │
│ 1. 🔴 Reunión cliente       │
│ 2. 🟡 Revisar código        │
│ 3. 🟢 Comprar materiales    │
│                             │
│ 💡 ¡Planifica tu día!       │
└─────────────────────────────┘
```

### **3️⃣ Tareas de Hoy** 🚨
```
Cuándo: Al iniciar la app (si hay tareas para hoy)
Mensaje:
┌─────────────────────────────┐
│ 🚨 ¡TAREAS PARA HOY! 🚨     │
│                             │
│ 📅 Tienes 2 tareas que      │
│    vencen HOY:              │
│                             │
│ 1. 🔴 Entregar proyecto     │
│ 2. 🟡 Llamar proveedor      │
│                             │
│ ⚡ ¡A trabajar!              │
└─────────────────────────────┘
```

### **4️⃣ Tareas Vencidas** ⚠️
```
Cuándo: Al iniciar la app (si hay tareas vencidas)
Mensaje:
┌─────────────────────────────┐
│ ⚠️ TAREAS VENCIDAS ⚠️        │
│                             │
│ 📛 Tienes 2 tareas que ya   │
│    vencieron:               │
│                             │
│ 1. 🔴 Pagar facturas        │
│    Vencida hace 3 días      │
│                             │
│ 2. 🟡 Renovar licencia      │
│    Vencida hace 1 día       │
│                             │
│ 🔥 ¡Atención urgente!       │
└─────────────────────────────┘
```

---

## 🔧 Configuración

### **Datos Pre-configurados:**
```
Bot Token: 8242520153:AAFAGHC88YFen6KnU6F6IioFWJyADgWz3Q8
Username Bot: @glitchbane_task_bot
Chat ID: 6009496370
Usuario: @glitchbane
Nombre: Isra
```

### **Configuración Automática:**
Al ejecutar la aplicación por primera vez, se crea automáticamente el archivo `telegram_config.json`:

```json
{
    "bot_token": "8242520153:AAFAGHC88YFen6KnU6F6IioFWJyADgWz3Q8",
    "chat_id": "6009496370",
    "username": "@glitchbane",
    "first_name": "Isra",
    "enabled": true,
    "notifications": {
        "task_completed": true,
        "task_tomorrow": true,
        "task_today": true,
        "task_overdue": true
    }
}
```

---

## 🎮 Uso del Sistema

### **Opción 13: Configurar Telegram**

```
╭──────────────────────────────╮
│ ⚙️  CONFIGURACIÓN DE TELEGRAM│
│                              │
│ Configura las notificaciones │
│ de tu gestor de tareas       │
╰──────────────────────────────╯

Configuración actual:
Bot Token: 8242520153:AAFAGH...
Chat ID: 6009496370
Usuario: @glitchbane
Estado: Habilitado

Opciones:
1. Probar conexión
2. Habilitar/Deshabilitar notificaciones
3. Configurar tipos de notificaciones
4. Enviar mensaje de prueba
5. Verificar tareas y enviar notificaciones ahora
0. Volver

Seleccione una opción:
```

### **Opción 1: Probar Conexión**
```
Probando conexión...
✅ Conexión exitosa con @glitchbane_task_bot
```

### **Opción 2: Habilitar/Deshabilitar**
```
✅ Notificaciones habilitadas
   o
⚠️  Notificaciones deshabilitadas
```

### **Opción 3: Configurar Tipos**
```
¿Notificar al completar tarea? (Y/n): y
¿Notificar tareas que vencen mañana? (Y/n): y
¿Notificar tareas que vencen hoy? (Y/n): y
¿Notificar tareas vencidas? (Y/n): y

✅ Configuración guardada
```

### **Opción 4: Mensaje de Prueba**
```
Enviando mensaje de prueba...
✅ Mensaje enviado correctamente
Revisa tu Telegram
```

### **Opción 5: Verificar Ahora**
```
Verificando tareas...
✅ Notificaciones enviadas
Revisa tu Telegram
```

---

## 🔄 Flujo Automático

### **Al Iniciar la Aplicación:**
```
1. python main.py
   ↓
2. Carga tareas desde tasks.json
   ↓
3. Verifica fechas límite
   ↓
4. Si hay tareas vencidas → Notificación ⚠️
   ↓
5. Si hay tareas para hoy → Notificación 🚨
   ↓
6. Si hay tareas para mañana → Notificación ⏰
   ↓
7. Muestra menú principal
```

### **Al Completar una Tarea:**
```
1. Opción 2 → Completar tarea
   ↓
2. Seleccionar tarea
   ↓
3. Marcar como completada
   ↓
4. Enviar notificación 🎉
   ↓
5. Mostrar mensaje confirmación
   ↓
6. "📱 Notificación enviada a Telegram"
```

---

## 🧠 Implementación Técnica

### **1. Módulo telegram_bot.py**

```python
import requests
import json

# Enviar mensaje básico
def send_telegram_message(message, parse_mode="HTML"):
    config = load_telegram_config()
    
    if not config.get("enabled", True):
        return False
    
    bot_token = config["bot_token"]
    chat_id = config["chat_id"]
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode
    }
    
    response = requests.post(url, json=payload, timeout=5)
    return response.status_code == 200
```

**¿Qué hace?**
1. Carga configuración desde JSON
2. Verifica si está habilitado
3. Construye URL de API de Telegram
4. Envía POST con mensaje
5. Retorna True si exitoso

### **2. Notificación de Tarea Completada**

```python
def notify_task_completed(task, pomodoros=0):
    config = load_telegram_config()
    
    # Verificar si este tipo está habilitado
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
    
    # Construir mensaje con HTML
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
```

**Tags HTML soportados:**
- `<b>texto</b>` - Negrita
- `<i>texto</i>` - Cursiva
- `<code>texto</code>` - Código
- `<pre>texto</pre>` - Preformateado

### **3. Verificación Diaria de Tareas**

```python
def check_and_send_daily_notifications(tasks):
    from datetime import date, timedelta
    
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
            
            # Clasificar por fecha
            if deadline_date == tomorrow:
                tasks_tomorrow.append(task)
            elif deadline_date == today:
                tasks_today.append(task)
            elif deadline_date < today:
                tasks_overdue.append(task)
        except:
            continue
    
    # Enviar notificaciones (prioridad: vencidas > hoy > mañana)
    if tasks_overdue:
        notify_tasks_overdue(tasks_overdue)
    
    if tasks_today:
        notify_tasks_today(tasks_today)
    
    if tasks_tomorrow:
        notify_tasks_tomorrow(tasks_tomorrow)
```

**Orden de prioridad:**
1. **Vencidas** (más urgente)
2. **Hoy** (urgente)
3. **Mañana** (recordatorio)

### **4. Integración en main.py**

```python
# Al iniciar
def main():
    tasks = load_tasks()
    
    # Verificar y notificar
    try:
        check_and_send_daily_notifications(tasks)
    except:
        pass  # Si falla, continuar
```

```python
# Al completar tarea (en task_manager.py)
tasks[original_index]["completed"] = True

# Notificar
try:
    from telegram_bot import notify_task_completed
    pomodoros = task_to_complete.get("pomodoros_completed", 0)
    notify_task_completed(task_to_complete, pomodoros)
except:
    pass
```

---

## 🔐 Seguridad y Privacidad

### **Archivo telegram_config.json:**
```
⚠️  IMPORTANTE:
- Este archivo contiene tu Bot Token
- NO lo compartas públicamente
- NO lo subas a GitHub sin .gitignore
- Guárdalo de forma segura
```

### **Añadir a .gitignore:**
```bash
# Archivo .gitignore
telegram_config.json
*.json
```

### **¿Cómo funciona el Bot Token?**
```
Bot Token = Contraseña del bot
Chat ID = Tu identificador único

Bot Token + Chat ID = Permiso para enviar mensajes a TI
```

**Nadie más puede:**
- Ver tus mensajes
- Recibir tus notificaciones
- Acceder a tu información

---

## 📊 API de Telegram Bot

### **Endpoints Utilizados:**

**1. Enviar Mensaje:**
```
POST https://api.telegram.org/bot{TOKEN}/sendMessage
Body: {
    "chat_id": "6009496370",
    "text": "Mensaje",
    "parse_mode": "HTML"
}
```

**2. Obtener Info del Bot:**
```
GET https://api.telegram.org/bot{TOKEN}/getMe
Response: {
    "ok": true,
    "result": {
        "username": "glitchbane_task_bot",
        "first_name": "TaskBot"
    }
}
```

### **Parse Modes:**

**HTML (usado):**
```html
<b>Negrita</b>
<i>Cursiva</i>
<code>Código</code>
```

**Markdown:**
```markdown
*Negrita*
_Cursiva_
`Código`
```

---

## 💡 Conceptos Técnicos Aprendidos

### **1. Requests (HTTP en Python)**

```python
import requests

# GET request
response = requests.get("https://api.example.com/data")

# POST request
response = requests.post(
    "https://api.example.com/send",
    json={"key": "value"},
    timeout=5
)

# Verificar respuesta
if response.status_code == 200:
    data = response.json()
```

**Status Codes:**
- 200: OK (éxito)
- 400: Bad Request (solicitud incorrecta)
- 401: Unauthorized (sin autorización)
- 404: Not Found (no encontrado)
- 500: Server Error (error del servidor)

### **2. Try-Except para Robustez**

```python
# Sin try-except (frágil)
def send_message(msg):
    response = requests.post(url, json=msg)
    return response.status_code == 200
# Si falla requests, programa crashea

# Con try-except (robusto)
def send_message(msg):
    try:
        response = requests.post(url, json=msg, timeout=5)
        return response.status_code == 200
    except requests.exceptions.Timeout:
        print("Timeout")
        return False
    except requests.exceptions.ConnectionError:
        print("Sin conexión")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
# Si falla, maneja el error gracefully
```

### **3. Configuración con JSON**

```python
# Guardar configuración
config = {
    "bot_token": "...",
    "enabled": True
}

with open("config.json", "w") as f:
    json.dump(config, f, indent=4)

# Cargar configuración
with open("config.json", "r") as f:
    config = json.load(f)
```

**Ventajas de JSON:**
- Legible por humanos
- Fácil de editar
- Compatible con todos los lenguajes
- Estructura flexible

### **4. Timedelta (Operaciones con Fechas)**

```python
from datetime import date, timedelta

today = date.today()
tomorrow = today + timedelta(days=1)
yesterday = today - timedelta(days=1)

# Comparaciones
if deadline_date == tomorrow:
    print("Vence mañana")
elif deadline_date < today:
    print("Vencida")
```

---

## 🎯 Casos de Uso

### **Caso 1: Recordatorio Matutino**
```
Situación: 7:00 AM, abres la app

Sistema verifica:
- 3 tareas para hoy
- 2 tareas para mañana
- 1 tarea vencida

Recibes 3 notificaciones en Telegram:
1. ⚠️  "Tareas vencidas" (más urgente)
2. 🚨 "Tareas para hoy"
3. ⏰ "Tareas para mañana"

Resultado: Empiezas el día informado
```

### **Caso 2: Trabajo Remoto**
```
Situación: Trabajando desde casa

Completas tarea en la app
↓
Notificación instantánea en Telegram
↓
Puedes verificar en el móvil sin abrir la app
↓
Sensación de logro inmediato
```

### **Caso 3: Equipo Colaborativo**
```
Situación: Múltiples personas usan la misma app

Cada persona tiene su:
- Bot propio
- Chat ID único
- Notificaciones personales

Ventaja: Privacidad y personalización
```

---

## 🚀 Testing

### **Test 1: Conexión del Bot**
```bash
1. python main.py
2. Opción 13 → Configurar Telegram
3. Opción 1 → Probar conexión
4. Verificar: "✅ Conexión exitosa con @glitchbane_task_bot"
```

### **Test 2: Mensaje de Prueba**
```bash
1. Opción 13 → Configurar Telegram
2. Opción 4 → Enviar mensaje de prueba
3. Abrir Telegram en el móvil
4. Verificar: Mensaje recibido del bot
```

### **Test 3: Notificación al Completar**
```bash
1. Crear una tarea
2. Opción 2 → Completar tarea
3. Seleccionar la tarea
4. Verificar en consola: "📱 Notificación enviada"
5. Verificar en Telegram: "🎉 ¡Tarea Completada!"
```

### **Test 4: Notificaciones Diarias**
```bash
1. Crear tareas con fechas:
   - 1 para hoy
   - 1 para mañana
   - 1 vencida (ayer)
2. Cerrar y volver a abrir la app
3. Verificar: 3 notificaciones en Telegram
```

### **Test 5: Habilitar/Deshabilitar**
```bash
1. Opción 13 → Opción 2 → Deshabilitar
2. Completar una tarea
3. Verificar: NO llega notificación
4. Opción 13 → Opción 2 → Habilitar
5. Completar otra tarea
6. Verificar: SÍ llega notificación
```

---

## 🎉 Resultado

Has implementado un **sistema completo de notificaciones** con:

1. ✅ **4 tipos de notificaciones** diferentes
2. ✅ **Configuración flexible** por tipo
3. ✅ **Verificación automática** al iniciar
4. ✅ **Notificación inmediata** al completar
5. ✅ **Interfaz de configuración** completa
6. ✅ **Manejo de errores** robusto
7. ✅ **Mensajes con formato** HTML
8. ✅ **Priorización inteligente** de notificaciones

**¡Tu gestor de tareas ahora te mantiene informado en todo momento!** 🚀

---

## 📚 Próximas Mejoras Posibles

- Comandos en el bot (responder mensajes)
- Crear tareas desde Telegram
- Ver lista de tareas desde Telegram
- Notificaciones programadas (8 AM diario)
- Estadísticas semanales por Telegram
- Integración con otros servicios (Slack, Discord)

¿Cuál te gustaría implementar? 😊