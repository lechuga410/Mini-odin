"""
Mini-Odin: Aplicación Flask para gestión de activos y alertas de seguridad.
Ruta A: Python + Flask + HTML/CSS/JS + SQLite
"""

from flask import Flask, render_template, jsonify
import os

# Crear instancia de Flask
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend')
)


@app.route('/')
def index():
    """Página de inicio: Panel resumen"""
    return render_template('index.html')


@app.route('/activos')
def activos():
    """Página de gestión de activos"""
    return render_template('activos.html')


@app.route('/alertas')
def alertas():
    """Página de gestión de alertas"""
    return render_template('alertas.html')


@app.route('/api/health')
def health():
    """Endpoint de verificación: confirma que el servidor está activo"""
    return jsonify({'status': 'ok', 'message': 'Mini-Odin backend activo'})


if __name__ == '__main__':
    # Ejecutar con debug=True para desarrollo
    app.run(debug=True, host='127.0.0.1', port=5000)
