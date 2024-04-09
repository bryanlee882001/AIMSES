import app
import query_from_db
import mysql.connector
from collections import defaultdict


def processQueryData(data, queried_list_of_dict):
    """A function that processes Data based on queried results (which are stored in dictionary format)"""

    # Store the list of time to obtain spectra values
    list_of_time = []

    # Loop through array of dictionaries to get the TIME 
    for i in range(len(queried_list_of_dict)):

        if not queried_list_of_dict[i]["TIME"]:
            continue 

        # Get Time from list of dictionary and append to a list
        list_of_time.append(queried_list_of_dict[i]["TIME"])

    # If No Time is Extracted
    if (len(list_of_time) == 0):
        return 0
    
    spectra = data["Spectra"]
    # Define a mapping of spectra values to table names
    spectra_tables = {
        "Downward": {"el_0_lc": "DOWNGOING_el_0_lc", "el_180_lc": "DOWNGOING_el_180_lc"},
        "Upward": {"el_0_lc": "UPGOING_el_0_lc", "el_180_lc": "UPGOING_el_180_lc"},
        "Perpendicular": {"perpendicular": "PERPENDICULAR"}
    }

    # Loop over each time in the list_of_time
    for time in list_of_time:
        # Get the table names based on the spectra value
        tables = spectra_tables.get(spectra)

        if tables:
            # Iterate over each table and execute the query
            for column, table_name in tables.items():
                query = f"SELECT * FROM {table_name} WHERE TIME = {time}"
                data_dict = query_from_db.queryDataDict(query)
                # Process the data_dict as needed
                # try:
                #     # Connect to MySQL
                #     connection = mysql.connector.connect(**db_config)

                #     # Create cursor
                #     cursor = connection.cursor()

                #     # Execute SQL query
                #     query = "SELECT * FROM your_table"
                #     cursor.execute(query)

                #     # Fetch data as a list of tuples
                #     data = cursor.fetchall()

                #     # Process the data if needed
                #     for row in data:
                #         print(row)  # Example: Print each row

                # except mysql.connector.Error as error:
                #     print("Error fetching data from MySQL:", error)

                # finally:
                #     # Close cursor and connection
                #     if connection.is_connected():
                #         cursor.close()
                #         connection.close()



    # spectra = data["Spectra"]
    # for ii in range(len(list_of_time)): 
        
    #     if spectra == "Downward":
    #         # Go to the downward tables to get el_0_lc and el_180_lc 
    #         query_el_0_lc = f"SELECT * FROM DOWNGOING_el_0_lc WHERE TIME = {list_of_time[ii]}"
    #         query_el_180_lc = f"SELECT * FROM DOWNGOING_el_180_lc WHERE TIME = {list_of_time[ii]}"
    #         dataDict_el_0_lc = query_from_db.queryDataDict(query_el_0_lc)
    #         dataDict_el_180_lc = query_from_db.queryDataDict(query_el_180_lc)

    #     elif spectra == "Upward":
    #         query_el_0_lc = f"SELECT * FROM UPGOING_el_0_lc WHERE TIME = {list_of_time[ii]}"
    #         query_el_180_lc = f"SELECT * FROM GOING_el_180_lc WHERE TIME = {list_of_time[ii]}"
    #         dataDict_el_0_lc = query_from_db.queryDataDict(query_el_0_lc)
    #         dataDict_el_180_lc = query_from_db.queryDataDict(query_el_180_lc)

    #     elif spectra == "Perpendicular":
    #         query = f"SELECT * FROM PERPENDICULAR WHERE TIME = {list_of_time[ii]}"
    #         dataDict = query_from_db.queryDataDict(query)    




def getSpectraTablesFromTime(list_of_time):
    """A function that searches a reference table and finds the spectra tables based on the given list of times """

    # Construct the SQL query with the IN clause
    query = "SELECT * FROM Time_Reference WHERE TIME IN (%s)"
    placeholders = ', '.join(['%s'] * len(list_of_time))
    query = query % placeholders

    # Query Data in the form of tuples
    data = query_from_db.queryDataTuples(query, list_of_time)

    return data
    

def getSpectraTableRows(table_names):
    """A function that queries rows of data in each table based on given time"""

    # Separate Time based on Spectra Tables
    # table_names_dict = defaultdict(list)
    # for time, spectra_table_name in table_names:
    #     table_names_dict[spectra_table_name].append(time)  

    # # Now the dictionary is stored in this format: table_names_dict { spectra_table_name : [time1, time2, time3]}
    # rows_of_spectra_data = []
    # for spectra_table_name, time in table_names_dict.items():
        
    #     # Query the time 
    #     # query = f"SELECT * FROM {spectra_table_name} WHERE TIME IN ({",".join(table_names_dict[spectra_table_name])})"

    #     # Execute query to get data from database in dictionary format 
    #     # table_row_data = query_from_db.queryDataDict(query)

    #     # rows_of_spectra_data.append(table_row_data)

    return 0


        
        


