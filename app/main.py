from flask import Flask, jsonify, request
import os
import datetime
from app.storage import read_from_gcs, write_to_gcs
from app.ai import generate_joke

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({
        "message": "Bienvenue sur notre Mini-API GCP!",
        "status": "success"
    }), 200

@app.route('/status', methods=['GET'])
def status():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({
        "server_time": current_time,
        "status": "running"
    }), 200

@app.route('/data', methods=['GET'])
def get_data():
    try:
        data = read_from_gcs()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data', methods=['POST'])
def post_data():
    try:
        content = request.json
        if not content:
            return jsonify({"error": "No data provided"}), 400
        
        result = write_to_gcs(content)
        return jsonify({
            "message": "Data successfully added",
            "data": content,
            "result": result
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/joke', methods=['GET'])
def joke():
    try:
        joke_text = generate_joke()
        return jsonify({
            "joke": joke_text
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


