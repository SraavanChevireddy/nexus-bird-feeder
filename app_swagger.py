#!/usr/bin/env python3
"""
Bird Feeding Flask Application with Swagger Documentation
A hobby project to track bird feeding activities using Nexus Repository for PyPI packages.
"""

from flask import Flask, request
from flask_restx import Api, Resource, fields
import sqlite3
import datetime
import json
import os
import requests

from observe_logger import ObserveLogger, observe_track

app = Flask(__name__)

# Configure Flask-RESTX
api = Api(
    app,
    version='1.0',
    title='🐦 Bird Feeding API',
    description='A comprehensive API for tracking bird feeding activities with enterprise-grade logging and Java integration',
    doc='/swagger/'
)

# Initialize Observe logging
observe_logger = ObserveLogger(app, 'config/observe_config.json')
app.observe_logger = observe_logger

# Database configuration
DATABASE = 'bird_feedings.db'

def load_db_config():
    """Load database configuration from local file or Nexus"""
    try:
        # Try to load from local config file first
        if os.path.exists('config/db_config.json'):
            with open('config/db_config.json', 'r') as f:
                config = json.load(f)
                return config.get('database', {})

        # Fallback: Try to fetch from Nexus (if configured)
        nexus_url = "http://localhost:8081/repository/test-raw/db_config.json"
        try:
            response = requests.get(nexus_url, auth=('admin', 'admin123'))
            if response.status_code == 200:
                print("📦 Loading database config from Nexus Repository!")
                config = response.json()
                return config.get('database', {})
        except Exception as e:
            print(f"Warning: Could not fetch config from Nexus: {e}")

        # Default configuration
        return {
            "type": "sqlite",
            "path": "./bird_feedings.db"
        }
    except Exception as e:
        print(f"Warning: Could not load database config: {e}")
        return {
            "type": "sqlite",
            "path": "./bird_feedings.db"
        }

# Load database configuration
DB_CONFIG = load_db_config()
DATABASE = DB_CONFIG.get('path', 'bird_feedings.db')

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def init_database():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bird_feedings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bird_type TEXT NOT NULL,
            food_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            location TEXT,
            feeding_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Define API models for Swagger documentation
feeding_model = api.model('BirdFeeding', {
    'bird_type': fields.String(required=True, description='Type of bird (e.g., Robin, Sparrow, Cardinal)', example='Robin'),
    'food_type': fields.String(required=True, description='Type of food given (e.g., Seeds, Breadcrumbs, Worms)', example='Seeds'),
    'quantity': fields.Integer(required=True, description='Quantity of food in grams', example=25),
    'location': fields.String(description='Location of feeding', example='Backyard feeder'),
    'notes': fields.String(description='Additional notes about the feeding', example='Morning feeding, bird seemed hungry')
})

feeding_response_model = api.model('FeedingResponse', {
    'id': fields.Integer(description='Unique feeding record ID'),
    'bird_type': fields.String(description='Type of bird'),
    'food_type': fields.String(description='Type of food'),
    'quantity': fields.Integer(description='Quantity of food in grams'),
    'location': fields.String(description='Location of feeding'),
    'notes': fields.String(description='Additional notes'),
    'feeding_time': fields.String(description='Timestamp of feeding')
})

stats_model = api.model('FeedingStats', {
    'total_feedings': fields.Integer(description='Total number of feedings recorded'),
    'most_common_bird': fields.String(description='Most frequently fed bird type'),
    'most_common_food': fields.String(description='Most frequently used food type'),
    'total_food_quantity': fields.Integer(description='Total amount of food given in grams')
})

# Define namespaces
feedings_ns = api.namespace('feedings', description='Bird feeding operations')
stats_ns = api.namespace('stats', description='Feeding statistics')

@api.route('/')
class Home(Resource):
    def get(self):
        """Get API information and available endpoints"""
        return {
            'message': '🐦 Bird Feeding API',
            'description': 'A hobby project to track bird feeding activities using Nexus Repository for PyPI packages',
            'endpoints': {
                'POST /feedings/': 'Add a new bird feeding record',
                'GET /feedings/': 'Get all bird feeding records',
                'GET /stats/': 'Get feeding statistics'
            },
            'swagger_ui': '/swagger/'
        }

@feedings_ns.route('/')
class Feedings(Resource):
    @feedings_ns.expect(feeding_model)
    @feedings_ns.marshal_with(feeding_response_model, code=201)
    @observe_track('bird_feeding_created')
    def post(self):
        """Add a new bird feeding record"""
        try:
            data = request.get_json()

            # Log business event
            app.observe_logger.log_business_event('feeding_request_received', {
                'bird_type': data.get('bird_type'),
                'food_type': data.get('food_type'),
                'quantity': data.get('quantity')
            })

            # Validate required fields
            required_fields = ['bird_type', 'food_type', 'quantity']
            for field in required_fields:
                if not data.get(field):
                    app.observe_logger.log_business_event('feeding_validation_failed', {
                        'missing_field': field,
                        'provided_data': list(data.keys())
                    }, 'WARNING')
                    api.abort(400, f'Missing required field: {field}')

            # Insert into database
            conn = get_db_connection()
            cursor = conn.execute('''
                INSERT INTO bird_feedings (bird_type, food_type, quantity, location, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                data['bird_type'],
                data['food_type'],
                int(data['quantity']),
                data.get('location', ''),
                data.get('notes', '')
            ))

            feeding_id = cursor.lastrowid
            conn.commit()
            conn.close()

            # Log successful creation
            app.observe_logger.log_business_event('feeding_created_successfully', {
                'feeding_id': feeding_id,
                'bird_type': data['bird_type'],
                'food_type': data['food_type'],
                'quantity': data['quantity']
            })

            return {
                'message': 'Feeding recorded successfully',
                'id': feeding_id,
                'timestamp': datetime.datetime.now().isoformat()
            }, 201

        except Exception as e:
            app.observe_logger.log_error(e, {
                'endpoint': '/feedings/',
                'method': 'POST',
                'data': data if 'data' in locals() else None
            })
            api.abort(500, str(e))

    @feedings_ns.marshal_list_with(feeding_response_model)
    @observe_track('bird_feedings_retrieved')
    def get(self):
        """Get all bird feeding records (limited to 50 most recent)"""
        try:
            conn = get_db_connection()
            feedings = conn.execute('''
                SELECT * FROM bird_feedings
                ORDER BY feeding_time DESC
                LIMIT 50
            ''').fetchall()
            conn.close()

            # Convert to list of dictionaries
            feeding_list = []
            for feeding in feedings:
                feeding_list.append({
                    'id': feeding['id'],
                    'bird_type': feeding['bird_type'],
                    'food_type': feeding['food_type'],
                    'quantity': feeding['quantity'],
                    'location': feeding['location'],
                    'notes': feeding['notes'],
                    'feeding_time': feeding['feeding_time']
                })

            # Log business metrics
            app.observe_logger.log_business_event('feedings_retrieved', {
                'total_records': len(feeding_list),
                'unique_birds': len(set(f['bird_type'] for f in feeding_list)),
                'total_quantity': sum(f['quantity'] for f in feeding_list)
            })

            return feeding_list

        except Exception as e:
            app.observe_logger.log_error(e, {
                'endpoint': '/feedings/',
                'method': 'GET'
            })
            api.abort(500, str(e))

@stats_ns.route('/')
class Stats(Resource):
    @stats_ns.marshal_with(stats_model)
    def get(self):
        """Get comprehensive feeding statistics"""
        try:
            conn = get_db_connection()

            # Total feedings
            total_feedings = conn.execute('SELECT COUNT(*) FROM bird_feedings').fetchone()[0]

            # Most common bird type
            common_bird = conn.execute('''
                SELECT bird_type, COUNT(*) as count
                FROM bird_feedings
                GROUP BY bird_type
                ORDER BY count DESC
                LIMIT 1
            ''').fetchone()

            # Most common food type
            common_food = conn.execute('''
                SELECT food_type, COUNT(*) as count
                FROM bird_feedings
                GROUP BY food_type
                ORDER BY count DESC
                LIMIT 1
            ''').fetchone()

            # Total food quantity
            total_quantity = conn.execute('SELECT SUM(quantity) FROM bird_feedings').fetchone()[0] or 0

            conn.close()

            return {
                'total_feedings': total_feedings,
                'most_common_bird': common_bird[0] if common_bird else None,
                'most_common_food': common_food[0] if common_food else None,
                'total_food_quantity': total_quantity
            }

        except Exception as e:
            api.abort(500, str(e))


if __name__ == '__main__':
    # Initialize database on startup
    init_database()

    print("🐦 Bird Feeding API Starting with Swagger Documentation...")
    print("📦 Using Nexus Repository for PyPI packages!")
    print("🌐 API Base URL: http://localhost:8000")
    print("📖 Swagger Documentation: http://localhost:8000/swagger/")
    print("📝 API endpoints:")
    print("   GET  /                    - API information")
    print("   POST /feedings/           - Add new feeding")
    print("   GET  /feedings/           - Get all feedings")
    print("   GET  /stats/              - Get statistics")

    app.run(debug=True, host='0.0.0.0', port=8000)