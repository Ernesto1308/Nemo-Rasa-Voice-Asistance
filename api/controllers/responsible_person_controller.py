from flask import Blueprint, jsonify, request

# Import the access data layer modules
from acces_data_layer.services.responsible_person_service import insert, select_all, select_by_id, delete, update

# Define the endpoint for old person
bp = Blueprint('responsible_person', __name__, url_prefix='/api/v1')


# Create
@bp.route('/responsible_person', methods=['POST'])
def create():
    data = request.get_json()
    responsible_person = data.get('responsible_person')
    insert(responsible_person)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/responsible_person', methods=['GET'])
def get_resp_persons():
    responsible_persons = select_all()  # Call the select all method in the access data layer
    return jsonify(responsible_persons)


@bp.route('/responsible_person/<responsible_person_id>', methods=['GET'])
def get_resp_person_by_id(responsible_person_id):
    responsible_person = select_by_id(responsible_person_id)  # Call the select by id method in the access data layer
    return jsonify({'responsible_person': responsible_person})


# Update
@bp.route('/responsible_person', methods=['PUT'])
def update_resp_person():
    data = request.get_json()
    responsible_person = data.get('responsible_person')
    update(responsible_person)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/responsible_person/<responsible_person_id>', methods=['DELETE'])
def delete_resp_person(responsible_person_id):
    delete(id_resp_person=responsible_person_id)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
