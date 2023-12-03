from flask import Blueprint, jsonify, request

from acces_data_layer.models.models import Medicine
# Import the access data layer modules
from acces_data_layer.services.medicine_service import insert, select_all, select_by_id, delete, update

# Define the endpoint for old person
bp = Blueprint('medicine', __name__, url_prefix='/api/v1')


# Create
@bp.route('/medicine', methods=['POST'])
def create():
    data = request.get_json()
    medicine_name = data.get('medicine_name')
    medicine = Medicine(medicine_name=medicine_name)
    insert(medicine)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/medicine', methods=['GET'])
def get_medicines():
    medicines = select_all()  # Call the select all method in the access data layer
    medicines_dict = [medicine.to_dict() for medicine in medicines]
    return jsonify(medicines_dict)


@bp.route('/medicine/<id_medicine>', methods=['GET'])
def get_medicine_id(id_medicine):
    medicine = select_by_id(id_medicine).to_dict()  # Call the select by id method in the access data layer
    return jsonify(medicine)


# Update
@bp.route('/medicine', methods=['PUT'])
def update_medicine():
    data = request.get_json()
    id_medicine = data.get('id_medicine')
    medicine_name = data.get('medicine_name')
    medicine = Medicine(
        id_medicine=id_medicine,
        medicine_name=medicine_name
    )
    update(medicine)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/medicine/<id_medicine>', methods=['DELETE'])
def delete_medicine(id_medicine):
    delete(id_medicine=id_medicine)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
