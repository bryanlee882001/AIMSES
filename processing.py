from typing import Any, Dict, List, Tuple
import query_from_db
import numpy as np
import statistics


def processQueryData(data: Dict[str, Any], queried_list_of_dict: List[Dict[str, Any]]) -> Tuple[List[str], Dict[str, List[str]]]:
    """A function that processes Data based on queried results (which are stored in dictionary format)"""

    # Store the list of time to obtain spectra values
    list_of_time: List[float] = []

    # Loop through array of dictionaries to get the TIME 
    for i in range(len(queried_list_of_dict)):

        if not queried_list_of_dict[i]["TIME"]:
            continue 

        # Get Time from list of dictionary and append to a list
        list_of_time.append(queried_list_of_dict[i]["TIME"])

    # If No Time is Extracted
    if (len(list_of_time) == 0):
        return [], {}
    
    yAxisQuery: Dict[str, List[str]] = { "Downward" : [], "Upward" : [], "Mirroring" : []}
    
    if "Spectra" in data: 
        if data["Spectra"][0]: 
            spectra: str = data["Spectra"][0]

        # Loop over each time in the list_of_time
        for time in list_of_time:

            if spectra == "Downward":
                # get el_0_lc and el_180_lc for upgoing 
                yAxisQuery[spectra].append("SELECT * FROM DOWNGOING WHERE TIME = %s")

            elif spectra == "Upward":
                # get el_0_lc and el_180_lc for downgoing
                yAxisQuery[spectra].append("SELECT * FROM UPGOING WHERE TIME = %s")

            elif spectra == "Mirroring":
                # get perpendicular (el_90_lcp12 + el_270_lcp12 / 2)
                yAxisQuery[spectra].append("SELECT * FROM PERPENDICULAR WHERE TIME = %s")

        # Compute Query 
        return yAxisQuery, list_of_time

    return 0



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



def getSpectraTablesFromTime(list_of_time: list):
    """A function that searches a reference table and finds the spectra tables based on the given list of times """

    # Construct the SQL query with the IN clause
    query = "SELECT * FROM Time_Reference WHERE TIME IN (%s)"
    placeholders = ', '.join(['%s'] * len(list_of_time))
    query = query % placeholders

    # Query Data in the form of tuples
    data = query_from_db.queryDataTuples(query, list_of_time)

    return data
    


        
        


