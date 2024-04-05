"""
Title: CDF Converter v1.2 
Author: Bryan Yen Sheng Lee
Description: This script extracts data from .cdf files, processes it, and inserts it into a MySQL database.
"""

import cdflib
import struct
import datetime
import mysql.connector
import numpy as np
import glob
import os
import time
import decimal
import math
import db_info


# Database credentials
db_config = db_info.db_configuration


def GetZVariables(path: str):
    """A function that extracts specific fields/attributes from cdf files. Add and remove fields in varNeeded list as needed. 
    Here are the fields:
    
    TIME, el_0_lc, el_0_lc12, el_0_20, el_180_lc, el_180_lc12, el_180_20, el_90_30, el_90_lcp12, el_270_30, el_270_lcp12, 
    el_en, el_de, el_low, el_low_pa, el_high, el_high_pa, el_vlow, el_vlow_pa, el_ulow, el_ulow_pa, dTime, lca, init_res_dim, 
    Je_0t90, Je_90t180, Je_0pm4, Je_180pm4, Je_0lc, Je_180lc, Je_0lcp12, Je_0lcm12, Je_180lcp12, Je_180lcm12, Je_net, JEe_0t90, 
    JEe_90t180, JEe_0pm4, JEe_180pm4, JEe_0lc, JEe_180lc, JEe_0lcp12, JEe_0lcm12, JEe_180lcp12, JEe_180lcm12, JEe_net, Je_0t90_lt30, 
    Je_90t180_lt30, Je_0pm4_lt30, Je_180pm4_lt30, Je_0lc_lt30, Je_180lc_lt30, Je_0lcp12_lt30, Je_0lcm12_lt30, Je_180lcp12_lt30, 
    Je_180lcm12_lt30, Je_net_lt30, JEe_0t90_lt30, JEe_90t180_lt30, JEe_0pm4_lt30, JEe_180pm4_lt30, JEe_0lc_lt30, JEe_180lc_lt30, 
    JEe_0lcp12_lt30, JEe_0lcm12_lt30, JEe_180lcp12_lt30, JEe_180lcm12_lt30, JEe_net_lt30
    
    """

    # NOTE:
    # If you want to limit fields which are pushed to database, then remove the fields from this array 
    varNeeded = ['TIME','JEe_0lc','JEe_180lc','JEe_0t90','JEe_90t180','Je_0lc','Je_180lc',
             'Je_0t90','Je_90t180','el_0_lc','el_180_lc','el_90_lcp12','el_270_lcp12','el_en']

    # Read CDF file into a CDF object
    try: 
        cdf = cdflib.CDF(path)
    except Exception as e:
         print(f"An exception of type {type(e).__name__} occurred when reading CDF File into a CDF object: {e}")
        
    varDict = {}

    # Get zVariables from CDF object
    try:
        zVariables = cdf.cdf_info().zVariables 
    except Exception as e: 
        print(f"An exception of type {type(e).__name__} occurred when getting Z-Variables from CDF File: {e}")
        return None; 
    else: 
        for ii in range(len(zVariables)):

            # NOTE:
            # Remove this if statement if you want all fields to be extracted
            if zVariables[ii] in varNeeded:
                # Insert values into Dictionary based on column names
                varDict[f"{zVariables[ii]}"] = cdf.varget(zVariables[ii])
        
    return varDict 


def PushToDataBase(varDict: dict, fileName: str):
    """ A function that pushes data from cdf files onto the database """
    
    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        start_time = time.time()

        # Calls CreateTableQuery() to generate table query 
        create_table_query, mainTableColumnsList = CreateTableQuery(varDict,fileName)

        try: 
            cursor.execute(create_table_query)
            conn.commit()  
        except Exception as e:
            print(f"Error creating table: {str(e)}")

        # Call CompileDataIntoQueryFormat() function and insert them into the database row-by-row
        data_lists_of_lists = CompileDataIntoQueryFormat(varDict, fileName)
        
        columns = ', '.join(mainTableColumnsList)

        for i in range(len(data_lists_of_lists)):

            values = ', '.join(map(str, data_lists_of_lists[i]))

            query = f"INSERT INTO {fileName} ({columns}) VALUES ({values});"

            try: 
                cursor.execute(query)
                conn.commit()
            except Exception as e:
                print(f"{fileName} Table: Error Inserting values at row {i}: {str(e)}")

        print(f"Successfully inserted data into {len(data_lists_of_lists)} row(s)")

        cursor.close()
        conn.close()
        
        print(f'Data inserted successfully for {fileName}. Time Taken: {time.time() - start_time}s \n')

    except mysql.connector.Error as err:
        print(f"Error pushing to database: {err}")

    finally:
        # Ensure the connection is closed in case of an exception
        if 'conn' in locals():
            conn.close()


def CompileDataIntoQueryFormat(varDict: dict, fileName: str):
    """ A function that compiles all data from dictionary into a list of list """
        
    # create empty tables 
    dataArr = [[] for _ in range(len(varDict["TIME"]))]

    list_of_time = []
    
    perpendicularTables = {
        "el_90_lcp12" : [],
        "el_270_lcp12" : []
    }

    # loop through each column
    for column, values in varDict.items():

        # replace 'isnan' with 'NULL' and set precision to 30
        values_list = values.tolist()
        values_updated = FormatValue(values_list, column)
                                  
        # create empty lists 
        altDataArr = [[] for _ in range(len(values_updated))]

        # loop through each list in dictionary values
        for index, value in enumerate(values_updated):
            # If data is a list and the list is not empty
            if isinstance(value, list) and len(value) != 0:    

                # Append values into each row           
                for i in range(len(value)):
                    altDataArr[index].append(value[i])

                # Get TIME
                time = decimal.Decimal("{:.{}f}".format(varDict["TIME"][index], 30))
                
                # Insert time at the beginning
                altDataArr[index].insert(0, time)

                # List of Time used to determine spectra for each row
                list_of_time.append(time)

            # If it is any other data types (not list)
            else:
                dataArr[index].append(value)
        
        # Only create alternate table for variables if its a list
        if any(altDataArr):
            
            # To Determine Upgoing and Downgoing 
            if (column == "el_0_lc" or column == "el_180_lc"):
                print("Determining Upgoing and Downgoing")

                # Gets a list of TIME along with ILAT values
                spectraDict = CheckSpectraFromNormalizedDB(list_of_time, column)

                # Create Alternate Table 
                CreateAltAndInsertTable(column, altDataArr, spectraDict)

            # To Determine Perpendicular (Computed outside for loop)
            if column == "el_90_lcp12":
                perpendicularTables[column] = altDataArr
            if column == "el_270_lcp12":
                perpendicularTables[column] = altDataArr
    

    len_el_90_lcp12 = len(perpendicularTables["el_90_lcp12"])
    len_el_270_lcp12 = len(perpendicularTables["el_270_lcp12"])

    if len_el_90_lcp12 == 0 or len_el_270_lcp12 == 0 or len_el_90_lcp12 != len_el_270_lcp12:
        print(f"Error in data: el_90_lcp12 and el_270_lcp12 cannot compute perpendicular spectra")
        return dataArr 
    
    perpendicularVal = [[] for _ in range(len(perpendicularTables['el_270_lcp12']))]

    print("Determining Perpendicular using el_270_lcp12 and el_90_lcp12")
    
    for ii in range(len_el_270_lcp12):
        # Add Time 
        perpendicularVal[ii].append(perpendicularTables["el_270_lcp12"][ii][0])

        for jj in range(1, len(perpendicularTables["el_270_lcp12"][ii])):

            if perpendicularTables['el_270_lcp12'][ii][jj] is None:
                perpendicularTables['el_270_lcp12'][ii][jj]  = decimal.Decimal(0.0)
            elif perpendicularTables['el_90_lcp12'][ii][jj] is None:
                perpendicularTables['el_90_lcp12'][ii][jj]  = decimal.Decimal(0.0)
        
            # Compute Perpendicular Values
            perpendicularVal[ii].append((perpendicularTables['el_270_lcp12'][ii][jj] + perpendicularTables['el_90_lcp12'][ii][jj]) / decimal.Decimal(2.0))

    CreateAltAndInsertPerpendicularTable(perpendicularVal)

    return dataArr


def CheckSpectraFromNormalizedDB(list_of_time: list, column: str): 
    """Checks Time from AIMSES_Norm to determine if time is upgoing, downgoing, or perpendicular"""

    if len(list_of_time) == 0:
        print(f"No TIME available for {column}")
        return None 

    spectraDict = {}

    query = f""" SELECT TIME, ILAT FROM AIMSES_Norm WHERE TIME IN 
                ({', '.join([f"'{time}'" for time in list_of_time])})
            """

    try: 
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Execute the query with the list of times as parameters
        # cursor.execute(query, list_of_time)
        cursor.execute(query)

        # Fetch all results
        results = cursor.fetchall()

        if results is None:
            print(f"No TIME queried from database for {column}")
            return None 
        
        for ii in range(len(results)):
            ilat = results[ii]['ILAT']
            time = results[ii]['TIME']

            # Check Upgoing, Downgoing
            if column == "el_0_lc":
                if ilat > 0:
                    spectraDict[time] = 'downgoing'
                elif ilat < 0:
                    spectraDict[time] = 'upgoing'
            elif column == "el_180_lc":
                if ilat > 0:
                    spectraDict[time] = 'upgoing'
                elif ilat < 0: 
                    spectraDict[time] = 'downgoing'
            else:
                return None

        if results is None:
            print(f"CheckSpectraFromNormalizedDB(): No ILAT values queried from DB for field {column}")
            return None
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    return spectraDict


def CreateAltAndInsertTable(fieldName: str, values: list, spectraDict: dict):
    """ A function that takes creates/update another table if values are in a list/array format """
    
    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        if len(values) == 0 or spectraDict is None:
            return None
        
        print(f"Creating Alternate Table for {fieldName}")

        isFaulty = False 
        for ii in range(1, len(values)):

            time = values[ii][0]

            # Downgoing, Upgoing or Perpendicular 
            if time not in spectraDict: 
                continue 
            
            spectra = spectraDict[time]
            
            create_alt_table_query = f"""
            CREATE TABLE IF NOT EXISTS {spectra}_{fieldName} (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                TIME DECIMAL(50,30) NULL, 
            """

            columnName = [] 

            # 47 elements in a row
            for ii in range(1, 48):
                create_alt_table_query += f"ele_{ii} DOUBLE NULL,"
                columnName.append(f"ele_{ii}")
            create_alt_table_query = create_alt_table_query.rstrip(', ') + ");"

            try: 
                cursor.execute(create_alt_table_query)
                conn.commit()  
            except Exception as e:
                print(f"Error creating alternate table for {fieldName}: {str(e)}")
            
            print(f"Inserting Values into Alternate Table for {fieldName}")

            # Loop through each row 
            for ii in range(len(values)):
                cleaned_values = ['Null' if math.isnan(val) else val for val in values[ii]]
                concatValues = ', '.join(map(str, cleaned_values))
                query = f"INSERT INTO {spectra}_{fieldName} (TIME,{','.join(columnName)}) VALUES ({concatValues});"

                try: 
                    cursor.execute(query)
                    conn.commit()
                except Exception as e:
                    isFaulty = True
                    print(f"{spectra}_{fieldName} Table: Error Inserting values at row {ii}: {str(e)}")

        if isFaulty == False:
            print(f"Successfully Inserted Values into Alternate Table for {fieldName}\n")
        else:
            print(f"Unsuccessfully Inserted Values into Alternate Table for {fieldName}\n")

        # Commit the changes and close the connection
        cursor.close()
        conn.close()
    
    except mysql.connector.Error as err:
        print(f"Error pushing to database: {err}")

    finally:
        # Ensure the connection is closed in case of an exception
        if 'conn' in locals():
            conn.close()


def CreateAltAndInsertPerpendicularTable(values):
    """ A function that takes creates/update another table for perpendicular values """

    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        print(f"Creating Alternate Table for Perpendicular Values")

        create_alt_table_query = f"""
        CREATE TABLE IF NOT EXISTS perpendicular (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            TIME DECIMAL(50,30) NULL, 
        """

        columnName = [] 

        # 47 elements in a row
        for i in range(1, 48):
            create_alt_table_query += f"ele_{i} DOUBLE NULL,"
            columnName.append(f"ele_{i}")
        create_alt_table_query = create_alt_table_query.rstrip(', ') + ");"

        try: 
            cursor.execute(create_alt_table_query)
            conn.commit()  
        except Exception as e:
            print(f"Error creating table for perpendicular values: {str(e)}")

        print(f"Inserting Values into Alternate Table for Perpendicular Values")
            
        # Loop through each row 
        isFaulty = False
        for ii in range(len(values)):
            cleaned_values = ['Null' if math.isnan(val) else val for val in values[ii]]
            concatValues = ', '.join(map(str, cleaned_values))
            query = f"INSERT INTO perpendicular (TIME,{','.join(columnName)}) VALUES ({concatValues});"

            try: 
                cursor.execute(query)
                conn.commit()
            except Exception as e:
                isFaulty = True 
                print(f"Perpendicular Table: Error Inserting values at row {ii} {query}: {str(e)}")

        if isFaulty == False:
            print(f"Successfully Inserted Values into Alternate Table for Perpendicular Values\n")

        # Commit the changes and close the connection
        cursor.close()
        conn.close()
    
    except mysql.connector.Error as err:
        print(f"Error pushing to database: {err}")

    finally:
        # Ensure the connection is closed in case of an exception
        if 'conn' in locals():
            conn.close()


def FormatValue(values : list, column : str):
    """ A function that returns a list in the form of the correct precision """

    values_updated = []

    for value in values:
        precision = 30 if column == "TIME" else 7 

        if isinstance(value, list):
            formatted_value = [decimal.Decimal("{:.{}f}".format(sub_value, precision)) for sub_value in value]
        elif np.isnan(value):
            formatted_value = 'NULL'
        else:
            formatted_value = decimal.Decimal("{:.{}f}".format(value, precision))

        values_updated.append(formatted_value)

    return values_updated


def CreateTableQuery(varDict: dict, fileName: str):
    """ A function that generates a query which creates a table if it does not exist and creates the columns  """

    # Store Field who are not list of list 
    mainTableColumns = []

    # Create table and columns 
    query = f"CREATE TABLE IF NOT EXISTS {fileName} (ID INT AUTO_INCREMENT PRIMARY KEY, "

    for column_name, column_data in varDict.items():

        # Skip columns with list of lists
        if isinstance(column_data, np.ndarray) and any(isinstance(item, np.ndarray) for item in column_data):
            continue
        
        # Map numpy data types to MySQL data types
        mysql_data_type = ""

        # Add more decimal places for TIME
        if column_name == "TIME":
            mysql_data_type = 'DECIMAL(50,30)'
        else: 
            data_type = str(column_data.dtype)
            if 'int' in data_type:
                mysql_data_type = 'INT'
            elif 'float' in data_type:
                mysql_data_type = 'DECIMAL(50,30)'
            elif 'datetime' in data_type:
                mysql_data_type = 'DATETIME'
            else:
                # Default to VARCHAR for strings
                mysql_data_type = 'VARCHAR(255)'  

        query += f"{column_name} {mysql_data_type}, "

        mainTableColumns.append(column_name)

    return (query.rstrip(', ') + ")", mainTableColumns)


def InsertToReferenceTable(varDict : dict, fileName : str):
    """ A function that inserts spectra table names and time into a reference table. """

    time = varDict.get('TIME')
    
    if time is None:
        print(f"Error: 'TIME' not found in {fileName}.")
        return
    
        # Connecting to MySQL database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Creating a reference table in MySQL
        create_table_query = """CREATE TABLE IF NOT EXISTS Time_Reference (
                                TIME DECIMAL(50, 30),
                                SPECTRA_TABLE VARCHAR(255)
                               )"""
        try: 
            cursor.execute(create_table_query)
            conn.commit()
        except Exception as e:
            print(f"Reference Table: Error Creating Reference Table: {str(e)}")
        
        # Inserting values into the reference table
        for time_value in time:
            insert_query = "INSERT INTO Time_Reference (TIME, SPECTRA_TABLE) VALUES (%s, %s)"
            cursor.execute(insert_query, (time_value, fileName))
            conn.commit()

        print("Time references created successfully.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def BinFileConverter(readFileDir, saveFileLocation):
    """ A function that reads .bin files and place the data into a .txt file """

    data_list = []  

    with open(readFileDir, 'rb') as file:
        while True:
            binary_data = file.read(struct.calcsize('d'))
            if not binary_data:
                break  # End of file reached

            # Unpack the binary data into variables
            unpacked_data = struct.unpack('d', binary_data)

            # Convert the unpacked data to a list
            data_as_list = list(unpacked_data)

            # Append the list to the data_list
            data_list.append(data_as_list)

    now = datetime.datetime.now()

    with open(saveFileLocation + now.strftime("%Y%m%d_%H%M"), 'w') as file:
        # Iterate through the list and write each integer to a new line
        for number in data_list:
            file.write(str(number) + '\n')


if __name__ == "__main__":

    path = os.path.expanduser("~/Desktop")

    try:
        cdf_files = glob.glob(os.path.join(path, '*.cdf'))
    except Exception as e:
        print(f"An exception of type {type(e).__name__} occurred when searching for CDF Files: {e}")
    else: 
        if len(cdf_files) == 0:
            print(f"No CDF files detected in path:{path}")
        
        for file in cdf_files: 

            #  Step 1: Get File path 
            fileDir = os.path.basename(file)
            fileName = os.path.splitext(fileDir)[0]
            print(f"\nProcessing file: {fileDir}")

            # Step 2: Get Variables and store it in a dictionary
            varDict = GetZVariables(file)

            # Step 3: Push to DombeckDB 
            PushToDataBase(varDict,fileName)
            
            # Step 4: Insert to Reference Table 
            InsertToReferenceTable(varDict, fileName)
        
        print(f"All cdf files in directory {path} successfully inserted into database\n")

    # GetCDFfiles(os.path.expanduser("~/Desktop"))
    # BinFileConverter('/Users/Bryan/Desktop/Dombeck/PythonScript/19.8e6ElecDng_vpara.bin','/Users/Bryan/desktop/')
