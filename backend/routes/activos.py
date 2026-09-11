"""
Rutas/endpoints para la gestión de activos.

Define los cuatro endpoints CRUD:
- GET /api/activos → Listar todos
- POST /api/activos → Crear nuevo
- PUT /api/activos/<id> → Editar
- DELETE /api/activos/<id> → Eliminar
"""

from flask import Blueprint, request, jsonify
from database.conexion import (
    crear_activo, obtener_activos, obtener_activo,
    actualizar_activo, eliminar_activo
)
from validadores import validar_activo

# Crear blueprint (grupo de rutas)
bp_activos = Blueprint('activos', __name__, url_prefix='/api/activos')


@bp_activos.route('', methods=['GET'])
def listar_activos():
    """
    GET /api/activos
    
    Retorna la lista de activos con búsqueda y filtro opcionales.
    
    Parámetros de query (opcionales):
    - buscar: Buscar por nombre o IP (búsqueda parcial)
    - criticidad: Filtrar por criticidad (Baja, Media, Alta, Crítica)
    
    Ejemplos:
    - GET /api/activos
    - GET /api/activos?buscar=PC-CONTABILIDAD
    - GET /api/activos?criticidad=Alta
    - GET /api/activos?buscar=192.168.1&criticidad=Media
    
    Returns:
        JSON: Lista de activos que coinciden
        HTTP 200 si éxito
        HTTP 400 si criticidad inválida
    """
    # Obtener parámetros de query
    buscar = request.args.get('buscar', None)
    criticidad = request.args.get('criticidad', None)
    
    # Validar criticidad si se proporciona
    if criticidad:
        criticidades_validas = ['Baja', 'Media', 'Alta', 'Crítica']
        if criticidad not in criticidades_validas:
            return jsonify({
                'error': f"Criticidad inválida. Permitidas: {', '.join(criticidades_validas)}"
            }), 400
    
    # Llamar a la función de base de datos con parámetros seguros
    activos = obtener_activos(buscar=buscar, criticidad=criticidad)
    
    return jsonify(activos), 200


@bp_activos.route('', methods=['POST'])
def crear_activo_endpoint():
    """
    POST /api/activos
    
    Crea un nuevo activo con los datos enviados en el body.
    
    Body esperado (JSON):
    {
        "nombre": "PC-CONTABILIDAD-01",
        "ip": "192.168.1.10",
        "sistema_operativo": "Windows",
        "responsable": "Juan Pérez",
        "criticidad": "Media"
    }
    
    Returns:
        JSON: Activo creado con su ID
        HTTP 201 si éxito
        HTTP 400 si datos inválidos
    """
    datos = request.get_json()
    
    # Validar que los datos no sean None
    if not datos:
        return jsonify({'error': 'El body debe ser JSON válido'}), 400
    
    # Validar los datos
    es_valido, mensaje_error = validar_activo(datos)
    if not es_valido:
        return jsonify({'error': mensaje_error}), 400
    
    # Establecer valores por defecto si no vienen
    sistema_operativo = datos.get('sistema_operativo', 'Otro')
    criticidad = datos.get('criticidad', 'Media')
    
    # Crear el activo
    activo = crear_activo(
        nombre=datos['nombre'],
        ip=datos['ip'],
        sistema_operativo=sistema_operativo,
        responsable=datos['responsable'],
        criticidad=criticidad
    )
    
    if not activo:
        return jsonify({'error': 'Error al crear el activo'}), 500
    
    return jsonify(activo), 201


@bp_activos.route('/<int:activo_id>', methods=['PUT'])
def editar_activo_endpoint(activo_id):
    """
    PUT /api/activos/<id>
    
    Edita un activo existente.
    
    Body esperado (JSON):
    {
        "nombre": "PC-CONTABILIDAD-01",
        "ip": "192.168.1.10",
        "sistema_operativo": "Windows",
        "responsable": "Juan Pérez",
        "criticidad": "Media"
    }
    
    Returns:
        JSON: Activo actualizado
        HTTP 200 si éxito
        HTTP 400 si datos inválidos
        HTTP 404 si el activo no existe
    """
    # Verificar que el activo existe
    activo = obtener_activo(activo_id)
    if not activo:
        return jsonify({'error': f'Activo con ID {activo_id} no encontrado'}), 404
    
    datos = request.get_json()
    
    if not datos:
        return jsonify({'error': 'El body debe ser JSON válido'}), 400
    
    # Validar los datos
    es_valido, mensaje_error = validar_activo(datos)
    if not es_valido:
        return jsonify({'error': mensaje_error}), 400
    
    # Establecer valores por defecto si no vienen
    sistema_operativo = datos.get('sistema_operativo', activo['sistema_operativo'])
    criticidad = datos.get('criticidad', activo['criticidad'])
    
    # Actualizar
    activo_actualizado = actualizar_activo(
        activo_id=activo_id,
        nombre=datos['nombre'],
        ip=datos['ip'],
        sistema_operativo=sistema_operativo,
        responsable=datos['responsable'],
        criticidad=criticidad
    )
    
    if not activo_actualizado:
        return jsonify({'error': 'Error al actualizar el activo'}), 500
    
    return jsonify(activo_actualizado), 200


@bp_activos.route('/<int:activo_id>', methods=['DELETE'])
def eliminar_activo_endpoint(activo_id):
    """
    DELETE /api/activos/<id>
    
    Elimina un activo.
    
    Returns:
        JSON: Confirmación de eliminación
        HTTP 200 si éxito
        HTTP 404 si el activo no existe
    """
    # Verificar que el activo existe
    activo = obtener_activo(activo_id)
    if not activo:
        return jsonify({'error': f'Activo con ID {activo_id} no encontrado'}), 404
    
    # Eliminar
    eliminado = eliminar_activo(activo_id)
    
    if not eliminado:
        return jsonify({'error': 'Error al eliminar el activo'}), 500
    
    return jsonify({'mensaje': f'Activo {activo_id} eliminado correctamente'}), 200
