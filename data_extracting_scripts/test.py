def remove_missing_times(varDict, timeIdDict):
    # Step 1: Identify TIME values in varDict not present in timeIdDict
    missing_times = [time for time in varDict['TIME'] if time not in timeIdDict]

    # Step 2: Get the index of missing TIME values
    indices_to_remove = [i for i, time in enumerate(varDict['TIME']) if time in missing_times]

    # Step 3: Remove the corresponding elements from each key in varDict
    for key in varDict.keys():
        if isinstance(varDict[key], list):
            # Remove the elements at the identified indices
            for index in sorted(indices_to_remove, reverse=True):
                del varDict[key][index]

    return varDict

# Example usage:
varDict = { 
    'TIME': ['t1', 't2', 't3'],
    'JEe_0lc': [1, 2, 3],
    'JEe_180lc': [4, 5, 6],
    'example': [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [10, 11, 12, 13, 14]]
}

timeIdDict = {
    't1': 'ID1'
}

updated_varDict = remove_missing_times(varDict, timeIdDict)
print(updated_varDict)