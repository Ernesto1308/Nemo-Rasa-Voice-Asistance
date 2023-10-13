from flask import Blueprint, jsonify, request

# Import the access data layer modules
from acces_data_layer.services.old_person_service import insert, select_all, select_by_id, delete, update

# Define the endpoint for old person
bp = Blueprint('old_person', __name__, url_prefix='/api/v1')


# Create
@bp.route('/old_person', methods=['POST'])
def create():
    data = request.get_json()
    old_person = data.get('old_person')
    insert(old_person)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/old_person', methods=['GET'])
def get_old_persons():
    old_persons = select_all()  # Call the select all method in the access data layer
    return jsonify(old_persons)


@bp.route('/old_person/<old_person_id>', methods=['GET'])
def get_old_person_by_id(old_person_id):
    old_person = select_by_id(old_person_id)  # Call the select by id method in the access data layer
    return jsonify({'old_person': old_person})


# Update
@bp.route('/old_person', methods=['PUT'])
def update_old_person():
    data = request.get_json()
    old_person = data.get('old_person')
    update(old_person)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/old_person/<old_person_id>', methods=['DELETE'])
def delete_old_person(old_person_id):
    delete(id_old_person=old_person_id)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
