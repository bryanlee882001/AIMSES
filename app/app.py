from flask import Flask, request, jsonify, render_template
from . import create_query
from . import utility
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database with path relative to project root
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLITE_DATABASE_URI', 'sqlite:///db/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/process-data', methods=['POST']) 
def processData(): 
    data = request.json['data'] 

    # 0: Check if there's any user input (other than statistics, spectra, normalization, and mission)
    if utility.hasFilters(data) == False:
        return jsonify({'result': 0}) 

    # 1: Create Join Query Based on Selection Criterias and Filters
    string_query, el_de_query, parameters, spectral_table_name = create_query.createJoinQuery(data)

    # 2: Query from database
    queried_results, el_de_data = utility.queryDataDict(string_query, el_de_query, parameters, spectral_table_name)

    if queried_results == 0 or el_de_data == 0:
        return jsonify({'result': 0})   
    
    # 3. Compute Statistics
    result = utility.computeStatistics(data, queried_results, el_de_data) 

    # 4. Returns final Y values after computing statistics 
    return jsonify({'result': result}) 


@app.route('/mission-data', methods=['POST']) 
def missionData(): 
    data = request.json['data'] 

    # Create queries for early and late missions
    string_query, parameters = create_query.createQueryForMission(data)

    # Get earlyMission count and lateMission count
    earlyMissionCount, lateMissionCount = utility.queryMissionCount(string_query, parameters)

    return jsonify({'result': (earlyMissionCount, lateMissionCount)}) 


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)