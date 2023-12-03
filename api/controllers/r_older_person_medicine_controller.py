from flask import Blueprint, jsonify, request

from acces_data_layer.models.models import RelOlderPersonMedicine
# Import the access data layer modules
from acces_data_layer.services.r_older_person_medicine_service import insert, select_all, delete, update, select_by_id
from acces_data_layer.services.medicine_service import select_by_id as select_medicine_by_id
from utils import set_rasa_verifier

# Define the endpoint for old person
bp = Blueprint('r_older_person_medicine', __name__, url_prefix='/api/v1')


# Create
@bp.route('/r_older_person_medicine', methods=['POST'])
def create():
    data = request.get_json()
    id_older_person = data.get('id_older_person')
    id_medicine = data.get('id_medicine')
    medicine_hour = data.get('medicine_hour')
    r_older_person_medicine = RelOlderPersonMedicine(
        id_older_person=id_older_person,
        id_medicine=id_medicine,
        medicine_hour=medicine_hour
    )
    insert(r_older_person_medicine)  # Call the insert method in the access data layer
    medicine_name = select_medicine_by_id(id_medicine).medicine_name

    set_rasa_verifier(
        user=id_older_person,
        medicine_name=medicine_name,
        medicine_hour=medicine_hour
    )

    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/r_older_person_medicine', methods=['GET'])
def get_r_older_person_medicines():
    r_older_person_medicines = select_all()  # Call the select all method in the access data layer
    return jsonify(r_older_person_medicines)


@bp.route('/r_older_person_medicine/<id_relation>', methods=['GET'])
def get_r_older_person_medicine_id(id_relation):
    r_older_person_medicine = select_by_id(id_relation).to_dict()  # Call the select by id method in the access data layer
    return jsonify(r_older_person_medicine)


# Update
@bp.route('/r_older_person_medicine', methods=['PUT'])
def update_r_older_person_medicine():
    data = request.get_json()
    id_relation = data.get('id')
    id_older_person = data.get('id_older_person')
    id_medicine = data.get('id_medicine')
    medicine_hour = data.get('medicine_hour')
    r_older_person_medicine = RelOlderPersonMedicine(
        id=id_relation,
        id_older_person=id_older_person,
        id_medicine=id_medicine,
        medicine_hour=medicine_hour
    )
    update(r_older_person_medicine)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/r_older_person_medicine/<id_relation>', methods=['DELETE'])
def delete_r_older_person_medicine(id_relation):
    delete(id_relation)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
