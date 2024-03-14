import app


# A function that processes Data based on queried results (which are stored in dictionary format)
def processQueryData(data, queried_list_of_dict):

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
    
    time_query = "SELECT Spectra_Table, TIME FROM Time_Reference WHERE "
    for i in range(len(list_of_time)):
        if (i < len(list_of_time)-1):
            time_query += f" TIME = {list_of_time[i]} OR"
        else:
            time_query += f" TIME = {list_of_time[i]}"

    # Get the list of dictionaries (each with Spectra_Table and Time given)
    list_of_times = app.queryData(time_query)

    # Query Spectral Data 
    spectra_data = getTimeFromTables(data, list_of_times)


    return spectra_data



# A function that goes into each table and finds the required time and 
def getTimeFromTables(data, list_of_times):

    spectra_data = []

    for i in range(len(list_of_times)):

        # Extract Time and Table
        table = list_of_times[i]["Spectra_Table"]
        time = list_of_times[i]["Time"]        

        if (not time or not table):
            continue 

        query = f"SELECT * FROM {table} WHERE TIME = {time} AND "

        # Check User Input on Spectra and Normalization 
        # if "Downward" in data["Spectra"]:
        

        # Spectra (Downward, Upward, Mirroring) produces 3 separate graphs?
        # When querying from each spectra table, 
        
            




        
        


