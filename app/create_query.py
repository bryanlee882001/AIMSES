from app import utility
from typing import Tuple, List, Union


def getTIMEQuery(string_query: str, filterData: dict) -> Tuple[str, List[Union[float, int]]]:
    """A function that determines the range for MLT based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    # Check Range
    rangeType = filterData.get("Range")
    if rangeType == "Between":
        minRange = utility.convertTIMEtoEPOCH(filterData.get("minRange"))
        maxRange = utility.convertTIMEtoEPOCH(filterData.get("maxRange"))

        # Everything between 2 and 22 
        string_query += "(AIMSES_NORM.TIME BETWEEN %s AND %s) AND "
        parameters.extend([minRange, maxRange])

    elif rangeType == "Lesser Than":
        lesserThanValue = utility.convertTIMEtoEPOCH(filterData.get("lesserThanValue"))
        string_query += "(AIMSES_NORM.TIME <= %s) AND "
        parameters.append(lesserThanValue)

    elif rangeType == "Greater Than":
        greaterThanValue = utility.convertTIMEtoEPOCH(filterData.get("greaterThanValue"))
        string_query += "(AIMSES_NORM.TIME >= %s) AND "
        parameters.append(greaterThanValue)

    else:
        raise ValueError("No range type specified")

    return string_query, parameters


def getMLTQuery(string_query: str, filterData: dict) -> Tuple[str, List[Union[float, int]]]:
    """A function that determines the range for MLT based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    # Check Range
    rangeType = filterData.get("Range")
    if rangeType == "Between":
        minRange = utility.convertMLT(filterData.get("minRange"))
        maxRange = utility.convertMLT(filterData.get("maxRange"))

        if minRange <= maxRange:
            # Everything between 2 and 22 
            string_query += "(AIMSES_NORM.MLT BETWEEN %s AND %s) AND "
            parameters.extend([minRange, maxRange])
        else: 
            # minRange > maxRange
            string_query += "(AIMSES_NORM.MLT BETWEEN %s AND 24.0) OR (MLT BETWEEN 0.0 AND %s) AND"
            parameters.extend([minRange, maxRange])

    elif rangeType == "Lesser Than":
        lesserThanValue = utility.convertMLT(filterData.get("lesserThanValue"))
        string_query += "(AIMSES_NORM.MLT <= %s) AND "
        parameters.append(lesserThanValue)

    elif rangeType == "Greater Than":
        greaterThanValue = utility.convertMLT(filterData.get("greaterThanValue"))
        string_query += "(AIMSES_NORM.MLT >= %s) AND "
        parameters.append(greaterThanValue)

    else:
        raise ValueError("No range type specified")

    return string_query, parameters


def getILATQuery(string_query: str, filterData: dict) -> Tuple[str, List[Union[float, int]]]:
    """A function that determines the range for ILAT based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    hemisphere = filterData.get("Hemisphere")
    if not hemisphere:
        raise ValueError("No hemisphere selected")

    # Check Range
    rangeType = filterData.get("Range")
    if rangeType == "Lesser Than":
        lesserThanValue = utility.checkNumInput(filterData.get("lesserThanValue"))

        if hemisphere == "Northern Hemisphere" and 0 <= lesserThanValue <= 90:
            string_query += "(AIMSES_NORM.ILAT <= %s) AND "
            parameters.append(lesserThanValue)
        elif hemisphere == "Southern Hemisphere" and -90 <= lesserThanValue <= 0:
            string_query += "(AIMSES_NORM.ILAT <= %s) AND "
            parameters.append(lesserThanValue)
        elif hemisphere == "Either" and 0 <= abs(lesserThanValue) <= 90:
            string_query += "(AIMSES_NORM.ILAT <= %s) AND "
            parameters.append(lesserThanValue)
        else:
            raise ValueError("Invalid range for 'Lesser Than' type")

    if rangeType == "Greater Than":
        greaterThanValue = utility.checkNumInput(filterData.get("greaterThanValue"))

        if hemisphere == "Northern Hemisphere" and 0 <= greaterThanValue <= 90:
            string_query += "(AIMSES_NORM.ILAT >= %s) AND "
            parameters.append(greaterThanValue)
        elif hemisphere == "Southern Hemisphere" and -90 <= greaterThanValue <= 0:
            string_query += "(AIMSES_NORM.ILAT >= %s) AND "
            parameters.append(greaterThanValue)
        elif hemisphere == "Either" and 0 <= abs(greaterThanValue) <= 90:
            string_query += "(AIMSES_NORM.ILAT >= %s) AND "
            parameters.append(greaterThanValue)
        else:
            raise ValueError("Invalid range for 'Greater Than' type")

    if rangeType == "Between":
        minRange = utility.checkNumInput(filterData.get("minRange"))
        maxRange = utility.checkNumInput(filterData.get("maxRange"))

        if hemisphere == "Northern Hemisphere" and 0 <= minRange < maxRange <= 90:
            string_query += "(AIMSES_NORM.ILAT BETWEEN %s AND %s) AND "
            parameters.extend([minRange, maxRange])
        elif hemisphere == "Southern Hemisphere" and -90 <= minRange < maxRange <= 0:
            string_query += "(AIMSES_NORM.ILAT BETWEEN %s AND %s) AND "
            parameters.extend([minRange, maxRange])
        elif hemisphere == "Either" and 0 <= abs(minRange) < abs(maxRange) <= 90:
            string_query += "(AIMSES_NORM.ILAT BETWEEN %s AND %s) AND "
            parameters.extend([minRange, maxRange])
        else:
            raise ValueError("Invalid range for 'Between' type")

    return string_query, parameters


def getALTQuery(string_query: str, filterData: dict) -> Tuple[str, List[Union[float, int]]]:
    """A function that determines the range for ALT based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    return genericFilterQuery(string_query, filterData, "AIMSES_NORM.ALT", parameters)


def getSZAQuery(string_query: str, filterData: dict) -> Tuple[str, List[Union[float, int]]]:
    """A function that determines the range for SZA based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    return genericFilterQuery(string_query, filterData, "AIMSES_NORM.SZA", parameters)


def getF107Query(string_query: str, filterData: dict) -> Tuple[str, List[Union[float, int]]]:
    """A function that determines the range for F10.7 based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    return genericFilterQuery(string_query, filterData, "AIMSES_NORM.F107", parameters)


def getEFLUXQuery(string_query: str, filterData: dict) -> Tuple[str, List[Union[float, int]]]:
    """A function that determines the range for EFLUX based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    return genericFilterQuery(string_query, filterData, "AIMSES_NORM.EFLUX", parameters)


def getNFLUXQuery(string_query: str, filterData: dict) -> Tuple[str, List[Union[float, int]]]:
    """A function that determines the range for NFLUX based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    return genericFilterQuery(string_query, filterData, "AIMSES_NORM.NFLUX", parameters)


def getCONJUGATESZAQuery(string_query: str, filterData: dict) -> Tuple[str, List[Union[float, int]]]:
    """A function that determines the range for Conjugate SZA based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    return genericFilterQuery(string_query, filterData, "AIMSES_NORM.CONJUGATE_SZA", parameters)


def getKPQuery(string_query: str, filterData: dict) -> Tuple[str, List[Union[float, int]]]:
    """A function that determines the range for KP based on user input for querying"""
    if not filterData:
        # No filter data provided, return the unchanged query
        return string_query, []

    parameters = []
    # Check Range
    rangeType = filterData.get("Range")
    if rangeType == "Lesser Than":
        maxRange = utility.checkNumInput(filterData.get("lesserThanValue"))
        string_query += "(AIMSES_NORM.KP < %s) AND "
        parameters.append(maxRange)

    elif rangeType == "Greater Than":
        minRange = utility.checkNumInput(filterData.get("greaterThanValue"))
        string_query += "(AIMSES_NORM.KP >= %s) AND "
        parameters.append(minRange)

    elif rangeType == "Between":
        minRange = utility.checkNumInput(filterData.get("minRange"))
        maxRange = utility.checkNumInput(filterData.get("maxRange"))

        if minRange > maxRange:
            raise ValueError("Minimum Range cannot be more than Maximum Range")

        string_query += "(AIMSES_NORM.KP BETWEEN %s AND %s) AND "
        parameters.extend([minRange, maxRange])

    else:
        raise ValueError("Invalid or No Range Selected")

    return string_query, parameters


def getAEQuery(string_query: str, filterData: dict) -> Tuple[str, List[float]]:
    """A function that determines the range for AE based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    return genericFilterQuery(string_query, filterData, "AIMSES_NORM.AE", parameters)


def getDSTQuery(string_query: str, filterData: dict) -> Tuple[str, List[float]]:
    """A function that determines the range for DST based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    return genericFilterQuery(string_query, filterData, "AIMSES_NORM.DST", parameters)


def getNEWELLFLUXQuery(string_query: str, filterData: dict) -> Tuple[str, List[float]]:
    """A function that determines the range for Newell Flux based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    return genericFilterQuery(string_query, filterData, "AIMSES_NORM.NEWELL_FLUX", parameters)


def getLCAQuery(string_query: str, filterData: dict) -> Tuple[str, List[float]]:
    """A function that determines the range for LCA based on user input for querying"""
    if not filterData:
        return string_query, []

    parameters = []
    return genericFilterQuery(string_query, filterData, "AIMSES_NORM.LCA", parameters)


def getMECHSQuery(string_query: str, filterData: dict) -> Tuple[str, List[float]]:
    """A function that determines the range for MECHS based on user input for querying"""
    if len(filterData) != 1:
        return string_query, []

    checkedMECH = filterData[0]
    parameters = []
    if checkedMECH == "QS Only":
        string_query += "(AIMSES_NORM.MECHS = -1) AND "
    elif checkedMECH == "QS Dominant":
        string_query += "(AIMSES_NORM.MECHS = -1 OR MECHS = 1) AND "
    elif checkedMECH == "Alf Only":
        string_query += "(AIMSES_NORM.MECHS = -2) AND "
    elif checkedMECH == "Alf Dominant":
        string_query += "(AIMSES_NORM.MECHS = -2 OR MECHS = 2) AND "
    elif checkedMECH == "WS Only":
        string_query += "(AIMSES_NORM.MECHS = -4) AND "
    elif checkedMECH == "WS Dominant":
        string_query += "(AIMSES_NORM.MECHS = -4 OR MECHS = 4) AND "
    elif checkedMECH == "QS + Alf":
        string_query += "(AIMSES_NORM.MECHS = 3) AND "
    elif checkedMECH == "QS + WS":
        string_query += "(AIMSES_NORM.MECHS = 5) AND "
    elif checkedMECH == "Alf + WS":
        string_query += "(AIMSES_NORM.MECHS = 6) AND "
    elif checkedMECH == "Alf + WS + QS":
        string_query += "(AIMSES_NORM.MECHS = 7) AND "
    elif checkedMECH == "Any QS":
        string_query += "(AIMSES_NORM.MECHS = -1 OR AIMSES_NORM.MECHS = 1 OR AIMSES_NORM.MECHS = 3 OR AIMSES_NORM.MECHS = 5 OR AIMSES_NORM.MECHS = 7) AND "
    elif checkedMECH == "Any Alf":
        string_query += "(AIMSES_NORM.MECHS = -2 OR AIMSES_NORM.MECHS = 2 OR AIMSES_NORM.MECHS = 3 OR AIMSES_NORM.MECHS = 6 OR AIMSES_NORM.MECHS = 7) AND "
    elif checkedMECH == "Any WS":
        string_query += "(AIMSES_NORM.MECHS = -4 OR AIMSES_NORM.MECHS = 4 OR AIMSES_NORM.MECHS = 5 OR AIMSES_NORM.MECHS = 6 OR AIMSES_NORM.MECHS = 7) AND "
    elif checkedMECH == "Weak":
        string_query += "(AIMSES_NORM.MECHS = 0) AND "
    elif checkedMECH == "Any Intense":
        string_query += "(NOT AIMSES_NORM.MECHS = 0) AND "
    else:
        return string_query, []

    return string_query, parameters


def getMissionTimeQuery(string_query: str, filterData: str) -> Tuple[str, List[float]]:
    """A function that determines the range for Time based on Mission"""
    parameters = []
    if filterData == "Early Mission":
        string_query += "(TIME BETWEEN %s AND %s) AND "
        parameters.extend([843419539, 1023754226])
    if filterData == "Late Mission":
        string_query += "(TIME BETWEEN %s AND %s) AND "
        parameters.extend([1023759079, 1241086949])

    return string_query, parameters


def genericFilterQuery(string_query: str, filterData: dict, column: str, parameters: List[float]) -> Tuple[str, List[float]]:
    """A helper function for selections that only have Range (Between, less than, greater than)"""
    # Check Range
    rangeType = filterData.get("Range")
    if rangeType == "Lesser Than":
        maxRange = utility.checkNumInput(filterData.get("lesserThanValue"))
        string_query += f"({column} <= %s) AND "
        parameters.append(maxRange)

    elif rangeType == "Greater Than":
        minRange = utility.checkNumInput(filterData.get("greaterThanValue"))
        string_query += f"({column} >= %s) AND "
        parameters.append(minRange)

    elif rangeType == "Between":
        minRange = utility.checkNumInput(filterData.get("minRange"))
        maxRange = utility.checkNumInput(filterData.get("maxRange"))

        if minRange > maxRange:
            raise ValueError("Minimum Range cannot be more than Maximum Range")

        string_query += f"({column} BETWEEN %s AND %s) AND "
        parameters.extend([minRange, maxRange])

    else:
        raise ValueError("Invalid or No Range Selected")

    return string_query, parameters


def createQueryForMission(dataDict: dict) -> Tuple[str, str, List[float], List[float]]:
    """A function that creates queries based on user input for mission"""
    filter_functions = {
        "TIME": getTIMEQuery,
        "MLT": getMLTQuery,
        "ILAT": getILATQuery,
        "ALT": getALTQuery,
        "SZA": getSZAQuery,
        "F10.7": getF107Query,
        "EFLUX": getEFLUXQuery,
        "NFLUX": getNFLUXQuery,
        "CONJUGATE SZA": getCONJUGATESZAQuery,
        "KP": getKPQuery,
        "AE": getAEQuery,
        "DST": getDSTQuery,
        "SOLAR WIND DRIVING": getNEWELLFLUXQuery,
        "LCA": getLCAQuery,
        "MECHANISMS": getMECHSQuery
    }
    
    parameters = []

    # Compute Early Mission 
    string_query = "SELECT SUM(CASE WHEN (TIME BETWEEN %s AND %s) AND "
    parameters.append(843419539)
    parameters.append(1023754226)

    for key, func in filter_functions.items():
        if key in dataDict:
            string_query, params = func(string_query, dataDict[key])
            parameters.extend(params)

    if string_query.endswith('AND '):
        string_query = string_query[:-4]

    string_query += "THEN 1 ELSE 0 END) AS EARLY_MISSION_COUNT, "


    # Compute Late Mission 
    string_query += "SUM(CASE WHEN (TIME BETWEEN %s AND %s) AND "
    parameters.append(1023759079)
    parameters.append(1241086949)

    for key, func in filter_functions.items():
        if key in dataDict:
            string_query, params = func(string_query, dataDict[key])
            parameters.extend(params)

    if string_query.endswith('AND '):
        string_query = string_query[:-4]

    string_query += "THEN 1 ELSE 0 END) AS LATE_MISSION_COUNT FROM AIMSES_NORM"

    return string_query, parameters


def createJoinQuery(dataDict: dict): 
    """
    Creates a join query between time values in AIMSES_NORM and UPGOING/DOWNGOING/PERP
    for SQLite syntax.
    """

    filter_functions = {
        "TIME": getTIMEQuery,
        "MLT": getMLTQuery,
        "ILAT": getILATQuery,
        "ALT": getALTQuery,
        "SZA": getSZAQuery,
        "F10.7": getF107Query,
        "EFLUX": getEFLUXQuery,
        "NFLUX": getNFLUXQuery,
        "CONJUGATE SZA": getCONJUGATESZAQuery,
        "KP": getKPQuery,
        "AE": getAEQuery,
        "DST": getDSTQuery,
        "SOLAR WIND DRIVING": getNEWELLFLUXQuery,
        "LCA": getLCAQuery,
        "MECHANISMS": getMECHSQuery,
        "Mission": getMissionTimeQuery
    }

    if dataDict["Spectra"][0] == "Downward":
        spectral_table_name = "DOWNGOING"
    elif dataDict["Spectra"][0] == "Upward":
        spectral_table_name = "UPGOING"
    else:
        spectral_table_name = "PERPENDICULAR"
    
    # Updated SQLite syntax
    el_de_query = f"""SELECT el_de.*
                     FROM AIMSES_NORM 
                     JOIN el_de
                     ON AIMSES_NORM.ID = el_de.TIME_ID
                     WHERE """
    
    string_query = f"""SELECT {spectral_table_name}.*
                      FROM AIMSES_NORM 
                      JOIN {spectral_table_name} 
                      ON AIMSES_NORM.ID = {spectral_table_name}.TIME_ID
                      WHERE """

    parameters = []

    for key, func in filter_functions.items():
        if key in dataDict:
            string_query, params = func(string_query, dataDict[key])
            el_de_query, params = func(el_de_query, dataDict[key])
            parameters.extend(params)

    if string_query.endswith('AND '):
        string_query = string_query[:-4]
    
    if el_de_query.endswith('AND '):
        el_de_query = el_de_query[:-4]

    return string_query, el_de_query, parameters, dataDict["Spectra"][0]