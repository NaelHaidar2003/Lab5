from flask import Flask, request, jsonify
from flask_cors import CORS
import database  

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/users', methods=['GET'])
def api_get_users():
    """Get all users."""
    return jsonify(database.get_users())

@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    """Get a user by user_id."""
    return jsonify(database.get_user_by_id(user_id))

@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    """Add a new user."""
    user = request.get_json()
    return jsonify(database.insert_user(user))

@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    """Update an existing user."""
    user = request.get_json()
    return jsonify(database.update_user(user))

@app.route('/api/users/delete/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    """Delete a user by user_id."""
    return jsonify(database.delete_user(user_id))

if __name__ == "__main__":
    database.create_db_table()  
    app.run(debug=True) 
