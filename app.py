from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database configuration
HOST = "python.cvq464wkqi4r.us-west-2.rds.amazonaws.com"
USERNAME = "admin"
PASSWORD = "password"
DATABASE = "python"

# Database functions
def connect_db():
    """Connects to the database and returns a connection object"""
    try:
        connection = mysql.connector.connect(
            host=HOST, user=USERNAME, password=PASSWORD, database=DATABASE
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def insert_ip(original_ip, reversed_ip):
    """Inserts original and reversed IP into the database"""
    try:
        connection = connect_db()
        if connection:
            cursor = connection.cursor()
            sql = "INSERT INTO ip_data (original_ip, reversed_ip) VALUES (%s, %s)"
            values = (original_ip, reversed_ip)
            cursor.execute(sql, values)
            connection.commit()
            print("Successfully inserted IP data")
            cursor.close()
            connection.close()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")

# Flask routes
@app.route('/')
def get_reversed_ip():
    """Returns both original and reversed IP addresses"""
    original_ip = request.remote_addr
    reversed_ip = '.'.join(original_ip.split('.')[::-1])
    insert_ip(original_ip, reversed_ip)
    return jsonify({'original_ip': original_ip, 'reversed_ip': reversed_ip})

@app.route('/original-ip')
def get_original_ip():
    """Returns the original IP address"""
    original_ip = request.remote_addr
    return jsonify({'original_ip': original_ip})

@app.route('/reversed-ip')
def get_reversed_ip_only():
    """Returns the reversed IP address"""
    original_ip = request.remote_addr
    reversed_ip = '.'.join(original_ip.split('.')[::-1])
    return jsonify({'reversed_ip': reversed_ip})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5600)

