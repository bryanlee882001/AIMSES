import mysql.connector
import utility

# A function that determines the range for MLT based on user input for querying
def getMLTQuery(string_query, filterData):
    string_query += f"{filterData}"
    return string_query 
    # minRange = filterData[0]
    # maxRange = filterData[1]

    # string_query += f"MLT BETWEEN {minRange} AND {maxRange} AND "


# A function that determines the range for ILAT based on user input for querying
def getILATQuery(string_query, filterData):
    
    if len(filterData) == 0:
        return string_query
 
    if filterData["Range"] == "Lesser Than":
        lesserThanValue = utility.checkNumInput(filterData["lesserThanValue"])
        hemisphere = filterData["Hemisphere"]

        if hemisphere == "Northern Hemisphere" and 0 <= lesserThanValue <= 90:
            string_query += f"ILAT < {lesserThanValue} AND "
        elif hemisphere == "Southern Hemisphere" and -90 <= lesserThanValue <= 0:
            string_query += f"ILAT < {lesserThanValue} AND "
        elif hemisphere == "Either" and 0 <= abs(lesserThanValue) == lesserThanValue <= 90:
            string_query += f"ILAT < {lesserThanValue} AND "
        else:
            raise ValueError("Invalid range for 'Lesser than' type")
        return string_query

    if filterData["Range"] == "Greater Than":
        greaterThanValue = utility.checkNumInput(filterData["greaterThanValue"])
        hemisphere = filterData["Hemisphere"]

        if hemisphere == "Northern Hemisphere" and 0 <= greaterThanValue <= 90:
            string_query += f"ILAT > {greaterThanValue} AND "
        elif hemisphere == "Southern Hemisphere" and -90 <= greaterThanValue <= 0:
            string_query += f"ILAT > {greaterThanValue} AND "
        elif hemisphere == "Either" and 0 <= minRange == abs(greaterThanValue) <= 90:
            string_query += f"ILAT > {greaterThanValue} AND "
        else:
            raise ValueError("Invalid range for 'Between' type")
        return string_query
        
    
    if filterData["Range"] == "Between":
        minRange = utility.checkNumInput(filterData["minRange"])            
        maxRange = utility.checkNumInput(filterData["maxRange"])
        hemisphere = filterData["Hemisphere"]

        if hemisphere == "Northern Hemisphere" and 0 <= minRange < maxRange <= 90:
            string_query += f"ILAT BETWEEN {minRange} AND {maxRange} AND "
        elif hemisphere == "Southern Hemisphere" and -90 <= minRange < maxRange <= 0:
            string_query += f"ILAT BETWEEN {minRange} AND {maxRange} AND "
        elif hemisphere == "Either" and 0 <= minRange == abs(minRange) < maxRange == abs(maxRange) <= 90:
            string_query += f"ILAT BETWEEN {minRange} AND {maxRange} AND " 
        else:
            raise ValueError("Invalid range for 'Between' type")
        return string_query
        
    raise ValueError("No hemisphere selected")


# A function that determines the range for ALT based on user input for querying
def getALTQuery(string_query, filterData):
    
    if len(filterData) == 0:
        return string_query
    
    if filterData["Range"] == "Lesser Than":
        maxRange = float(filterData["lesserThanValue"])
        string_query += f"ALT < {maxRange} AND "
        return string_query 
    
    if filterData["Range"] == "Greater Than":
        minRange = float(filterData["greaterThanValue"])
        string_query += f"ALT > {minRange} AND "
    
    if filterData["Range"] == "Between":
        minRange = float(filterData["minRange"])
        maxRange = float(filterData["maxRange"])

        if minRange < maxRange:
            string_query += f"ALT BETWEEN {minRange} AND {maxRange} AND "
        else:
            raise ValueError("Minimum Range cannot be more than Maximum Range") 
        return string_query

    raise ValueError("No Range Selected")


# A function that determines the range for SZA based on user input for querying
def getSZAQuery(string_query, filterData):

    if len(filterData) == 0:
        return string_query
    
    if filterData["Range"] == "lesserThanValue":
        maxRange = float(filterData["maxRange"])
        if 0 <= maxRange <= 180:
            string_query += f"SZA < {maxRange} AND "
        return string_query 
    
    if filterData["Range"] == "greaterThanValue":
        minRange = float(filterData["minRange"])
        if 0 <= minRange <= 180:
            string_query += f"SZA > {minRange} AND "
        return string_query 
    
    if filterData["Range"] == "Between":
        minRange = float(filterData[0])
        maxRange = float(filterData[1])
        if 0 <= minRange < maxRange <= 180: 
            string_query += f"SZA BETWEEN {minRange} AND {maxRange} AND "
        return string_query

    raise ValueError("No Range Selected")


# A function that determines the range for F10.7 based on user input for querying
def getF107Query(string_query, filterData):
    
    if len(filterData) == 0:
        return string_query
    
    for i in range(len(filterData)):
        if filterData[i] == "Lesser Than":
            maxRange = float(filterData[0])
            string_query += f"F107 < {maxRange} AND "
            return string_query 
        
        if filterData[i] == "Greater Than":
            minRange = float(filterData[0])
            string_query += f"F107 > {minRange} AND "
        
        if filterData[i] == "Between":
            minRange = float(filterData[0])
            maxRange = float(filterData[1])

            if minRange < maxRange:
                string_query += f"F107 BETWEEN {minRange} AND {maxRange} AND "
            else:
               raise ValueError("Minimum Range cannot be more than Maximum Range") 
            return string_query

    raise ValueError("No Range Selected")


# A function that determines the range for EFLUX based on user input for querying 
def getEFLUXQuery(string_query, filterData):
    return string_query 


# A function that determines the range for NFLUX based on user input for querying 
def getNFLUXQuery(string_query, filterData):
    return string_query 


# A function that determines the range for Conjugate SZA based on user input for querying 
def getCONJUGATESZAQuery(string_query, filterData):
    return string_query 


# A function that determines the range for KP based on user input for querying 
def getKPQuery(string_query, filterData):
    return string_query 


# A function that determines the range for AE based on user input for querying 
def getAEQuery(string_query, filterData):

    if len(filterData) == 0:
        return string_query
    
    for i in range(len(filterData)):
        if filterData[i] == "Lesser Than":
            maxRange = float(filterData[0])
            if 0 <= maxRange <= 180:
                string_query += f"AE < {maxRange} AND "
            return string_query 
        
        if filterData[i] == "Greater Than":
            minRange = float(filterData[0])
            string_query += f"AE > {minRange} AND "
            if 0 <= minRange <= 180:
                string_query += f"AE < {maxRange} AND "
            return string_query 
        
        if filterData[i] == "Between":
            minRange = float(filterData[0])
            maxRange = float(filterData[1])
            if 0 <= minRange < maxRange <= 180: 
                string_query += f"AE BETWEEN {minRange} AND {maxRange} AND "
            return string_query

    raise ValueError("No Range Selected")


# A function that determines the range for DST based on user input for querying 
def getDSTQuery(string_query, filterData):

    if len(filterData) == 0:
        return string_query
    
    for i in range(len(filterData)):
        if filterData[i] == "Lesser Than":
            maxRange = float(filterData[0])
            if 0 <= maxRange <= 180:
                string_query += f"DST < {maxRange} AND "
            return string_query 
        
        if filterData[i] == "Greater Than":
            minRange = float(filterData[0])
            string_query += f"DST > {minRange} AND "
            if 0 <= minRange <= 180:
                string_query += f"DST < {maxRange} AND "
            return string_query 
        
        if filterData[i] == "Between":
            minRange = float(filterData[0])
            maxRange = float(filterData[1])
            if 0 <= minRange < maxRange <= 180: 
                string_query += f"DST BETWEEN {minRange} AND {maxRange} AND "
            return string_query

    raise ValueError("No Range Selected")


# A function that determines the range for Newell Flux based on user input for querying 
def getNEWELLFLUXQuery(string_query, filterData):

    if len(filterData) == 0:
        return string_query
    
    for i in range(len(filterData)):
        if filterData[i] == "Lesser Than":
            maxRange = float(filterData[0])
            if 0 <= maxRange <= 180:
                string_query += f"NEWELL_FLUX < {maxRange} AND "
            return string_query 
        
        if filterData[i] == "Greater Than":
            minRange = float(filterData[0])
            string_query += f"NEWELL_FLUX > {minRange} AND "
            if 0 <= minRange <= 180:
                string_query += f"NEWELL_FLUX < {maxRange} AND "
            return string_query 
        
        if filterData[i] == "Between":
            minRange = float(filterData[0])
            maxRange = float(filterData[1])
            if 0 <= minRange < maxRange <= 180: 
                string_query += f"NEWELL_FLUX BETWEEN {minRange} AND {maxRange} AND "
            return string_query

    raise ValueError("No Range Selected")


# A function that determines the range for LCA based on user input for querying 
def getLCAQuery(string_query, filterData):

    if len(filterData) == 0:
        return string_query
    
    for i in range(len(filterData)):
        if filterData[i] == "Lesser Than":
            maxRange = float(filterData[0])
            if 0 <= maxRange <= 180:
                string_query += f"SZA < {maxRange} AND "
            return string_query 
        
        if filterData[i] == "Greater Than":
            minRange = float(filterData[0])
            string_query += f"SZA > {minRange} AND "
            if 0 <= minRange <= 180:
                string_query += f"SZA < {maxRange} AND "
            return string_query 
        
        if filterData[i] == "Between":
            minRange = float(filterData[0])
            maxRange = float(filterData[1])
            if 0 <= minRange < maxRange <= 180: 
                string_query += f"SZA BETWEEN {minRange} AND {maxRange} AND "
            return string_query

    raise ValueError("No Range Selected")


# A function that determines the range for LCA based on user input for querying 
def getMECHSQuery(string_query, filterData):
    return string_query 


# A function that creates a query based on user input
def createQuery(dataDict):

    string_query = 'SELECT * FROM AIMSES_Norm WHERE '

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

    return string_query 







