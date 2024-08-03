from flask import Flask, jsonify
from pymongo import MongoClient
from app import app
import app.data_processing as dp

def connect_db():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['data_db']
    return db

@app.route('/all_courses', methods=['GET'])
def list_all_courses():
    db = connect_db()
    collection = db['data_collection']
    
    # Fetch all documents from the collection
    cursor = collection.find()
    
    # Convert documents to a list and ensure ObjectIds are converted to strings
    courses = list(cursor)
    for course in courses:
        course['_id'] = str(course['_id'])  # Convert ObjectId to string
    
    # Return the list of courses as JSON
    return jsonify(courses)

@app.route('/process_data', methods=['GET'])
def process_data():
    try:
        dp.download_and_normalize_data('data.csv')
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
