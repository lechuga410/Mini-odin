"""
Rutas/endpoints para la gestión de alertas.

Define tres endpoints:
- GET /api/alertas/<activo_id> → Listar alertas de un activo
- POST /api/alertas → Crear nueva alerta
- PUT /api/alertas/<id>/estado → Cambiar estado
"""

from flask import Blueprint, request, jsonify
from database.conexion import (
    obtener_activo, crear_alerta, obtener_alertas_por_activo,
    obtener_alerta, actualizar_estado_alerta
)
from validadores import validar_alerta, validar_estado_alerta

# Crear blueprint (grupo de rutas)
bp_alertas = Blueprint('alertas', __name__, url_prefix='/api/alertas')


@bp_alertas.route('/<int:activo_id>', methods=['GET'])
def listar_alertas_endpoint(activo_id):
    """
    GET /api/alertas/<activo_id>
    
    Retorna las alertas asociadas a un activo.
    
    Args:
        activo_id (int): ID del activo
    
    Returns:
        JSON: Lista de alertas
        HTTP 200 si éxito
        HTTP 404 si el activo no existe
    """
    # Verificar que el activo existe
    activo = obtener_activo(activo_id)
    if not activo:
        return jsonify({'error': f'Activo con ID {activo_id} no encontrado'}), 404
    
    # Obtener alertas del activo
    alertas = obtener_alertas_por_activo(activo_id)
    
    return jsonify(alertas), 200 


@bp_alertas.route('', methods=['POST'])
def crear_alerta_endpoint():
    """
    POST /api/alertas
    
    Crea una nueva alerta sobre un activo.
    
    Body esperado (JSON):
    {
        "activo_id": 1,
        "titulo": "Antivirus desactualizado",
        "descripcion": "La versión instalada necesita actualización",
        "severidad": "Alta",
        "estado": "Abierta"
    }
    
    Returns:
        JSON: Alerta creada con su ID
        HTTP 201 si éxito
        HTTP 400 si datos inválidos
        HTTP 404 si el activo no existe
    """
    datos = request.get_json()
    
    # Validar que los datos sean JSON válido
    if not datos:
        return jsonify({'error': 'El body debe ser JSON válido'}), 400
    
    # Verificar que activo_id existe
    if not datos.get('activo_id'):
        return jsonify({'error': "El campo 'activo_id' es obligatorio"}), 400
    
    activo = obtener_activo(datos['activo_id'])
    if not activo:
        return jsonify({'error': f"Activo con ID {datos['activo_id']} no encontrado"}), 404
    
    # Validar los datos de la alerta
    es_valido, mensaje_error = validar_alerta(datos)
    if not es_valido:
        return jsonify({'error': mensaje_error}), 400
    
    # Crear la alerta
    # descripcion es opcional, usar vacío si no viene
    descripcion = datos.get('descripcion', '')
    
    alerta = crear_alerta(
        activo_id=datos['activo_id'],
        titulo=datos['titulo'],
        descripcion=descripcion,
        severidad=datos['severidad'],
        estado=datos['estado']
    )
    
    if not alerta:
        return jsonify({'error': 'Error al crear la alerta'}), 500
    
    return jsonify(alerta), 201


@bp_alertas.route('/<int:alerta_id>/estado', methods=['PUT'])
def cambiar_estado_alerta_endpoint(alerta_id):
    """
    PUT /api/alertas/<id>/estado
    
    Cambia el estado de una alerta.
    
    Body esperado (JSON):
    {
        "estado": "En análisis"
    }
    
    Returns:
        JSON: Alerta actualizada
        HTTP 200 si éxito
        HTTP 400 si estado inválido
        HTTP 404 si la alerta no existe
    """
    # Verificar que la alerta existe
    alerta = obtener_alerta(alerta_id)
    if not alerta:
        return jsonify({'error': f'Alerta con ID {alerta_id} no encontrada'}), 404
    
    datos = request.get_json()
    
    if not datos:
        return jsonify({'error': 'El body debe ser JSON válido'}), 400
    
    # Obtener y validar estado
    nuevo_estado = datos.get('estado')
    if not nuevo_estado:
        return jsonify({'error': "El campo 'estado' es obligatorio"}), 400
    
    if not validar_estado_alerta(nuevo_estado):
        return jsonify({'error': "Estado inválido. Permitidos: Abierta, En análisis, Cerrada"}), 400
    
    # Actualizar estado
    alerta_actualizada = actualizar_estado_alerta(alerta_id, nuevo_estado)
    
    if not alerta_actualizada:
        return jsonify({'error': 'Error al actualizar el estado'}), 500
    
    return jsonify(alerta_actualizada), 200
