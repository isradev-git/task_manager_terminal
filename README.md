# 📋 Task Manager Terminal

Gestor de tareas para terminal escrito en Python. Prioridades, fechas límite,
técnica Pomodoro integrada y notificaciones por Telegram, todo sobre una
interfaz de terminal hecha con [Rich](https://github.com/Textualize/rich).

Nació como un proyecto para dejar de usar notas sueltas y acabó siendo el sitio
donde llevo el día a día.

---

## ✨ Qué hace

- **Tareas con prioridad** (alta / media / baja) y **fecha límite** opcional
- **Dashboard** al arrancar: pendientes, completadas, vencidas y próximas
- **Filtros**: pendientes, completadas, urgentes (vencidas o que vencen ya), todas
- **Búsqueda** por texto y **edición** de tareas existentes
- **Ordenación automática** por prioridad y proximidad de la fecha límite
- **🍅 Modo Pomodoro** por tarea, con contador de pomodoros completados
- **📱 Notificaciones por Telegram**: al completar una tarea, y avisos de tareas
  de hoy, de mañana y vencidas
- **Import / export CSV** para sacar los datos a otro sitio

---

## 🖥️ Aspecto

```
╭──────────────────────────────────────────────────────────────────────────────────────╮
│                    ╔════════════════════════════════════════════════╗                │
│                    ║   ████████╗ █████╗ ███████╗██╗  ██╗███████╗   ║                 │
│                    ║   ╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝██╔════╝   ║                 │
│                    ║      ██║   ███████║███████╗█████╔╝ ███████╗   ║                 │
│                    ║      ██║   ██╔══██║╚════██║██╔═██╗ ╚════██║   ║                 │
│                    ║      ██║   ██║  ██║███████║██║  ██╗███████║   ║                 │
│                    ║      ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝   ║                 │
│                    ║         🚀 Gestor de Tareas Pro v3.0 🚀        ║                │
│                    ╚════════════════════════════════════════════════╝                │
╰──────────────────────────────────────────────────────────────────────────────────────╯
                      📅 25/08/2026 - 14:04:14  |  👤 @glitchbane

╭──────────────────╮   ╭──────────────────╮   ╭──────────────────╮  ╭──────────────────╮
│   3              │   │    3             │   │   0              │  │     2            │
│   Total Tareas   │   │    Pendientes    │   │   Completadas    │  │     Urgentes     │
╰──────────────────╯   ╰──────────────────╯   ╰──────────────────╯  ╰──────────────────╯

╭────────────────────────────────── 📊 Estadísticas ───────────────────────────────────╮
│  Progreso General:                                                                   │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0%                               │
│  0 de 3 tareas completadas                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────── 🚨 ATENCIÓN 🚨 ───────────────────────────────────╮
│                          ⏰ 2 tarea(s) próxima(s) a vencer                           │
╰──────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────── 📋 Tus Tareas ────────────────────────────────────╮
│  ┏━━━━┳━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━┓  │
│  ┃ ID ┃ ┃ Tarea                             ┃ Prioridad ┃    Fecha Límite    ┃ 🍅 ┃  │
│  ┡━━━━╇━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━┩  │
│  │ 1  │ │ Entregar informe trimestral       │  🔴 ALTA  │   ⏰ 25/08/2026    │ 3  │  │
│  │    │ │                                   │           │      (¡Hoy!)       │    │  │
│  ├────┼─┼───────────────────────────────────┼───────────┼────────────────────┼────┤  │
│  │ 2  │ │ Revisar pull requests del equipo  │ 🟡 MEDIA  │   ⏰ 26/08/2026    │ 1  │  │
│  │    │ │                                   │           │      (Mañana)      │    │  │
│  ├────┼─┼───────────────────────────────────┼───────────┼────────────────────┼────┤  │
│  │ 3  │ │ Actualizar dependencias           │  🟢 BAJA  │     Sin fecha      │ -  │  │
│  └────┴─┴───────────────────────────────────┴───────────┴────────────────────┴────┘  │
╰──────────────────────────────────────────────────────────────────────────────────────╯

            Leyenda: ⚠️ Vencida | ⏰ Vence pronto | 🍅 Pomodoros completados
```

---

## 🚀 Instalación

Requiere **Python 3.10 o superior**.

```bash
git clone https://github.com/isradev-git/task_manager_terminal.git
cd task_manager_terminal

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

Dependencias: `rich` (interfaz) y `requests` (solo para Telegram).

---

## 📱 Notificaciones por Telegram (opcional)

La app funciona sin esto. Si las quieres:

1. Habla con [@BotFather](https://t.me/BotFather), `/newbot`, y guarda el token.
2. Escríbele a [@userinfobot](https://t.me/userinfobot) para saber tu chat ID.
3. Copia la plantilla y rellénala:

   ```bash
   cp telegram_config.example.json telegram_config.json
   ```

4. Desde el menú, **opción 13 → Probar conexión**.

> ⚠️ `telegram_config.json` está en `.gitignore`. **No subas tu token a ningún
> repositorio.** Este proyecto tuvo uno hardcodeado y acabó robado por un
> scraper en cuestión de días.

---

## 🎮 Menú

| Opción | Qué hace |
|:---:|---|
| 1 | Agregar tarea |
| 2 | Marcar como completada |
| 3 | Eliminar tarea |
| 4 | Filtrar (pendientes / completadas / urgentes / todas) |
| 5 | Editar tarea |
| 6 | Buscar tareas |
| 7 | Exportar a CSV |
| 8 | Importar desde CSV |
| 9 | Mostrar u ocultar completadas |
| 10 | 🍅 Iniciar Pomodoro sobre una tarea |
| 11 | 🍅 Estadísticas de Pomodoro |
| 12 | 🍅 Configurar tiempos de Pomodoro |
| 13 | 📱 Configurar Telegram |
| 14 | Salir |

---

## 🧩 Estructura

| Fichero | Responsabilidad |
|---|---|
| `main.py` | Bucle principal y despacho del menú |
| `task_manager.py` | CRUD de tareas, filtros, búsqueda, import/export CSV |
| `ui.py` | Todo lo visual: panel, dashboard, tablas, ordenación |
| `pomodoro.py` | Temporizador Pomodoro y estadísticas |
| `telegram_bot.py` | Envío de notificaciones vía Bot API |
| `test_no_secrets.py` | Comprueba que no se cuela ningún token en el repo |
| `docs/` | Documentación detallada de cada subsistema |

Los datos viven en `tasks.json` (se crea solo al arrancar, no se versiona).

---

## 🍅 Pomodoro

Por defecto 25 min de trabajo, 5 de descanso corto y 15 de descanso largo cada
4 pomodoros. Configurable desde la opción 12. Cada tarea guarda cuántos
pomodoros le has dedicado.

---

## 📚 Documentación

- [Modo Pomodoro](docs/MODO_POMODORO_GUIA.md)
- [Notificaciones por Telegram](docs/NOTIFICACIONES_TELEGRAM.md)
- [Fechas límite](docs/FECHAS_LIMITE.md)
- [Ordenación de tareas](docs/ORDENAMIENTO_INT.md)

---

## 📄 Licencia

[MIT](LICENSE) © Israel Zamora Tejero
