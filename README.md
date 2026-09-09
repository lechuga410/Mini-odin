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
├── backend/
│   ├── app.py                 # Aplicación Flask principal
│   ├── riesgo.py              # Función de cálculo de riesgo (por implementar)
│   ├── validadores.py         # Validaciones (por implementar)
│   ├── routes/                # Blueprints de rutas
│   └── database/              # Módulo de base de datos
├── frontend/
│   ├── index.html             # Panel resumen
│   ├── activos.html           # Gestión de activos
│   ├── alertas.html           # Gestión de alertas
│   ├── css/
│   │   └── estilos.css        # Estilos globales
│   └── js/
│       ├── api.js             # Comunicación con backend
│       ├── resumen.js         # Lógica del panel
│       ├── activos.js         # Lógica de activos
│       ├── alertas.js         # Lógica de alertas
│       └── validadores.js     # Validaciones en cliente
├── requirements.txt
├── README.md
└── PROMPTS.md
```

## Estado de implementación

- ✅ Estructura de carpetas
- ✅ Configuración básica de Flask
- ✅ Páginas HTML mínimas
- ✅ Estilos CSS básicos
- ⏳ Base de datos SQLite (siguiente fase)
- ⏳ Endpoints CRUD
- ⏳ Función de riesgo
- ⏳ Validaciones
- ⏳ Interfaz de usuario funcional

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
