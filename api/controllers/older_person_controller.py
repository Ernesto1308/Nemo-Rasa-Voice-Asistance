from flask import Blueprint, jsonify, request

from acces_data_layer.models.models import OlderPerson
# Import the access data layer modules
from acces_data_layer.services.older_person_service import insert, select_all, select_by_id, delete, update
from utils import deserialize_bytes

# Define the endpoint for old person
bp = Blueprint('older_person', __name__, url_prefix='/api/v1')


# Create
@bp.route('/older_person', methods=['POST'])
def create():
    data = request.get_json()
    older_person_name = data.get('older_person_name')
    audio = data.get('audio')
    older_person = OlderPerson(older_person_name=older_person_name, audio=audio)
    insert(older_person)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/older_person', methods=['GET'])
def get_older_persons():
    old_persons = select_all()  # Call the select all method in the access data layer
    old_persons_dict = [older_person.to_dict() for older_person in old_persons]
    return jsonify(old_persons_dict)


@bp.route('/older_person/<id_older_person>', methods=['GET'])
def get_older_person_by_id(id_older_person):
    older_person = select_by_id(id_older_person).to_dict()  # Call the select by id method in the access data layer
    return jsonify(older_person)


# Update
@bp.route('/older_person', methods=['PUT'])
def update_older_person():
    data = request.get_json()
    id_older_person = data.get('id_older_person')
    older_person_name = data.get('older_person_name')
    audio = deserialize_bytes(data.get('audio'))
    older_person = OlderPerson(
        id_older_person=id_older_person,
        older_person_name=older_person_name,
        audio=audio
    )
    update(older_person)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/older_person/<id_older_person>', methods=['DELETE'])
def delete_older_person(id_older_person):
    delete(id_older_person)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
