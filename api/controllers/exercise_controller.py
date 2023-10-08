from flask import Blueprint, jsonify, request

# Import the access data layer modules
from acces_data_layer.services.exercise_service import insert, select_all, select_by_id, delete, update

# Define the endpoint for old person
bp = Blueprint('exercise', __name__, url_prefix='/api/v1')


# Create
@bp.route('/exercise', methods=['POST'])
def create():
    data = request.get_json()
    exercise = data.get('exercise')
    insert(exercise)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/exercise', methods=['GET'])
def get_exercises():
    exercises = select_all()  # Call the select all method in the access data layer
    return jsonify({'exercises': exercises})


@bp.route('/exercise/<exercise_id>', methods=['GET'])
def get_exercise_id(exercise_id):
    exercise = select_by_id(exercise_id)  # Call the select by id method in the access data layer
    return jsonify({'exercise': exercise})


# Update
@bp.route('/exercise', methods=['PUT'])
def update_exercise():
    data = request.get_json()
    exercise = data.get('exercise')
    update(exercise)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/exercise/<exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    delete(id_exercise=exercise_id)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
