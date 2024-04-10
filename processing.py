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
    

    dict_of_query = { "Downward" : [],
                      "Upward" : [], 
                      "Mirroring" : []}
    
    if "Spectra" in data: 
        spectra = data["Spectra"][0]

        # Loop over each time in the list_of_time
        for time in list_of_time:

            if spectra == "Downward":
                # get el_0_lc and el_180_lc for upgoing 
                dict_of_query[spectra].append(f"SELECT * FROM DOWNGOING_el_0_lc WHERE TIME = {time}")
                dict_of_query[spectra].append(f"SELECT * FROM DOWNGOING_el_180_lc WHERE TIME = {time}")

            elif spectra == "Upward":
                # get el_0_lc and el_180_lc for downgoing
                dict_of_query[spectra].append(f"SELECT * FROM UPGOING_el_0_lc WHERE TIME = {time}")
                dict_of_query[spectra].append(f"SELECT * FROM UPGOING_el_180_lc WHERE TIME = {time}")

            elif spectra == "Mirroring":
                # get perpendicular (el_90_lcp12 + el_270_lcp12 / 2)
                dict_of_query[spectra].append(f"SELECT * FROM PERPENDICULAR WHERE TIME = {time}")

        # Compute Query 
        return dict_of_query 

    return 0
                


def getStatistics(list_of_spectral_data):

    # Get User's Input on Statistics
    # spectra = data["Statistics"] 


    return 0


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


        
        


