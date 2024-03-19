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
    

    # Downward: el_0_lc for iLat >0 and el_180_lc for iLat <0
    if ("Downward" in data["Spectra"]):

        # Downgoing, Energy Flux: JEe_0lc for iLat >0 and JEe_180lc for iLat <0  
        if (data["Normalization"] == "Energy Flux"): 
            return 
        
        # Downgoing, Number Flux: Je_0lc for iLat >0 and Je_180lc for iLat <0
        if (data["Normalization"] == "Number Flux"): 
            return 
        
        # Downgoing, Raw: ? 
        if (data["Normalization"] == "Raw"): 
            return  
        


    # Upward: el_0_lc for iLat <0 and el_180_lc for iLat >0
    if ("Upward" in data["Spectra"]):

        # Upward, Energy Flux: JEe_0lc for iLat >0 and JEe_180lc for iLat <0  
        if (data["Normalization"] == "Energy Flux"): 
            return 
        
        # Upward, Number Flux: Je_0lc for iLat >0 and Je_180lc for iLat <0
        if (data["Normalization"] == "Number Flux"): 
            return 
        
        # Upward, Raw/ Perpendicular: ? 
        if (data["Normalization"] == "Raw"): 
            return  
        


    # Mirroring: (el_90_lcp12 + el_270_lcp12) / 2)
    if ("Upward" in data["Spectra"]):

        # Upward, Energy Flux: JEe_0lc for iLat >0 and JEe_180lc for iLat <0  
        if (data["Normalization"] == "Energy Flux"): 
            return 
        
        # Upward, Number Flux: Je_0lc for iLat >0 and Je_180lc for iLat <0
        if (data["Normalization"] == "Number Flux"): 
            return 
        
        # Upward, Raw: ? 
        if (data["Normalization"] == "Raw"): 
            return  
    
    
    # Question:
    # - What should be queired for raw data?
    # - 





    # Get the list of dictionaries (each with Spectra_Table and Time given)
    # list_of_times = app.queryData(time_query)

    # Query Spectral Data 
    # spectra_data = getTimeFromTables(data, list_of_times)

    # return spectra_data



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
        
            




        
        


