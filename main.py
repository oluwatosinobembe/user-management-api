from flask import Flask, jsonify, request
import json

app = Flask(__name__)

USER_DATA_FILE = 'user_data.json'

# Function to save user data to a file
def save_user_data(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

# Function to load user data from a file
def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Initialize users from file or create an empty list if file doesn't exist
users = load_user_data()

# Endpoint to retrieve a list of users
@app.route('/v1/users', methods=['GET'])
def get_users():
    return jsonify(users)

# Endpoint to create a new user
@app.route('/v1/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    users.append(user_data)
    save_user_data(users)  # Save updated user data to file
    return jsonify({'message': 'User created successfully'}), 201

# Endpoint to retrieve a user by ID
@app.route('/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['id'] == user_id:
            return jsonify(user)
    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
