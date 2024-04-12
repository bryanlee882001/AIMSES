from flask import Flask, request, jsonify, render_template
import create_query
import processing
import query_from_db

app = Flask(__name__)


@app.route('/process-data', methods=['POST']) 
def processData(): 
    data = request.json['data'] 

    # 1: Create String Query Based on Selection Criterias and Filters
    string_query = create_query.createQuery(data)

    # 2: Get Information 
    queried_results = query_from_db.queryDataDict(string_query)

    # 3. Process Data and Query from CDF_DATA / UPGOING / DOWNGOING / PERPENDICULAR 
    process_query = processing.processQueryData(data, queried_results)
    
    if process_query is None: 
        return jsonify({'result': 0})     

    # 4. Query data and return values in the form of a dictionary 
    spectral_data = query_from_db.queryFromSpectraDict(process_query)
    
    # 5. Compute Statistics
    result = processing.getStatistics(data, spectral_data) 
    
    # result = (final x values, final y values)
    return jsonify({'result': result}) 


@app.route('/mission-data', methods=['POST']) 
def missionData(): 
    data = request.json['data'] 

    # Count for Early Mission and Late Mission Query
    query = create_query.createQueryForMission(data)

    # get earlyMission count and lateMission count
    earlyMissionCount, lateMissionCount = query_from_db.queryMissionCount(query)

    return jsonify({'result': (earlyMissionCount, lateMissionCount)}) 


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
