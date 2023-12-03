from flask import Blueprint, jsonify, request

from acces_data_layer.models.models import ResponsiblePerson
# Import the access data layer modules
from acces_data_layer.services.responsible_person_service import insert, select_all, select_by_id, delete, update

# Define the endpoint for old person
bp = Blueprint('responsible_person', __name__, url_prefix='/api/v1')


# Create
@bp.route('/responsible_person', methods=['POST'])
def create():
    data = request.get_json()
    responsible_person_name = data.get('responsible_person_name')
    responsible_person = ResponsiblePerson(responsible_person_name=responsible_person_name)
    insert(responsible_person)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/responsible_person', methods=['GET'])
def get_resp_persons():
    responsible_persons = select_all()  # Call the select all method in the access data layer
    responsible_persons_dict = [resp_person.to_dict() for resp_person in responsible_persons]
    return jsonify(responsible_persons_dict)


@bp.route('/responsible_person/<id_responsible_person>', methods=['GET'])
def get_resp_person_by_id(id_responsible_person):
    responsible_person = select_by_id(id_responsible_person).to_dict() # Call the select by id method in the access data layer
    return jsonify(responsible_person)


# Update
@bp.route('/responsible_person', methods=['PUT'])
def update_resp_person():
    data = request.get_json()
    id_responsible_person = data.get('id_responsible_person')
    responsible_person_name = data.get('responsible_person_name')
    responsible_person = ResponsiblePerson(
        id_responsible_person=id_responsible_person,
        responsible_person_name=responsible_person_name
    )
    update(responsible_person)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/responsible_person/<id_responsible_person>', methods=['DELETE'])
def delete_resp_person(id_responsible_person):
    delete(id_resp_person=id_responsible_person)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
