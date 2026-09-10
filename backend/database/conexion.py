"""
Módulo de conexión y inicialización de SQLite para Mini-Odin.

Funciones simples para:
- Obtener conexión a la base de datos
- Inicializar las tablas si no existen
- CRUD de activos
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


# ============ CRUD DE ACTIVOS ============

def crear_activo(nombre, ip, sistema_operativo, responsable, criticidad):
    """
    Inserta un nuevo activo en la base de datos.
    
    Args:
        nombre (str): Nombre del activo
        ip (str): Dirección IP
        sistema_operativo (str): SO del activo
        responsable (str): Persona responsable
        criticidad (str): Nivel de criticidad
        
    Returns:
        dict: Activo creado con su ID, o None si hay error
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute(
            '''INSERT INTO activos 
               (nombre, ip, sistema_operativo, responsable, criticidad) 
               VALUES (?, ?, ?, ?, ?)''',
            (nombre, ip, sistema_operativo, responsable, criticidad)
        )
        conexion.commit()
        
        # Obtener el ID del activo creado
        activo_id = cursor.lastrowid
        
        # Recuperar el activo completo para devolverlo
        activo = obtener_activo(activo_id)
        conexion.close()
        
        return activo
    except Exception as err:
        print(f"[ERROR] crear_activo: {err}")
        conexion.close()
        return None


def obtener_activos():
    """
    Obtiene todos los activos de la base de datos.
    
    Returns:
        list: Lista de diccionarios con los activos
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT * FROM activos ORDER BY id')
    filas = cursor.fetchall()
    conexion.close()
    
    # Convertir filas a diccionarios
    activos = []
    for fila in filas:
        activo = {
            'id': fila[0],
            'nombre': fila[1],
            'ip': fila[2],
            'sistema_operativo': fila[3],
            'responsable': fila[4],
            'criticidad': fila[5],
            'fecha_creacion': fila[6]
        }
        activos.append(activo)
    
    return activos


def obtener_activo(activo_id):
    """
    Obtiene un activo por su ID.
    
    Args:
        activo_id (int): ID del activo
        
    Returns:
        dict: Diccionario con los datos del activo, o None si no existe
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT * FROM activos WHERE id = ?', (activo_id,))
    fila = cursor.fetchone()
    conexion.close()
    
    if not fila:
        return None
    
    return {
        'id': fila[0],
        'nombre': fila[1],
        'ip': fila[2],
        'sistema_operativo': fila[3],
        'responsable': fila[4],
        'criticidad': fila[5],
        'fecha_creacion': fila[6]
    }


def actualizar_activo(activo_id, nombre, ip, sistema_operativo, responsable, criticidad):
    """
    Actualiza los datos de un activo existente.
    
    Args:
        activo_id (int): ID del activo a actualizar
        nombre (str): Nuevo nombre
        ip (str): Nueva IP
        sistema_operativo (str): Nuevo SO
        responsable (str): Nuevo responsable
        criticidad (str): Nueva criticidad
        
    Returns:
        dict: Activo actualizado, o None si no existe o hay error
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute(
            '''UPDATE activos 
               SET nombre = ?, ip = ?, sistema_operativo = ?, responsable = ?, criticidad = ? 
               WHERE id = ?''',
            (nombre, ip, sistema_operativo, responsable, criticidad, activo_id)
        )
        conexion.commit()
        
        # Verificar si se actualizó algo
        if cursor.rowcount == 0:
            conexion.close()
            return None
        
        # Recuperar el activo actualizado
        activo = obtener_activo(activo_id)
        conexion.close()
        
        return activo
    except Exception as err:
        print(f"[ERROR] actualizar_activo: {err}")
        conexion.close()
        return None


def eliminar_activo(activo_id):
    """
    Elimina un activo de la base de datos.
    
    Nota: Las alertas asociadas se eliminan automáticamente por ON DELETE CASCADE.
    
    Args:
        activo_id (int): ID del activo a eliminar
        
    Returns:
        bool: True si se eliminó, False si no existe o hay error
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('DELETE FROM activos WHERE id = ?', (activo_id,))
        conexion.commit()
        
        # Verificar si se eliminó algo
        eliminado = cursor.rowcount > 0
        conexion.close()
        
        return eliminado
    except Exception as err:
        print(f"[ERROR] eliminar_activo: {err}")
        conexion.close()
        return False
