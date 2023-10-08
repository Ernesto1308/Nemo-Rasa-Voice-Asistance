from flask import Blueprint, jsonify, request

# Import the access data layer modules
from acces_data_layer.services.r_old_person_feeding_service import insert, select_all, delete, update

# Define the endpoint for old person
bp = Blueprint('r_old_person_feeding', __name__, url_prefix='/api/v1')


# Create
@bp.route('/r_old_person_feeding', methods=['POST'])
def create():
    data = request.get_json()
    r_old_person_feeding = data.get('r_old_person_feeding')
    insert(r_old_person_feeding)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/r_old_person_feeding', methods=['GET'])
def get_r_old_person_feeding():
    r_old_person_feeding = select_all()  # Call the select all method in the access data layer
    return jsonify({'r_old_person_feeding': r_old_person_feeding})


# Update
@bp.route('/r_old_person_feeding', methods=['PUT'])
def update_r_old_person_feeding():
    data = request.get_json()
    r_old_person_feeding = data.get('r_old_person_feeding')
    update(r_old_person_feeding)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/r_old_person_feeding/<old_person_id>/<feeding_id>/<feeding_hour>', methods=['DELETE'])
def delete_r_old_person_feeding(old_person_id, feeding_id, feeding_hour):
    delete(old_person_id, feeding_id, feeding_hour)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
