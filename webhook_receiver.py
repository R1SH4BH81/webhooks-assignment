from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Environment variables with defaults
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.environ.get('MONGO_DB', 'github_webhooks')
MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION', 'actions')
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# MongoDB connection
try:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    # Test connection
    client.admin.command('ping')
    logger.info(f"Connected to MongoDB at {MONGO_URI}")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    # Continue anyway to allow the app to start even if MongoDB is not available yet

@app.route('/')
def index():
    return jsonify({
        "status": "running",
        "endpoints": {
            "/webhook": "POST - Receive GitHub webhook events",
            "/actions": "GET - Retrieve all actions"
        }
    })

@app.route('/webhook', methods=['POST'])
def github_webhook():
    try:
        data = request.json
        logger.info(f"Received webhook: {json.dumps(data)[:100]}...")
        
        # Validate required fields
        required_fields = ['request_id', 'author', 'action', 'from_branch', 'to_branch', 'timestamp']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 400
        
        # Validate action type
        valid_actions = ['PUSH', 'PULL_REQUEST', 'MERGE']
        if data['action'] not in valid_actions:
            error_msg = f"Invalid action type: {data['action']}. Must be one of {valid_actions}"
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 400
        
        # Insert into MongoDB
        try:
            collection.insert_one({
                'request_id': data['request_id'],
                'author': data['author'],
                'action': data['action'],
                'from_branch': data['from_branch'],
                'to_branch': data['to_branch'],
                'timestamp': data['timestamp']
            })
            logger.info(f"Stored action: {data['action']} by {data['author']}")
            return jsonify({'status': 'success'}), 201
        except Exception as e:
            logger.error(f"Database error: {e}")
            return jsonify({'error': f"Database error: {str(e)}"}), 500
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({'error': f"Server error: {str(e)}"}), 500

@app.route('/actions', methods=['GET'])
def get_actions():
    try:
        # Return all actions sorted by timestamp descending
        actions = list(collection.find({}, {'_id': 0}).sort('timestamp', -1))
        logger.info(f"Retrieved {len(actions)} actions")
        return jsonify(actions)
    except Exception as e:
        logger.error(f"Error retrieving actions: {e}")
        return jsonify({'error': f"Database error: {str(e)}"}), 500

if __name__ == '__main__':
    logger.info(f"Starting server on port {PORT}")
    app.run(debug=DEBUG, port=PORT, host='0.0.0.0')