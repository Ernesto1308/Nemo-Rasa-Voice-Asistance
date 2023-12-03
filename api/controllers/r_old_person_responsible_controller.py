from flask import Blueprint, jsonify, request

from acces_data_layer.models.models import RelOlderPersonResponsible
# Import the access data layer modules
from acces_data_layer.services.r_older_person_responsible_service import insert, select_all, delete, update, \
    select_by_id

# Define the endpoint for old person
bp = Blueprint('r_older_person_responsible', __name__, url_prefix='/api/v1')


# Create
@bp.route('/r_older_person_responsible', methods=['POST'])
def create():
    data = request.get_json()
    id_older_person = data.get('id_older_person')
    id_responsible_person = data.get('id_responsible_person')
    r_older_person_responsible = RelOlderPersonResponsible(
        id_older_person=id_older_person,
        id_responsible_person=id_responsible_person
    )
    insert(r_older_person_responsible)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/r_older_person_responsible', methods=['GET'])
def get_r_older_person_responsible():
    r_older_person_responsible = select_all()  # Call the select all method in the access data layer
    r_older_person_responsible_dict = [r_older_person_responsible.to_dict() for r_older_person_responsible in
                                       r_older_person_responsible]
    return jsonify(r_older_person_responsible_dict)


@bp.route('/r_older_person_responsible/<id_relation>', methods=['GET'])
def get_r_older_person_responsible_id(id_relation):
    r_older_person_responsible = select_by_id(id_relation).to_dict()  # Call the select by id method in the access data layer
    return jsonify(r_older_person_responsible)


# Update
@bp.route('/r_older_person_responsible', methods=['PUT'])
def update_r_older_person_responsible():
    data = request.get_json()
    id_relation = data.get('id')
    id_older_person = data.get('id_older_person')
    id_responsible_person = data.get('id_responsible_person')
    r_older_person_responsible = RelOlderPersonResponsible(
        id=id_relation,
        id_older_person=id_older_person,
        id_responsible_person=id_responsible_person
    )
    update(r_older_person_responsible)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/r_older_person_responsible/<id_relation>', methods=['DELETE'])
def delete_r_older_person_responsible(id_relation):
    delete(id_relation)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
