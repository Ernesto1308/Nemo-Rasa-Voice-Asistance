from flask import Blueprint, jsonify, request

# Import the access data layer modules
from acces_data_layer.services.r_old_person_activity_service import insert, select_all, delete, update

# Define the endpoint for old person
bp = Blueprint('r_old_person_activity', __name__, url_prefix='/api/v1')


# Create
@bp.route('/r_old_person_activity', methods=['POST'])
def create():
    data = request.get_json()
    r_old_person_activity = data.get('r_old_person_activity')
    insert(r_old_person_activity)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/r_old_person_activity', methods=['GET'])
def get_r_old_person_activities():
    r_old_person_activity = select_all()  # Call the select all method in the access data layer
    return jsonify({'r_old_person_activity': r_old_person_activity})


# Update
@bp.route('/r_old_person_activity', methods=['PUT'])
def update_r_old_person_activity():
    data = request.get_json()
    r_old_person_activity = data.get('r_old_person_activity')
    update(r_old_person_activity)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/r_old_person_activity/<old_person_id>/<activity_id>/<activity_hour>', methods=['DELETE'])
def delete_r_old_person_activity(old_person_id, activity_id, activity_hour):
    delete(old_person_id, activity_id, activity_hour)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
