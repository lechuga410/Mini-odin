"""
Módulo de conexión y inicialización de SQLite para Mini-Odin.

Funciones simples para:
- Obtener conexión a la base de datos
- Inicializar las tablas si no existen
"""

import sqlite3
import os

# Ruta de la base de datos (en la raíz del proyecto)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'mini_odin.db')


def obtener_conexion():
    """
    Abre una conexión a SQLite.
    
    Retorna:
        sqlite3.Connection: Conexión activa a mini_odin.db
    """
    conexion = sqlite3.connect(DB_PATH)
    # Activar soporte de foreign keys en SQLite
    conexion.execute('PRAGMA foreign_keys = ON')
    return conexion


def inicializar_bd():
    """
    Crea las tablas (activos y alertas) si no existen.
    
    Esta función se ejecuta una sola vez al iniciar la aplicación.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Crear tabla ACTIVOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ip TEXT NOT NULL,
            sistema_operativo TEXT NOT NULL,
            responsable TEXT NOT NULL,
            criticidad TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Crear tabla ALERTAS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activo_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            severidad TEXT NOT NULL,
            estado TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (activo_id) REFERENCES activos(id) ON DELETE CASCADE
        )
    ''')
    
    # Crear índices para mejorar búsquedas
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_alertas_activo_id 
        ON alertas(activo_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_alertas_estado 
        ON alertas(estado)
    ''')
    
    conexion.commit()
    conexion.close()
