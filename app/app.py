import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from .query_builder import QueryBuilder  
from .aimses import AIMSES  

app = Flask(__name__)

# Database Configuration
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/process-data', methods=['POST']) 
def processData(): 
    data = request.json['data'] 
    
    try:
        # Initialize AIMSES for events
        aimses = AIMSES('events', data)
        
        # Get events from database
        events = aimses.get_events()
        if not events:
            return jsonify({'result': 0, 'error': "No Events found"})
        
        # Compute statistics
        aimses.compute_statistics()
        
        # Get final statistics
        result = aimses.get_final_statistics()
        
        return jsonify({'result': result})
    
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return jsonify({'result': 0, 'error': str(e)})


@app.route('/mission-data', methods=['POST']) 
def missionData(): 
    data = request.json['data'] 
    
    try:
        # Initialize AIMSES for count
        aimses = AIMSES('count', data)
        
        # Get events count
        success = aimses.get_events()
        if not success:
            return jsonify({'result': (0, 0)})
        
        # Get final count
        counts = aimses.get_final_count()
        
        return jsonify({
            'result': (
                counts['early_mission'],
                counts['late_mission']
            )
        })
    
    except Exception as e:
        print(f"Error getting mission data: {str(e)}")
        return jsonify({'result': (0, 0), 'error': str(e)})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)