from flask import Blueprint, jsonify, request

# Import the access data layer modules
from acces_data_layer.services.activity_service import insert, select_all, select_by_id, delete, update

# Define the endpoint for old person
bp = Blueprint('activity', __name__, url_prefix='/api/v1')


# Create
@bp.route('/activity', methods=['POST'])
def create():
    data = request.get_json()
    activity = data.get('activity')
    insert(activity)  # Call the insert method in the access data layer
    return jsonify({'message': 'Resource created successfully'})


# Read
@bp.route('/activity', methods=['GET'])
def get_activities():
    activities = select_all()  # Call the select all method in the access data layer
    return jsonify({'activities': activities})


@bp.route('/activity/<activity_id>', methods=['GET'])
def get_activity_id(activity_id):
    activity = select_by_id(activity_id)  # Call the select by id method in the access data layer
    return jsonify({'activity': activity})


# Update
@bp.route('/activity', methods=['PUT'])
def update_activity():
    data = request.get_json()
    activity = data.get('activity')
    update(activity)  # Call the update method in the access data layer
    return jsonify({'message': 'Resource updated successfully'})


# Delete
@bp.route('/activity/<activity_id>', methods=['DELETE'])
def delete_resp_person(activity_id):
    delete(id_activity=activity_id)  # Call the delete method in the access data layer
    return jsonify({'message': 'Resource deleted successfully'})
