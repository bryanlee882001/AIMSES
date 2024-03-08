import utility


# A function that determines the range for MLT based on user input for querying
def getMLTQuery(string_query, filterData):
    if not filterData:
        return string_query

    # Check Range
    rangeType = filterData.get("Range")
    if rangeType == "Between":
        minRange = utility.convertMLT(filterData.get("minRange"))
        maxRange = utility.convertMLT(filterData.get("maxRange"))

        if minRange <= maxRange:
            string_query += f"(MLT BETWEEN {minRange} AND {maxRange}) AND "
        else: 
            # minRange > maxRange
            string_query += f"(MLT BETWEEN {minRange} AND 24.0) OR (MLT BETWEEN 0.0 AND {maxRange}) AND"

    elif rangeType == "Lesser Than":
        lesserThanValue = utility.convertMLT(filterData.get("lesserThanValue"))
        string_query += f"(MLT <= {lesserThanValue}) AND "

    elif rangeType == "Greater Than":
        greaterThanValue = utility.convertMLT(filterData.get("greaterThanValue"))
        string_query += f"(MLT >= {greaterThanValue}) AND "
    
    else:
        raise ValueError("No range type specified")

    return string_query


# A function that determines the range for ILAT based on user input for querying
def getILATQuery(string_query, filterData):

    if not filterData:
        return string_query

    hemisphere = filterData.get("Hemisphere")
    if not hemisphere:
        raise ValueError("No hemisphere selected")

    # Check Range
    rangeType = filterData.get("Range")
    if rangeType == "Lesser Than":
        lesserThanValue = utility.checkNumInput(filterData.get("lesserThanValue"))

        if hemisphere == "Northern Hemisphere" and 0 <= lesserThanValue <= 90:
            string_query += f"(ILAT <= {lesserThanValue}) AND "
        elif hemisphere == "Southern Hemisphere" and -90 <= lesserThanValue <= 0:
            string_query += f"(ILAT <= {lesserThanValue}) AND "
        elif hemisphere == "Either" and 0 <= abs(lesserThanValue) <= 90:
            string_query += f"(ILAT <= {lesserThanValue}) AND "
        else:
            raise ValueError("Invalid range for 'Lesser Than' type")
        return string_query

    if rangeType == "Greater Than":
        greaterThanValue = utility.checkNumInput(filterData.get("greaterThanValue"))

        if hemisphere == "Northern Hemisphere" and 0 <= greaterThanValue <= 90:
            string_query += f"(ILAT >= {greaterThanValue}) AND "
        elif hemisphere == "Southern Hemisphere" and -90 <= greaterThanValue <= 0:
            string_query += f"(ILAT >= {greaterThanValue}) AND "
        elif hemisphere == "Either" and 0 <= abs(greaterThanValue) <= 90:
            string_query += f"(ILAT >= {greaterThanValue}) AND "
        else:
            raise ValueError("Invalid range for 'Greater Than' type")
        return string_query

    if rangeType == "Between":
        minRange = utility.checkNumInput(filterData.get("minRange"))
        maxRange = utility.checkNumInput(filterData.get("maxRange"))

        if hemisphere == "Northern Hemisphere" and 0 <= minRange < maxRange <= 90:
            string_query += f"(ILAT BETWEEN {minRange} AND {maxRange}) AND "
        elif hemisphere == "Southern Hemisphere" and -90 <= minRange < maxRange <= 0:
            string_query += f"(ILAT BETWEEN {minRange} AND {maxRange}) AND "
        elif hemisphere == "Either" and 0 <= abs(minRange) < abs(maxRange) <= 90:
            string_query += f"(ILAT BETWEEN {minRange} AND {maxRange}) AND "
        else:
            raise ValueError("Invalid range for 'Between' type")
        return string_query

    raise ValueError("Invalid or No Range Selected")
    

# A function that determines the range for ALT based on user input for querying
def getALTQuery(string_query, filterData):

    if not filterData:
        # No filter data provided, return the unchanged query
        return string_query
    
    return genericFilterQuery(string_query, filterData, "ALT")


# A function that determines the range for SZA based on user input for querying
def getSZAQuery(string_query, filterData):

    if not filterData:
        # No filter data provided, return the unchanged query
        return string_query
    
    return genericFilterQuery(string_query, filterData, "SZA")


# A function that determines the range for F10.7 based on user input for querying
def getF107Query(string_query, filterData):
    
    if not filterData:
        # No filter data provided, return the unchanged query
        return string_query
    
    return genericFilterQuery(string_query, filterData, "F107")


# A function that determines the range for EFLUX based on user input for querying 
def getEFLUXQuery(string_query, filterData):

    if not filterData:
        # No filter data provided, return the unchanged query
        return string_query
    
    return genericFilterQuery(string_query, filterData, "EFLUX")


# A function that determines the range for NFLUX based on user input for querying 
def getNFLUXQuery(string_query, filterData):

    if not filterData:
        # No filter data provided, return the unchanged query
        return string_query
    
    return genericFilterQuery(string_query, filterData, "NFLUX")


# A function that determines the range for Conjugate SZA based on user input for querying 
def getCONJUGATESZAQuery(string_query, filterData):

    if not filterData:
        # No filter data provided, return the unchanged query
        return string_query
    
    return genericFilterQuery(string_query, filterData, "CONJUGATE_SZA")


# A function that determines the range for KP based on user input for querying 
def getKPQuery(string_query, filterData):

    if not filterData:
        # No filter data provided, return the unchanged query
        return string_query
    
    # Check Range
    rangeType = filterData.get("Range")
    if rangeType == "Lesser Than":
        maxRange = utility.checkNumInput(filterData.get("lesserThanValue"))
        string_query += f"(KP < {maxRange}) AND "
        return string_query 

    elif rangeType == "Greater Than":
        minRange = utility.checkNumInput(filterData.get("greaterThanValue"))
        string_query += f"(KP >= {minRange}) AND "
        return string_query

    elif rangeType == "Between":
        minRange = utility.checkNumInput(filterData.get("minRange"))
        maxRange = utility.checkNumInput(filterData.get("maxRange"))

        if minRange > maxRange:
            raise ValueError("Minimum Range cannot be more than Maximum Range")

        string_query += f"(NFLUX BETWEEN {minRange} AND {maxRange}) AND "
        return string_query

    else:
        raise ValueError("Invalid or No Range Selected")


# A function that determines the range for AE based on user input for querying 
def getAEQuery(string_query, filterData):

    if not filterData:
        # No filter data provided, return the unchanged query
        return string_query
    
    return genericFilterQuery(string_query, filterData, "AE")


# A function that determines the range for DST based on user input for querying 
def getDSTQuery(string_query, filterData):

    if not filterData:
        # No filter data provided, return the unchanged query
        return string_query
    
    return genericFilterQuery(string_query, filterData, "DST")


# A function that determines the range for Newell Flux based on user input for querying 
def getNEWELLFLUXQuery(string_query, filterData):

    if not filterData:
        # No filter data provided, return the unchanged query
        return string_query
    
    return genericFilterQuery(string_query, filterData, "NEWELL_FLUX")


# A function that determines the range for LCA based on user input for querying 
def getLCAQuery(string_query, filterData):

    if not filterData:
        # No filter data provided, return the unchanged query
        return string_query
    
    return genericFilterQuery(string_query, filterData, "LCA")


# A function that determines the range for LCA based on user input for querying 
def getMECHSQuery(string_query, filterData):
    return string_query


def genericFilterQuery(string_query, filterData, column):
    
    # Check Range
    rangeType = filterData.get("Range")
    if rangeType == "Lesser Than":
        maxRange = utility.checkNumInput(filterData.get("lesserThanValue"))
        string_query += f"({column} <= {maxRange}) AND "
        return string_query 

    elif rangeType == "Greater Than":
        minRange = utility.checkNumInput(filterData.get("greaterThanValue"))
        string_query += f"({column} >= {minRange}) AND "
        return string_query

    elif rangeType == "Between":
        minRange = utility.checkNumInput(filterData.get("minRange"))
        maxRange = utility.checkNumInput(filterData.get("maxRange"))

        if minRange > maxRange:
            raise ValueError("Minimum Range cannot be more than Maximum Range")

        string_query += f"({column} BETWEEN {minRange} AND {maxRange}) AND "
        return string_query

    else:
        raise ValueError("Invalid or No Range Selected")
    

# A function that creates a query based on user input
def createQuery(dataDict):

    string_query = 'SELECT * FROM AIMSES_NORM WHERE '

    for key in dataDict: 

        if key == "MLT":
            string_query = getMLTQuery(string_query, dataDict[key])

        elif key == "ILAT":
            string_query = getILATQuery(string_query, dataDict[key])

        elif key == "ALT":
            string_query = getALTQuery(string_query, dataDict[key])

        elif key == "SZA":
            string_query = getSZAQuery(string_query, dataDict[key])

        elif key == "F10.7":
            string_query = getF107Query(string_query, dataDict[key])

        elif key == "EFLUX":
            string_query = getEFLUXQuery(string_query, dataDict[key])
        
        elif key == "NFLUX": 
            string_query = getNFLUXQuery(string_query, dataDict[key])

        elif key == "CONJUGATE SZA": 
            string_query = getCONJUGATESZAQuery(string_query, dataDict[key])

        elif key == "KP": 
            string_query = getKPQuery(string_query, dataDict[key])

        elif key == "AE": 
            string_query = getAEQuery(string_query, dataDict[key])

        elif key == "DST": 
            string_query = getDSTQuery(string_query, dataDict[key])

        elif key == "NEWELL FLUX": 
            string_query = getNEWELLFLUXQuery(string_query, dataDict[key])

        elif key == "LOST CONE ANGLE": 
            string_query = getLCAQuery(string_query, dataDict[key])

        elif key == "MECHANISMS": 
            string_query = getMECHSQuery(string_query, dataDict[key])

    # Remove the last 'AND' if it exists
    if string_query.endswith('AND '):
        string_query = string_query[:-4]

    return string_query 







