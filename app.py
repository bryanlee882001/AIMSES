from flask import Flask, request, jsonify, render_template
import create_query
import processing
import query_from_db
import utility

app = Flask(__name__)


@app.route('/process-data', methods=['POST']) 
def processData(): 
    data = request.json['data'] 

    # 0: Check if there's any user input (other than statistics, spectra, normalization, and mission)
    if utility.hasFilters(data) == False:
        return jsonify({'result': 0}) 

    # 1: Create String Query Based on Selection Criterias and Filters
    string_query, parameters, spectral_table_name = create_query.createJoinQuery(data)

    # 2: Query from MySQL database
    queried_results = query_from_db.queryDataDict(string_query, parameters, spectral_table_name)

    if queried_results == 0:
        return jsonify({'result': 0})   
    
    # 3. Compute Statistics
    result = processing.computeStatistics(data, queried_results) 

    if result == 0: 
        return jsonify({'result': 0})    
    
    # result = (final x values, final y values)
    return jsonify({'result': result}) 



@app.route('/mission-data', methods=['POST']) 
def missionData(): 
    data = request.json['data'] 

    # Create queries for early and late missions
    early_mission_query, late_mission_query, early_params, late_params = create_query.createQueryForMission(data)

    # Get earlyMission count and lateMission count
    earlyMissionCount, lateMissionCount = query_from_db.queryMissionCount(early_mission_query, late_mission_query, early_params, late_params)

    return jsonify({'result': (earlyMissionCount, lateMissionCount)}) 


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
