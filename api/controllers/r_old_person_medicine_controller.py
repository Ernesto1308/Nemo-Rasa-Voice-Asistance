from flask import Blueprint, jsonify, request

# Import the access data layer modules
from acces_data_layer.services.r_old_person_medicine_service import insert, select_all, delete, update

# Define the endpoint for old person
bp = Blueprint('r_old_person_medicine', __name__, url_prefix='/api/v1')


# Create
@bp.route('/r_old_person_medicine', methods=['POST'])
def create():
    data = request.get_json()
    r_old_person_medicine = data.get('r_old_person_medicine')
    insert(r_old_person_medicine)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/r_old_person_medicine', methods=['GET'])
def get_r_old_person_medicines():
    r_old_person_medicine = select_all()  # Call the select all method in the access data layer
    return jsonify({'r_old_person_medicine': r_old_person_medicine})


# Update
@bp.route('/r_old_person_medicine', methods=['PUT'])
def update_r_old_person_medicine():
    data = request.get_json()
    r_old_person_medicine = data.get('r_old_person_medicine')
    update(r_old_person_medicine)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/r_old_person_medicine/<old_person_id>/<medicine_id>/<medicine_hour>', methods=['DELETE'])
def delete_r_old_person_medicine(old_person_id, medicine_id, medicine_hour):
    delete(old_person_id, medicine_id, medicine_hour)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
