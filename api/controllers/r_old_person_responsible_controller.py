from flask import Blueprint, jsonify, request

# Import the access data layer modules
from acces_data_layer.services.r_old_person_responsible_service import insert, select_all, delete, update

# Define the endpoint for old person
bp = Blueprint('r_old_person_responsible', __name__, url_prefix='/api/v1')


# Create
@bp.route('/r_old_person_responsible', methods=['POST'])
def create():
    data = request.get_json()
    r_old_person_responsible = data.get('r_old_person_responsible')
    insert(r_old_person_responsible)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/r_old_person_responsible', methods=['GET'])
def get_r_old_person_responsible():
    r_old_person_responsible = select_all()  # Call the select all method in the access data layer
    return jsonify({'r_old_person_responsible': r_old_person_responsible})


# Update
@bp.route('/r_old_person_responsible', methods=['PUT'])
def update_r_old_person_responsible():
    data = request.get_json()
    r_old_person_responsible = data.get('r_old_person_responsible')
    update(r_old_person_responsible)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/r_old_person_responsible/<old_person_id>/<responsible_id>', methods=['DELETE'])
def delete_r_old_person_responsible(old_person_id, responsible_id):
    delete(old_person_id, responsible_id)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
