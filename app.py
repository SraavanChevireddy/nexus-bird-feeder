#!/usr/bin/env python3
"""
Bird Feeding Flask Application
A hobby project to track bird feeding activities using Nexus Repository for PyPI packages.
"""

from flask import Flask, request, jsonify
import sqlite3
import datetime
import json
import os
import requests

app = Flask(__name__)

# Database configuration
DATABASE = 'bird_feedings.db'

def load_db_config():
    """Load database configuration from local file or Nexus"""
    try:
        # Try to load from local config file first
        if os.path.exists('db_config.json'):
            with open('db_config.json', 'r') as f:
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

@app.route('/')
def home():
    """API information endpoint"""
    return jsonify({
        'message': '🐦 Bird Feeding API',
        'description': 'A hobby project to track bird feeding activities using Nexus Repository for PyPI packages',
        'endpoints': {
            'POST /api/feedings': 'Add a new bird feeding record',
            'GET /api/feedings': 'Get all bird feeding records',
            'GET /api/stats': 'Get feeding statistics'
        },
        'example_post_data': {
            'bird_type': 'Robin',
            'food_type': 'Seeds',
            'quantity': 25,
            'location': 'Backyard feeder',
            'notes': 'Morning feeding'
        }
    })

@app.route('/api/feedings', methods=['POST'])
def add_feeding():
    """Add a new bird feeding record"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['bird_type', 'food_type', 'quantity']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
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
        
        return jsonify({
            'message': 'Feeding recorded successfully',
            'id': feeding_id,
            'timestamp': datetime.datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedings', methods=['GET'])
def get_feedings():
    """Get all bird feeding records"""
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
        
        return jsonify(feeding_list)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get feeding statistics"""
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
        
        return jsonify({
            'total_feedings': total_feedings,
            'most_common_bird': common_bird[0] if common_bird else None,
            'most_common_food': common_food[0] if common_food else None,
            'total_food_quantity': total_quantity
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    
    print("🐦 Bird Feeding API Starting...")
    print("📦 Using Nexus Repository for PyPI packages!")
    print("🌐 API Base URL: http://localhost:8080")
    print("📝 API endpoints:")
    print("   GET  /              - API information")
    print("   POST /api/feedings  - Add new feeding")
    print("   GET  /api/feedings  - Get all feedings")
    print("   GET  /api/stats     - Get statistics")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
