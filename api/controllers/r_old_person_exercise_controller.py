from flask import Blueprint, jsonify, request

# Import the access data layer modules
from acces_data_layer.services.r_old_person_exercise_service import insert, select_all, delete, update

# Define the endpoint for old person
bp = Blueprint('r_old_person_exercise', __name__, url_prefix='/api/v1')


# Create
@bp.route('/r_old_person_exercise', methods=['POST'])
def create():
    data = request.get_json()
    r_old_person_exercise = data.get('r_old_person_exercise')
    insert(r_old_person_exercise)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/r_old_person_exercise', methods=['GET'])
def get_r_old_person_exercises():
    r_old_person_exercise = select_all()  # Call the select all method in the access data layer
    return jsonify(r_old_person_exercise)


# Update
@bp.route('/r_old_person_exercise', methods=['PUT'])
def update_r_old_person_exercise():
    data = request.get_json()
    r_old_person_exercise = data.get('r_old_person_exercise')
    update(r_old_person_exercise)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/r_old_person_exercise/<old_person_id>/<exercise_id>/<exercise_hour>', methods=['DELETE'])
def delete_r_old_person_exercise(old_person_id, exercise_id, exercise_hour):
    delete(old_person_id, exercise_id, exercise_hour)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
