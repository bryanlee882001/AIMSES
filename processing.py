import query_from_db
import numpy as np
import statistics
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
    
    dict_of_query = { "Downward" : { "el_0_lc" : [], "el_180_lc" : []},
                      "Upward" : { "el_0_lc" : [], "el_180_lc" : []}, 
                      "Mirroring" : { "perpendicular" : []}}
    
    if "Spectra" in data: 
        spectra = data["Spectra"][0]

        # Loop over each time in the list_of_time
        for time in list_of_time:

            if spectra == "Downward":
                # get el_0_lc and el_180_lc for upgoing 
                dict_of_query[spectra]["el_0_lc"].append(f"SELECT * FROM DOWNGOING_el_0_lc WHERE TIME = {time}")
                dict_of_query[spectra]["el_180_lc"].append(f"SELECT * FROM DOWNGOING_el_180_lc WHERE TIME = {time}")

            elif spectra == "Upward":
                # get el_0_lc and el_180_lc for downgoing
                dict_of_query[spectra]["el_0_lc"].append(f"SELECT * FROM UPGOING_el_0_lc WHERE TIME = {time}")
                dict_of_query[spectra]["el_180_lc"].append(f"SELECT * FROM UPGOING_el_180_lc WHERE TIME = {time}")

            elif spectra == "Mirroring":
                # get perpendicular (el_90_lcp12 + el_270_lcp12 / 2)
                dict_of_query[spectra]["perpendicular"].append(f"SELECT * FROM PERPENDICULAR WHERE TIME = {time}")

        # Compute Query 
        return dict_of_query 

    return 0
                


def getStatistics(data, spectral_data):

    computedValue, computed_el_0_lc, computed_el_180_lc, computed_perpendicular = [], [], [], []

    # Get User's Input on Statistics
    if "Statistics" not in data:
        return 0 
    
    finalSpectraDict = {}

    for spectra, fieldDict in spectral_data.items():
        for field, list_of_spectral_data in fieldDict.items():

            if list_of_spectral_data: 
                final_list_spectral_data = list_of_spectral_data[0]

                # Initialize an empty list to store the sums
                index_values = []

                # Iterate over each sublist in list_of_spectral_data
                for lst in final_list_spectral_data:

                    # Remove the first three and last elements from each sublist
                    lst = lst[3:]
                    # Append the modified sublist to sums
                    index_values.append(lst)

                # Transpose the modified lists to get the values at each index
                transposed_values = zip(*index_values)

                # Initialize empty lists to store the calculated statistics for each index
                statistics_required = data["Statistics"]
                computed_statistics = {stat: [] for stat in statistics_required}

                for elements in transposed_values:
                    
                    if "Mean" in statistics_required:
                        computed_statistics["Mean"].append(np.mean(elements))

                    # Compute standard deviation
                    std_dev = np.std(elements)

                    if "+1\u03c3" in statistics_required:
                        computed_statistics["+1\u03c3" ].append(np.mean(elements) - std_dev)
                    
                    if "-1\u03c3" in statistics_required:
                        computed_statistics["-1\u03c3"].append(np.mean(elements) + std_dev)

                    if "Median" in statistics_required:
                        computed_statistics["Median"].append(statistics.median(elements))

                    if "25%" in statistics_required:
                        computed_statistics["25%"].append(np.percentile(elements, 25))

                    if "75%" in statistics_required:
                        computed_statistics["75%"].append(np.percentile(elements, 75))

                finalSpectraDict[field] = computed_statistics
                
    return finalSpectraDict


def getSpectraTablesFromTime(list_of_time):
    """A function that searches a reference table and finds the spectra tables based on the given list of times """

    # Construct the SQL query with the IN clause
    query = "SELECT * FROM Time_Reference WHERE TIME IN (%s)"
    placeholders = ', '.join(['%s'] * len(list_of_time))
    query = query % placeholders

    # Query Data in the form of tuples
    data = query_from_db.queryDataTuples(query, list_of_time)

    return data
    


        
        


