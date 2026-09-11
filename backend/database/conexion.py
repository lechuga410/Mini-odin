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


# ============ CRUD DE ALERTAS ============

def crear_alerta(activo_id, titulo, descripcion, severidad, estado):
    """
    Inserta una nueva alerta en la base de datos.
    
    La fecha se genera automáticamente en SQLite.
    
    Args:
        activo_id (int): ID del activo asociado
        titulo (str): Título de la alerta
        descripcion (str): Descripción (puede ser vacío)
        severidad (str): Nivel de severidad
        estado (str): Estado inicial de la alerta
        
    Returns:
        dict: Alerta creada con su ID, o None si hay error
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute(
            '''INSERT INTO alertas 
               (activo_id, titulo, descripcion, severidad, estado) 
               VALUES (?, ?, ?, ?, ?)''',
            (activo_id, titulo, descripcion, severidad, estado)
        )
        conexion.commit()
        
        # Obtener el ID de la alerta creada
        alerta_id = cursor.lastrowid
        
        # Recuperar la alerta completa para devolverla
        alerta = obtener_alerta(alerta_id)
        conexion.close()
        
        return alerta
    except Exception as err:
        print(f"[ERROR] crear_alerta: {err}")
        conexion.close()
        return None


def obtener_alertas_por_activo(activo_id):
    """
    Obtiene todas las alertas de un activo específico.
    
    Args:
        activo_id (int): ID del activo
        
    Returns:
        list: Lista de diccionarios con las alertas del activo
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT * FROM alertas WHERE activo_id = ? ORDER BY id', (activo_id,))
    filas = cursor.fetchall()
    conexion.close()
    
    # Convertir filas a diccionarios
    alertas = []
    for fila in filas:
        alerta = {
            'id': fila[0],
            'activo_id': fila[1],
            'titulo': fila[2],
            'descripcion': fila[3],
            'severidad': fila[4],
            'estado': fila[5],
            'fecha': fila[6]
        }
        alertas.append(alerta)
    
    return alertas


def obtener_alerta(alerta_id):
    """
    Obtiene una alerta por su ID.
    
    Args:
        alerta_id (int): ID de la alerta
        
    Returns:
        dict: Diccionario con los datos de la alerta, o None si no existe
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT * FROM alertas WHERE id = ?', (alerta_id,))
    fila = cursor.fetchone()
    conexion.close()
    
    if not fila:
        return None
    
    return {
        'id': fila[0],
        'activo_id': fila[1],
        'titulo': fila[2],
        'descripcion': fila[3],
        'severidad': fila[4],
        'estado': fila[5],
        'fecha': fila[6]
    }


def actualizar_estado_alerta(alerta_id, nuevo_estado):
    """
    Actualiza únicamente el estado de una alerta.
    
    Args:
        alerta_id (int): ID de la alerta
        nuevo_estado (str): Nuevo estado
        
    Returns:
        dict: Alerta actualizada, o None si no existe o hay error
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute(
            'UPDATE alertas SET estado = ? WHERE id = ?',
            (nuevo_estado, alerta_id)
        )
        conexion.commit()
        
        # Verificar si se actualizó algo
        if cursor.rowcount == 0:
            conexion.close()
            return None
        
        # Recuperar la alerta actualizada
        alerta = obtener_alerta(alerta_id)
        conexion.close()
        
        return alerta
    except Exception as err:
        print(f"[ERROR] actualizar_estado_alerta: {err}")
        conexion.close()
        return None
