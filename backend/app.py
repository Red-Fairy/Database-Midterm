from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Set up MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'  # Update if your MySQL server is on a different host
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username, e.g., 'root'
app.config['MYSQL_PASSWORD'] = '123456'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'sampledb'  # Replace with your database name, in this case, 'sampledb'


mysql = MySQL(app)

@app.route('/api/data')
def get_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    # Convert the data to a list of dictionaries
    result = []
    for row in data:
        result.append({'ID': row[0], 'Name': row[1], 'Email': row[2]})

    return jsonify(result)

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()

    name = data.get('Name')
    email = data.get('Email')

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (Name, Email) VALUES (%s, %s)", (name, email))
    mysql.connection.commit()

    print("Affected rows:", cursor.rowcount)  # Debug print

    return jsonify({"message": "User added successfully"})

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    name = data.get('Name')
    email = data.get('Email')

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET Name = %s, Email = %s WHERE ID = %s", (name, email, user_id))
    mysql.connection.commit()

    return jsonify({"message": "User updated successfully"})


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE ID = %s", (user_id,))
    mysql.connection.commit()

    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
