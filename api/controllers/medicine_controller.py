from flask import Blueprint, jsonify, request

# Import the access data layer modules
from acces_data_layer.services.medicine_service import insert, select_all, select_by_id, delete, update

# Define the endpoint for old person
bp = Blueprint('medicine', __name__, url_prefix='/api/v1')


# Create
@bp.route('/medicine', methods=['POST'])
def create():
    data = request.get_json()
    medicine = data.get('medicine')
    insert(medicine)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/medicine', methods=['GET'])
def get_medicines():
    medicine = select_all()  # Call the select all method in the access data layer
    return jsonify(medicine)


@bp.route('/medicine/<medicine_id>', methods=['GET'])
def get_medicine_id(medicine_id):
    medicine = select_by_id(medicine_id)  # Call the select by id method in the access data layer
    return jsonify({'medicine': medicine})


# Update
@bp.route('/medicine', methods=['PUT'])
def update_medicine():
    data = request.get_json()
    medicine = data.get('medicine')
    update(medicine)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/medicine/<medicine_id>', methods=['DELETE'])
def delete_medicine(medicine_id):
    delete(id_medicine=medicine_id)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
