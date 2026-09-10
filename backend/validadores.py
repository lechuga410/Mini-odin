"""
Funciones de validación para Mini-Odin.

Valida datos de entrada antes de guardarlos en la base de datos.
"""

import re


def validar_ipv4(ip):
    """
    Valida que una IP sea una IPv4 válida.
    
    Formato esperado: XXX.XXX.XXX.XXX donde cada X está entre 0 y 255.
    
    Args:
        ip (str): Dirección IP a validar
        
    Returns:
        bool: True si es válida, False en caso contrario
    """
    if not isinstance(ip, str):
        return False
    
    # Verificar formato básico: debe tener exactamente 3 puntos
    partes = ip.split('.')
    if len(partes) != 4:
        return False
    
    # Verificar que cada parte sea un número entre 0 y 255
    for parte in partes:
        # Debe ser número
        if not parte.isdigit():
            return False
        
        # Sin ceros a la izquierda (excepto "0")
        if len(parte) > 1 and parte[0] == '0':
            return False
        
        # Debe estar entre 0 y 255
        num = int(parte)
        if num < 0 or num > 255:
            return False
    
    return True


def validar_activo(datos):
    """
    Valida los datos de un activo nuevo.
    
    Args:
        datos (dict): Diccionario con campos del activo
        
    Returns:
        tuple: (es_válido: bool, mensaje_error: str)
               Si es válido, mensaje_error es vacio
    """
    # Campos obligatorios
    if not datos.get('nombre', '').strip():
        return False, "El campo 'nombre' es obligatorio"
    
    if not datos.get('ip', '').strip():
        return False, "El campo 'ip' es obligatorio"
    
    if not datos.get('responsable', '').strip():
        return False, "El campo 'responsable' es obligatorio"
    
    # Validar IP
    if not validar_ipv4(datos.get('ip', '')):
        return False, "La IP no es válida. Formato esperado: XXX.XXX.XXX.XXX (0-255 cada segmento)"
    
    # Validar sistema_operativo (opcional, pero si viene debe ser válido)
    so_permitidos = ['Windows', 'Linux', 'macOS', 'Otro']
    if 'sistema_operativo' in datos and datos['sistema_operativo']:
        if datos['sistema_operativo'] not in so_permitidos:
            return False, f"Sistema operativo inválido. Permitidos: {', '.join(so_permitidos)}"
    
    # Validar criticidad (opcional, pero si viene debe ser válida)
    criticidad_permitidas = ['Baja', 'Media', 'Alta', 'Crítica']
    if 'criticidad' in datos and datos['criticidad']:
        if datos['criticidad'] not in criticidad_permitidas:
            return False, f"Criticidad inválida. Permitidas: {', '.join(criticidad_permitidas)}"
    
    return True, ""
