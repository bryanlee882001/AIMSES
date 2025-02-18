from datetime import datetime

class QueryBuilder:
    """A class for building SQL queries for the AIMSES database."""

    def __init__(self, spectra_type: str, filter_data: dict):
        """
        Initialize QueryBuilder with spectra type and filter data.
        
        Args:
            spectra_type (str): One of "Downward", "Upward", or "Perpendicular"
            filter_data (Dict[str, Any]): Dictionary containing filter parameters
        """
        self.filter_functions = {
            "TIME"              : self.get_time,
            "MLT"               : self.get_mlt,
            "ILAT"              : self.get_ilat,
            "ALT"               : self.get_alt,
            "SZA"               : self.get_sza,
            "F10.7"             : self.get_f107,
            "EFLUX"             : self.get_eflux,
            "NFLUX"             : self.get_nflux,
            "CONJUGATE SZA"     : self.get_conjugate_sza,
            "KP"                : self.get_kp,
            "AE"                : self.get_ae,
            "DST"               : self.get_dst,
            "SOLAR WIND DRIVING": self.get_swd,
            "LCA"               : self.get_lca,
            "MECHANISMS"        : self.get_mech,
            "Mission"           : self.get_mission
        }
        
        self.filter_data = filter_data
        self.spectral_table = self._get_spectral_table(spectra_type)


    @staticmethod
    def _get_spectral_table(spectra_type: str) -> str:
        """Get the spectral table name based on spectra type."""
        spectral_mapping = {
            "Downward": "DOWNGOING",
            "Upward": "UPGOING",
            "Perpendicular": "PERPENDICULAR"
        }

        spectral_table = spectral_mapping.get(spectra_type)
        if not spectral_table:
            raise ValueError("Invalid spectra type. Must be 'Downward', 'Upward', or 'Perpendicular'")
            
        return spectral_table
    

    @staticmethod
    def _convert_mlt(time_str: str) -> float:
        """A function that converts HH:MM:SS Format to Fractional Hours (MLT)"""
        try:
            # If input is 24:00:00, we assume that its 00:00:00 in the database
            if (time_str == '24:00:00'): 
                return 0.0

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


    @staticmethod
    def _convert_time_to_epoch(time_str: str) -> int:
        """ A function that converts TIME to Epoch"""
        # Parse the time string to a datetime object and get epoch time
        datetime_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        epoch_time = datetime_obj.timestamp()

        # Convert to integer to remove decimal places
        return int(epoch_time)


    @staticmethod
    def _check_num_input(input_str: str) -> float:
        """A function that checks Input to see if its an int/float or it has any notations"""
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


    def _generic_filter_query(self, string_query: str, filter_data: dict, column: str, parameters: list) -> tuple:
        """Helper function for selections that only have Range (Between, less than, greater than)"""
        range_type = filter_data.get("Range")
        
        if range_type == "Lesser Than":
            max_range = self._check_num_input(filter_data.get("lesserThanValue"))
            string_query += f"({column} <= ?) AND "
            parameters.append(max_range)
        
        elif range_type == "Greater Than":
            min_range = self._check_num_input(filter_data.get("greaterThanValue"))
            string_query += f"({column} >= ?) AND "
            parameters.append(min_range)
        
        elif range_type == "Between":
            min_range = self._check_num_input(filter_data.get("minRange"))
            max_range = self._check_num_input(filter_data.get("maxRange"))
            
            if min_range > max_range:
                raise ValueError("Minimum Range cannot be more than Maximum Range")
            
            string_query += f"({column} BETWEEN ? AND ?) AND "
            parameters.extend([min_range, max_range])
        
        else:
            raise ValueError("Invalid or No Range Selected")
        
        return string_query, parameters


    def get_time(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for TIME based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        range_type = filter_data.get("Range")
        
        if range_type == "Between":
            min_range = self._convert_time_to_epoch(filter_data.get("minRange"))
            max_range = self._convert_time_to_epoch(filter_data.get("maxRange"))
            string_query += "(AIMSES_NORM.TIME BETWEEN ? AND ?) AND "
            parameters.extend([min_range, max_range])
        
        elif range_type == "Lesser Than":
            lesser_than_value = self._convert_time_to_epoch(filter_data.get("lesserThanValue"))
            string_query += "(AIMSES_NORM.TIME <= ?) AND "
            parameters.append(lesser_than_value)
        
        elif range_type == "Greater Than":
            greater_than_value = self._convert_time_to_epoch(filter_data.get("greaterThanValue"))
            string_query += "(AIMSES_NORM.TIME >= ?) AND "
            parameters.append(greater_than_value)
        
        else:
            raise ValueError("No range type specified")
        
        return string_query, parameters


    def get_mlt(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for MLT based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        range_type = filter_data.get("Range")
        
        if range_type == "Between":
            min_range = self._convert_mlt(filter_data.get("minRange"))
            max_range = self._convert_mlt(filter_data.get("maxRange"))
            
            if min_range <= max_range:
                string_query += "(AIMSES_NORM.MLT BETWEEN ? AND ?) AND "
                parameters.extend([min_range, max_range])
            else:
                string_query += "((AIMSES_NORM.MLT BETWEEN ? AND 24.0) OR (AIMSES_NORM.MLT BETWEEN 0.0 AND ?)) AND"
                parameters.extend([min_range, max_range])
        
        elif range_type == "Lesser Than":
            lesser_than_value = self._convert_mlt(filter_data.get("lesserThanValue"))
            string_query += "(AIMSES_NORM.MLT <= ?) AND "
            parameters.append(lesser_than_value)
        
        elif range_type == "Greater Than":
            greater_than_value = self._convert_mlt(filter_data.get("greaterThanValue"))
            string_query += "(AIMSES_NORM.MLT >= ?) AND "
            parameters.append(greater_than_value)
        
        else:
            raise ValueError("No range type specified")
        
        return string_query, parameters


    def get_ilat(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for ILAT based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        hemisphere = filter_data.get("Hemisphere")
        if not hemisphere:
            raise ValueError("No hemisphere selected")
        
        range_type = filter_data.get("Range")
        
        if range_type == "Lesser Than":
            lesser_than_value = self._check_num_input(filter_data.get("lesserThanValue"))
            
            if (hemisphere == "Northern Hemisphere" and 0 <= lesser_than_value <= 90) or \
               (hemisphere == "Southern Hemisphere" and -90 <= lesser_than_value <= 0) or \
               (hemisphere == "Either" and 0 <= abs(lesser_than_value) <= 90):
                string_query += "(AIMSES_NORM.ILAT <= ?) AND "
                parameters.append(lesser_than_value)
            else:
                raise ValueError("Invalid range for 'Lesser Than' type")
        
        elif range_type == "Greater Than":
            greater_than_value = self._check_num_input(filter_data.get("greaterThanValue"))
            
            if (hemisphere == "Northern Hemisphere" and 0 <= greater_than_value <= 90) or \
               (hemisphere == "Southern Hemisphere" and -90 <= greater_than_value <= 0) or \
               (hemisphere == "Either" and 0 <= abs(greater_than_value) <= 90):
                string_query += "(AIMSES_NORM.ILAT >= ?) AND "
                parameters.append(greater_than_value)
            else:
                raise ValueError("Invalid range for 'Greater Than' type")
        
        elif range_type == "Between":
            min_range = self._check_num_input(filter_data.get("minRange"))
            max_range = self._check_num_input(filter_data.get("maxRange"))
            
            if (hemisphere == "Northern Hemisphere" and 0 <= min_range < max_range <= 90) or \
               (hemisphere == "Southern Hemisphere" and -90 <= min_range < max_range <= 0) or \
               (hemisphere == "Either" and 0 <= abs(min_range) < abs(max_range) <= 90):
                string_query += "(AIMSES_NORM.ILAT BETWEEN ? AND ?) AND "
                parameters.extend([min_range, max_range])
            else:
                raise ValueError("Invalid range for 'Between' type")
        
        return string_query, parameters


    def get_alt(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for ALT based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        return self._generic_filter_query(string_query, filter_data, "AIMSES_NORM.ALT", parameters)


    def get_sza(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for SZA based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        return self._generic_filter_query(string_query, filter_data, "AIMSES_NORM.SZA", parameters)


    def get_f107(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for F10.7 based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        return self._generic_filter_query(string_query, filter_data, "AIMSES_NORM.F107", parameters)


    def get_eflux(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for EFLUX based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        return self._generic_filter_query(string_query, filter_data, "AIMSES_NORM.EFLUX", parameters)


    def get_nflux(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for NFLUX based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        return self._generic_filter_query(string_query, filter_data, "AIMSES_NORM.NFLUX", parameters)


    def get_conjugate_sza(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for Conjugate SZA based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        return self._generic_filter_query(string_query, filter_data, "AIMSES_NORM.CONJUGATE_SZA", parameters)


    def get_kp(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for KP based on user input for querying"""
        if not filter_data:
            return string_query, []
            
        parameters = []
        range_type = filter_data.get("Range")
        
        if range_type == "Lesser Than":
            max_range = self._check_num_input(filter_data.get("lesserThanValue"))
            string_query += "(AIMSES_NORM.KP < ?) AND "
            parameters.append(max_range)
        
        elif range_type == "Greater Than":
            min_range = self._check_num_input(filter_data.get("greaterThanValue"))
            string_query += "(AIMSES_NORM.KP >= ?) AND "
            parameters.append(min_range)
        
        elif range_type == "Between":
            min_range = self._check_num_input(filter_data.get("minRange"))
            max_range = self._check_num_input(filter_data.get("maxRange"))
            
            if min_range > max_range:
                raise ValueError("Minimum Range cannot be more than Maximum Range")
            
            string_query += "(AIMSES_NORM.KP BETWEEN ? AND ?) AND "
            parameters.extend([min_range, max_range])
        
        else:
            raise ValueError("Invalid or No Range Selected")
        
        return string_query, parameters


    def get_ae(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for AE based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        return self._generic_filter_query(string_query, filter_data, "AIMSES_NORM.AE", parameters)


    def get_dst(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for DST based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        return self._generic_filter_query(string_query, filter_data, "AIMSES_NORM.DST", parameters)


    def get_swd(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for Solar Wind Driving based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        return self._generic_filter_query(string_query, filter_data, "AIMSES_NORM.NEWELL_FLUX", parameters)


    def get_lca(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for LCA based on user input for querying"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        return self._generic_filter_query(string_query, filter_data, "AIMSES_NORM.LCA", parameters)


    def get_mech(self, string_query: str, filter_data: dict) -> tuple:
        """Function that determines the range for MECHS based on user input for querying"""
        if len(filter_data) != 1:
            return string_query, []
        
        checked_mech = filter_data[0]
        parameters = []
        mech_queries = {
            "QS Only": "(AIMSES_NORM.MECHS = -1)",
            "QS Dominant": "(AIMSES_NORM.MECHS = -1 OR AIMSES_NORM.MECHS = 1)",
            "Alf Only": "(AIMSES_NORM.MECHS = -2)",
            "Alf Dominant": "(AIMSES_NORM.MECHS = -2 OR AIMSES_NORM.MECHS = 2)",
            "WS Only": "(AIMSES_NORM.MECHS = -4)",
            "WS Dominant": "(AIMSES_NORM.MECHS = -4 OR AIMSES_NORM.MECHS = 4)",
            "QS + Alf": "(AIMSES_NORM.MECHS = 3)",
            "QS + WS": "(AIMSES_NORM.MECHS = 5)",
            "Alf + WS": "(AIMSES_NORM.MECHS = 6)",
            "Alf + WS + QS": "(AIMSES_NORM.MECHS = 7)",
            "Any QS": "(AIMSES_NORM.MECHS = -1 OR AIMSES_NORM.MECHS = 1 OR AIMSES_NORM.MECHS = 3 OR AIMSES_NORM.MECHS = 5 OR AIMSES_NORM.MECHS = 7)",
            "Any Alf": "(AIMSES_NORM.MECHS = -2 OR AIMSES_NORM.MECHS = 2 OR AIMSES_NORM.MECHS = 3 OR AIMSES_NORM.MECHS = 6 OR AIMSES_NORM.MECHS = 7)",
            "Any WS": "(AIMSES_NORM.MECHS = -4 OR AIMSES_NORM.MECHS = 4 OR AIMSES_NORM.MECHS = 5 OR AIMSES_NORM.MECHS = 6 OR AIMSES_NORM.MECHS = 7)",
            "Weak": "(AIMSES_NORM.MECHS = 0)",
            "Any Intense": "(NOT AIMSES_NORM.MECHS = 0)"
        }
        
        if checked_mech in mech_queries:
            string_query += mech_queries[checked_mech] + " AND "
        
        return string_query, parameters


    def get_mission(self, string_query: str, filter_data: str) -> tuple:
        """Function that determines the range for Time based on Mission"""
        if not filter_data:
            return string_query, []
        
        parameters = []
        mission_times = {
            "Early Mission": (843419539, 1023754226),
            "Late Mission" : (1023759079, 1241086949)
        }
        
        mission = filter_data[0]
        if mission in mission_times:
            start_time, end_time = mission_times[mission]
            string_query += "(AIMSES_NORM.TIME BETWEEN ? AND ?) AND "
            parameters.extend([start_time, end_time])
        
        return string_query, parameters


    def create_query_for_mission(self) -> tuple:
        """Creates queries based on user input for mission"""
        parameters = []
        
        # Build the basic WHERE clause for filters
        filter_conditions = ""
        filter_params = []
        for key, value in self.filter_data.items():
            if key in self.filter_functions and key != 'Mission':
                condition, params = self.filter_functions[key]("", value)
                if condition.strip():
                    # Remove the trailing 'AND' if it exists
                    cleaned_condition = condition.strip()
                    if cleaned_condition.endswith('AND'):
                        cleaned_condition = cleaned_condition[:-3].strip()
                    filter_conditions += cleaned_condition + " AND "
                    filter_params.extend(params)
        
        # Remove trailing 'AND' if it exists
        if filter_conditions.endswith('AND '):
            filter_conditions = filter_conditions[:-4]
        
        # Base query that counts for both mission periods
        string_query = f"""
            SELECT 
                SUM(CASE 
                    WHEN AIMSES_NORM.TIME BETWEEN ? AND ? AND {filter_conditions}
                    THEN 1 
                    ELSE 0 
                END) AS EARLY_MISSION_COUNT,
                SUM(CASE 
                    WHEN AIMSES_NORM.TIME BETWEEN ? AND ? AND {filter_conditions}
                    THEN 1 
                    ELSE 0 
                END) AS LATE_MISSION_COUNT
            FROM AIMSES_NORM
            JOIN {self.spectral_table} 
            ON AIMSES_NORM.ID = {self.spectral_table}.TIME_ID
        """
        
        # Add parameters in correct order
        parameters.extend([843419539, 1023754226])   # Early mission time range
        parameters.extend(filter_params)             # Filter params for early mission
        parameters.extend([1023759079, 1241086949])  # Late mission time range
        parameters.extend(filter_params)             # Filter params for late mission
        
        return string_query, parameters


    def create_join_query(self) -> tuple:
        """Creates a join query between time values in AIMSES_NORM and UPGOING/DOWNGOING/PERP"""

        el_de_query = """SELECT el_de.*
                        FROM AIMSES_NORM 
                        JOIN el_de
                        ON AIMSES_NORM.ID = el_de.TIME_ID
                        WHERE """
        
        string_query = f"""SELECT {self.spectral_table}.*
                        FROM AIMSES_NORM 
                        JOIN {self.spectral_table} 
                        ON AIMSES_NORM.ID = {self.spectral_table}.TIME_ID
                        WHERE """

        parameters = []

        for key, value in self.filter_data.items():
            if key in self.filter_functions:
                string_query, params = self.filter_functions[key](string_query, value)
                el_de_query, params = self.filter_functions[key](el_de_query, value)
                parameters.extend(params)
        
        if string_query.endswith('AND '):
            string_query = string_query[:-4]
        
        if el_de_query.endswith('AND '):
            el_de_query = el_de_query[:-4]
        
        return string_query, el_de_query, parameters