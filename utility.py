import numpy as np
import mysql.connector
import statistics
from datetime import datetime
from typing import Any, Dict, List, Tuple
from data_extracting_scripts import db_info

# Database credentials
db_config = db_info.db_configuration

# Energy Values for early, late, and both missions
earlyMission_xValues = [5.88, 9.80, 13.72, 17.64, 21.56, 25.48, 29.4, 35.28, 43.12, 50.96,
58.8, 70.56, 86.24, 101.92, 117.6, 141.12, 172.48, 203.84, 235.2, 282.24, 
344.96, 407.68, 470.4, 564.48, 689.92, 815.36, 940.8, 1128.96, 1379.84, 1630.72, 
1881.6, 2257.92, 2759.68, 3261.44, 3763.2, 4515.84, 5519.36, 6522.88, 7526.4, 9031.68, 
11038.72, 13045.75, 15052.79, 18063.35, 22077.43, 26091.51, 30105.59]

lateMission_xValues = [3.92, 3.92, 7.84, 15.19, 19.6, 23.52, 27.44, 31.85, 39.2, 47.04, 
54.88, 63.7, 78.4, 94.08, 109.76, 127.4, 156.8, 188.16, 219.52, 254.8,
313.6, 376.32, 439.04, 509.6, 627.2, 752.64, 878.08, 1019.2, 1254.4, 1505.28,
1756.16, 2038.4, 2508.8, 3010.56, 3512.32, 4076.8, 5017.6, 6021.12, 7024.643,
8153.6, 10035.2, 12042.2, 14049.29, 16307.21, 20070.4, 24084.48, 28098.57]

bothMissions_xValues =  [4.9, 6.86, 10.78, 16.415, 20.58, 24.5, 28.42, 33.565, 41.16, 49, 
                        56.84, 67.13, 82.32, 97, 113.68, 134.26, 164.64, 195.5, 227.36, 268.52, 
                        329.28, 391, 454.72, 537.04, 647.6, 784.28, 910.5, 1030.04, 1184.08, 1317.12, 
                        1552.5, 1819.28, 2148.16, 2526.16, 2909.12, 3375.12, 3946.32, 4766.72, 5770.24, 6773.7615, 
                        8592.64, 10586.96, 12543.975, 14550.04, 17185.28, 21073.915, 25153.495, 29152.08]

def queryDataDict(string_query : str, el_de_query : str, parameters: list, spectra: str):
    """A function that executes the query to extract data in the form of a dictionary format from MySQL Database"""
    
    try:
        yAxisData = {}

        # Connect to MySQL and execute query with parameters
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(string_query, parameters)

        # Fetch data for yAxis
        result = cursor.fetchall()

        cursor.execute(el_de_query, parameters)
        
        # Fetch el_de data for normalization
        el_de_data = cursor.fetchall()

        if not result:
            return 0 

        # Append to yAxis data 
        yAxisData[spectra] = result

        return yAxisData, el_de_data

    except mysql.connector.Error as error:
        print("Error fetching data from MySQL:", error)
        return None
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def queryMissionCount(string_query: str, parameters: List[float]) -> Tuple[int, int]:
    """A function that executes the query to extract mission count data from MySQL Database """
    
    try:
        # Connect to MySQL and execute query 
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(string_query, parameters)

        # Fetch data 
        earlyMissionCount, lateMissionCount = cursor.fetchone()
        
        return earlyMissionCount, lateMissionCount 
    
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return 0,0 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def computeNormalization(el_de_data : list, input_data : dict, yAxisData : dict):
    
    yAxisList = yAxisData[input_data["Spectra"][0]]

    if len(el_de_data) != len(yAxisList):
        return 0
    
    dict_bins = {lst[0]: lst[3:] for lst in yAxisList}
    dict_el_de = {el_de_lst[0]: el_de_lst[3:] for el_de_lst in el_de_data}

    normalized_data = [] 

    mission = input_data["Mission"][0]
    mission_en = {
        "Early Mission": earlyMission_xValues,
        "Late Mission": lateMission_xValues,
        "Both": bothMissions_xValues
    }.get(mission, [])

    normalization = input_data["Normalization"][0]

    # Normalized data
    true = False
    for time_id in dict_bins.keys() & dict_el_de.keys():

        if true:
            break 

        np_dict_bins = np.array(dict_bins[time_id])
        np_el_de = np.array(dict_el_de[time_id])
        np_mission_de = np.array(mission_en)

        if normalization == "Number Flux":
            result = np.divide(np.multiply(np_dict_bins, np_el_de), np_mission_de, out=np.zeros_like(np_mission_de), where=np_mission_de!=0)
            normalized_data.append(result.tolist())

        elif normalization == "Energy Flux":
            result = np.divide(np_dict_bins, np.multiply(np_dict_bins, np_el_de), out=np.zeros_like(np_dict_bins), where=np_dict_bins!=0)
            normalized_data.append(result.tolist())

    # return normalized_data
    return np_dict_bins.tolist(), np_el_de.tolist(), np_mission_de.tolist(), result.tolist()
        

def computeStatistics(input_data: dict, yAxisData: dict, el_de_data : dict):
    """ A function that computes the statistics of the queried data """

    # Get User's Input on Statistics
    if "Statistics" not in input_data or "Spectra" not in input_data or "Normalization" not in input_data:
        return 0 
    
    computed_data = {}
    
    # Get yAxisData in terms of list of list 
    yAxisList = yAxisData[input_data["Spectra"][0]]

    if yAxisList: 

        normalized_values = []
        for lst in yAxisList:
            normalized_values.append(lst[3:])

        # Initialize empty lists to store the calculated statistics for each index
        statistics_required = input_data["Statistics"]
        computed_statistics = {stat: [] for stat in statistics_required}

        # Transpose normalized values
        transposed_values = zip(*normalized_values)
        
        # Iterate over transposed values
        for elements in transposed_values:

            # Compute Statistics
            if "Mean" in statistics_required:
                computed_statistics["Mean"].append(np.mean(elements))

            if "+1\u03c3" in statistics_required:
                computed_statistics["+1\u03c3"].append(np.mean(elements) + np.std(elements))
            
            if "-1\u03c3" in statistics_required:
                computed_statistics["-1\u03c3"].append(np.mean(elements) - np.std(elements))

            if "Median" in statistics_required:
                computed_statistics["Median"].append(statistics.median(elements))

            if "25%" in statistics_required:
                computed_statistics["25%"].append(np.percentile(elements, 25))

            if "75%" in statistics_required:
                computed_statistics["75%"].append(np.percentile(elements, 75))

        computed_data["yAxis"]=computed_statistics

    return computed_data


def convertMLT(time_str : str):
    """A function that converts HH:MM:SS Format to Fractional Hours (MLT)"""

    try:
        # If input is 24:00:00, we assume that its 00:00:00 in the database
        if (time_str == '24:00:00'): 
            return 0.0

        # Parse the time string to a datetime object
        time_obj = datetime.strptime(time_str, '%H:%M:%S')

        # Calculate the total seconds since midnight
        total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second

        # Convert total seconds to fractional hours (MLT)
        mlt = total_seconds / 3600

        return mlt
    except ValueError as e:
        # Handle the ValueError (invalid time string format)
        raise ValueError("Invalid time format. Please provide time in HH:MM:SS format.") from e


def convertTIMEtoEPOCH(time_str : str):
    # Parse the time string to a datetime object
        datetime_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

        # Get the Unix timestamp (Epoch time)
        epoch_time = datetime_obj.timestamp()

        # Convert to integer to remove decimal places
        return int(epoch_time)


def checkNumInput(input_str : str):
    """A function that checks Input to see if its an int/float or it has any notations"""

    try:
        # Attempt to convert input to a float
        num = float(input_str)
        return num
    except ValueError:
        # If ValueError occurs, attempt to handle scientific notation
        if 'e' in input_str.lower():
            try:
                # Split input based on 'e' and convert coefficient and exponent to float
                coefficient, exponent = map(float, input_str.lower().split("e"))
                # Calculate the result using scientific notation
                result = coefficient * pow(10, exponent)
                return result
            except ValueError:
                # Invalid scientific notation format
                raise ValueError("Invalid scientific notation format")
        else:
            # Invalid input
            raise ValueError("Invalid input")


def hasFilters(inputDict : dict):
    """ A function that checks if there is any user input"""

    # Set of allowed keys
    allowed_keys = {'Statistics', 'Spectra', 'Normalization', 'Mission'}
    
    # Check if there are any keys in the dictionary that are not in the allowed keys
    return any(key not in allowed_keys for key in inputDict.keys())




