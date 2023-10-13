from flask import Blueprint, jsonify, request

# Import the access data layer modules
from acces_data_layer.services.feeding_service import insert, select_all, select_by_id, delete, update

# Define the endpoint for old person
bp = Blueprint('feeding', __name__, url_prefix='/api/v1')


# Create
@bp.route('/feeding', methods=['POST'])
def create():
    data = request.get_json()
    feeding = data.get('feeding')
    insert(feeding)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/feeding', methods=['GET'])
def get_feeding():
    feeding = select_all()  # Call the select all method in the access data layer
    return jsonify(feeding)


@bp.route('/feeding/<feeding_id>', methods=['GET'])
def get_feeding_id(feeding_id):
    feeding = select_by_id(feeding_id)  # Call the select by id method in the access data layer
    return jsonify({'feeding': feeding})


# Update
@bp.route('/feeding', methods=['PUT'])
def update_feeding():
    data = request.get_json()
    feeding = data.get('feeding')
    update(feeding)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/feeding/<feeding_id>', methods=['DELETE'])
def delete_feeding(feeding_id):
    delete(id_feeding=feeding_id)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
