import numpy as np
import mysql.connector
import statistics
from datetime import datetime
from typing import Any, Dict, List, Tuple
from data_extracting_scripts import db_info

# Database credentials
db_config = db_info.db_configuration


def queryDataDict(string_query : str, parameters: list, spectra: str):
    """A function that executes the query to extract data in the form of a dictionary format from MySQL Database"""
    try:

        yAxisData = {}

        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)

        # Create cursor
        cursor = connection.cursor()

        # Execute SQL query with parameters
        cursor.execute(string_query, parameters)

        # Fetch data
        result = cursor.fetchall()

        if not result:
            return 0 

        # Append to yAxis data 
        yAxisData[spectra] = result

        return yAxisData

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
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)

        # Create cursor 
        cursor = connection.cursor()

        # Execute the early mission query
        cursor.execute(string_query, parameters)
        earlyMissionCount, lateMissionCount = cursor.fetchone()
        
        return earlyMissionCount, lateMissionCount 
    
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return 0,0 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def computeStatistics(input_data: dict, yAxisData: dict):
    """ A function that computes the statistics of the data """

    # Get User's Input on Statistics
    if "Statistics" not in input_data:
        return 0 
    
    computed_data = {}

    # Get yAxisData in terms of list of list 
    yAxisList = yAxisData[input_data["Spectra"][0]]

    if yAxisList: 

        # Initialize an empty list to store the sums
        index_values = []

        # Iterate over each sublist in yAxisList
        for lst in yAxisList:
            index_values.append(lst[3:])

        # Transpose the modified lists to get the values at each index
        transposed_values = zip(*index_values)

        # Initialize empty lists to store the calculated statistics for each index
        statistics_required = input_data["Statistics"]
        computed_statistics = {stat: [] for stat in statistics_required}

        # Iterate over transposed values
        for elements in transposed_values:
            
            # Compute Normalization
            # 106     for yy = 0l, n_times-1 do begin
            # 107       ;;print, yy
            # 108       current_time = cur_times[yy]
            # 109       tm_index = where(tm[0:n_tm-1] eq cur_times[yy])
            # 110       cnt = n_elements(tm_index)
            # 111       ;;stop
            # 112      if cnt eq 1 and tm_index[0] eq -1 then begin
            # 113        print, 'Times do not match orbits.  Orbit: '+strcompress(string(current_orb),/remove_all)+ $
            # 114                ' Time: '+time_string(current_time)
            # 115        continue
            # 116      endif
            # 117      if energy[tm_index,0] lt 20000 or energy[tm_index,46] gt 10 then continue
            # 118      if keyword_set(numnorm) then begin
            # 119       tflxel0[nn]=total(el0[tm_index,*]*norm_fac[tm_index,*]/energy[tm_index,*])
            # 120       tflxel180[nn]=total(el180[tm_index,*]*norm_fac[tm_index,*]/energy[tm_index,*])
            # 121       tflxel90[nn]=total(el90[tm_index,*]*norm_fac[tm_index,*]/energy[tm_index,*])
            # 122       tflxel270[nn]=total(el270[tm_index,*]*norm_fac[tm_index,*]/energy[tm_index,*])
            # 123     endif else if keyword_set(ennorm) then begin
            # 124       tflxel0[nn]=total(el0[tm_index,*]*norm_fac[tm_index,*])
            # 125       tflxel180[nn]=total(el180[tm_index,*]*norm_fac[tm_index,*])
            # 126       tflxel90[nn]=total(el90[tm_index,*]*norm_fac[tm_index,*])
            # 127       tflxel270[nn]=total(el270[tm_index,*]*norm_fac[tm_index,*])
            # 128     endif else begin
            # 129       tflxel0[nn]=1.
            # 130       tflxel180[nn]=1.
            # 131       tflxel90[nn]=1.
            # 132       tflxel270[nn]=1.
            # 133     endelse
            # 134      keep_el0[nn,*] = el0[tm_index,*]/tflxel0[nn]
            # 135      keep_el180[nn,*] = el180[tm_index,*]/tflxel180[nn]
            # 136      keep_el90[nn,*] = el90[tm_index,*]/tflxel90[nn]
            # 137      keep_el270[nn,*] = el270[tm_index,*]/tflxel270[nn]
            # 138      keep_energy[nn,*] = energy[tm_index,*]
            # 139      keep_orb[nn] = current_orb
            # 140      keep_times[nn] = current_time
            # 141      nn=nn+1
            # 142     endfor
            # Do I need el_de to compute normalization? 
            # How do I compute the statistics then since normalization itself returns the final 47 elements. 

            # Compute Statistics
            if "Mean" in statistics_required:
                computed_statistics["Mean"].append(np.mean(elements))

            if "+1\u03c3" in statistics_required:
                computed_statistics["+1\u03c3"].append(np.mean(elements) - np.std(elements))
            
            if "-1\u03c3" in statistics_required:
                computed_statistics["-1\u03c3"].append(np.mean(elements) + np.std(elements))

            if "Median" in statistics_required:
                computed_statistics["Median"].append(statistics.median(elements))

            if "25%" in statistics_required:
                computed_statistics["25%"].append(np.percentile(elements, 25))

            if "75%" in statistics_required:
                computed_statistics["75%"].append(np.percentile(elements, 75))

        computed_data["yAxis"]=computed_statistics

    # Not sure if xAxis is computed like this: (there might be multiple sets of values for x-axis)
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




