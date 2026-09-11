# Mini-Odin

**Sistema de gestión de activos tecnológicos y alertas de seguridad**

Versión sencilla y educativa para la prueba técnica de Indtech.

## Stack

- **Backend:** Python + Flask
- **Frontend:** HTML, CSS, JavaScript puro
- **Datos:** SQLite
- **Sin frameworks frontend:** No React, Vue, ni Angular

## Instalación y ejecución

### Requisitos previos

- Python 3.9 o superior
- pip

### Pasos

1. **Clonar o descargar el proyecto**

   ```bash
   cd Mini-Odin
   ```

2. **Crear un entorno virtual** (opcional pero recomendado)

   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el servidor**

   ```bash
   python backend/app.py
   ```

5. **Abrir en el navegador**

   - Panel de inicio: [http://localhost:5000](http://localhost:5000)
   - Activos: [http://localhost:5000/activos](http://localhost:5000/activos)
   - Alertas: [http://localhost:5000/alertas](http://localhost:5000/alertas)

## Estructura del proyecto

```
mini-odin/
├── mini_odin.db
├── requirements.txt
├── README.md
├── PROMPTS.md
├── backend/
│   ├── app.py
│   ├── riesgo.py
│   ├── validadores.py
│   ├── routes/
│   │   └── __init__.py
│   └── database/
│       ├── __init__.py
│       └── conexion.py
└── frontend/
    ├── index.html
    ├── activos.html
    ├── alertas.html
    ├── css/
    │   └── estilos.css
    └── js/
        ├── api.js
        ├── resumen.js
        ├── activos.js
        ├── alertas.js
        └── validadores.js
```

## Estado de implementación

- ✅ Fase 0 — Estructura inicial y configuración de Flask
- ✅ Fase 1 — Base de datos SQLite
- ✅ Fase 2 — Gestión de activos (backend CRUD + pruebas)
- ✅ Fase 3 — Gestión de alertas (backend CRUD + 9 pruebas)
- ✅ Fase 4 — Buscador y filtros( 12/12 PASADAS PRUEBAS)
- ⏳ Fase 5 — Panel resumen (backend)
- ⏳ Fase 6 — Función de cálculo de riesgo 
- ⏳ Fase 7 — Integración completa del panel y backend
- ⏳ Fase 8 — Frontend completo de la aplicación 
- ✅ Fase 9 — Pruebas completas y manejo de errores
- ✅ Fase 10 — Documentación y prompts
- ✅ Fase 11 — Preparación de videos y entrega

## Ejecución

Actualmente, la aplicación inicia correctamente y sirve las páginas HTML.

Para verificar que el backend está activo:
- Abre [http://localhost:5000/api/health](http://localhost:5000/api/health)
- Deberías ver: `{"status":"ok","message":"Mini-Odin backend activo"}`

## Notas

- No hay autenticación.
- No hay APIs externas.
- El código prioriza simplicidad y claridad sobre complejidad.
- Cada línea debe poder explicarse en una entrevista técnica.
