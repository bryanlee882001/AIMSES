from datetime import datetime


# Convert HH:MM:SS Format to Fractional Hours (MLT)
def convertMLT(time_str):

    try:
        # ERROR: 23:59:59. BUT THERE ARE 52 ELEMENTS IN 24:00:00
        
        # Parse the time string to a datetime object
        time_obj = datetime.strptime(time_str, '%H:%M:%S')

        # Calculate the total seconds since midnight
        total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second

        # Convert total seconds to fractional hours (MLT)
        mlt = total_seconds / 3600

        return mlt
    except ValueError as e:
        # Handle the ValueError (invalid time string format)
        raise ValueError("Invalid time format. Please provide time in HH:MM:SS format.") from e


# Check Input to see if its an int/float or it has any notations
def checkNumInput(input_str):

    try:
        # Attempt to convert input to a float
        num = float(input_str)
        return num
    except ValueError:
        # If ValueError occurs, attempt to handle scientific notation
        if 'e' in input_str.lower():
            try:
                # Split input based on 'e' and convert coefficient and exponent to float
                coefficient, exponent = map(float, input_str.lower().split("e"))
                # Calculate the result using scientific notation
                result = coefficient * pow(10, exponent)
                return result
            except ValueError:
                # Invalid scientific notation format
                raise ValueError("Invalid scientific notation format")
        else:
            # Invalid input
            raise ValueError("Invalid input")


