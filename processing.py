import app
import query_from_db
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
        list_of_time.append(round(queried_list_of_dict[i]["TIME"],7))

    # If No Time is Extracted
    if (len(list_of_time) == 0):
        return 0
    
    for ii in range(len(list_of_time)): 
        spectra = queried_list_of_dict["Spectra"]
        if spectra == "Downward":
            # Go to the downward tables to get el_0_lc and el_180_lc 
            query = f"SELECT * FROM downgoing_el_0_lc WHERE TIME = {list_of_time[ii]}"
            dataDict = query_from_db.queryDataDict(query)

        elif spectra == "Upward":
            query = f"SELECT * FROM downgoing_el_0_lc WHERE TIME = {list_of_time[ii]}"
            dataDict = query_from_db.queryDataDict(query)

        elif spectra == "Perpendicular":
            query = f"SELECT * FROM downgoing_el_0_lc WHERE TIME = {list_of_time[ii]}"
            dataDict = query_from_db.queryDataDict(query)

    # Get List of Spectra Table Names tuples (TIME, Table Name) from Reference Table
    table_names = getSpectraTablesFromTime(list_of_time)
    

    
    # Question:
    # - What should be queried for raw data?
    # - If User selects upgoing and downgoing we put them on the same graph?
    # - If User selects Raw, Energy Flux, and Number Flux we put them on a separate graph? 
        
    # Work Flow:
    # =================================================
    # 1. Query all the results from AIMSES_Norm using selected fields (DONE)
    # 2. Filter results using JEe_0lc, JEe_180lc, ilat (do we reference AIMSES_Norm) and get the remaining time (Normalization: Energy flux, Number flux, Raw)
    # 3. Get the el_90_lcp12, el_270_lcp12, el_0_lc, el_180_lc (Spectra: Downward, Upward, Mirroring) using time 
    

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


        
        


