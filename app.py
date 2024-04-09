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

    # 3. Process Data
    # processed_result = processing.processQueryData(data, queried_results)
    
    # result = f'{data}'
    result = (data, string_query)
    return jsonify({'result': result}) 


@app.route("/")
def index():

    # data = fetchData()
    
    # if data is None:
    #     # Handle case where data retrieval failed
    #     error_message = "Failed to fetch data from database."
    #     return render_template("error.html", error_message=error_message)
    # return render_template("index.html", data=data)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
