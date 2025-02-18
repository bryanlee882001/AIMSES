import sqlite3
import numpy as np
from .query_builder import QueryBuilder
from .constants import (EARLY_MISSION_VALUES, LATE_MISSION_VALUES, BOTH_MISSIONS_VALUES)


class AIMSES:
    """
    AIMSES class is the interface between the Database and the Web Application. It gets the parameters, queries the 
    events/counts from the SQLite Database, and computes the statistics and normalization. 

    Procedures:
    (1) load_params()          : Load the parameters into the class's attributes
    (2) get_events()           : Strings the query using QueryBuilder() and queries the events from the Database
    (3) compute_statistics()   : Computes the statistics based on the events, and calls compute_normalization if necessary 
    (4) get_final_statistics()/
        get_final_count()      : Returns the final statistics/count after computation to be sent back to the frontend 
    """

    def __init__ (self, query_type: str, params: dict={}):
        """
        Constructor for AIMSES Database Management System

        Params:
            params: collection of params (both filters and generation requirements) obtained from frontend
            type: querying type (count or events)
                i)  Count : Getting the number of events given the params
                ii) Events: Getting the list of events given the params for spectral computation
        """
        # Main Attributes
        self.params = params
        self.type   = query_type
        self.query  = {'sql' : '', 'param' : []}
        
        # Statistical Computation
        self.events        = []
        self.energy_fluxes = []

        # Filtering Requirements
        self.filters = {}
        
        # Generation Requirements
        self.statistics    = []
        self.spectra       = ''
        self.normalization = ''
        self.mission       = ''

        # Energy Values
        self.mission_values = BOTH_MISSIONS_VALUES

        # Final Output
        self.final_statistics = {}
        self.final_count      = {}

        # Load parameters if provided
        if params:
            self.load_params()


    def load_params(self):
        """
        Function to set the class's attributes for both filter and generation requirements with
        the given parameters from the user (frontend). 
        """
        # Set generation requirements
        self.statistics    = self.params.get('Statistics'   , [])
        self.spectra       = self.params.get('Spectra'      , [''])[0]  
        self.normalization = self.params.get('Normalization', [''])[0]
        self.mission       = self.params.get('Mission'      , [''])[0]

        # Set mission values based on mission type
        self.mission_values = {
            "Early Mission": EARLY_MISSION_VALUES,
            "Late Mission": LATE_MISSION_VALUES,
            "Both": BOTH_MISSIONS_VALUES
        }.get(self.mission, BOTH_MISSIONS_VALUES)

        # Set filters
        self.filters = {k: v for k, v in self.params.items() 
                       if k not in {'Statistics', 'Spectra', 'Normalization'}}

        # Initialize QueryBuilder
        query_builder = QueryBuilder(spectra_type=self.spectra, 
                                     filter_data=self.filters)

        # Get Query String Based on Type
        if  self.type  == 'count':
            sql, params = query_builder.create_query_for_mission()
            self.query  = {
                'sql'   : sql, 
                'param' : params
            }

        elif self.type == 'events':
            sql, el_de_sql, params = query_builder.create_join_query()
            self.query = {
                'sql'      : sql,
                'el_de_sql': el_de_sql,
                'param'    : params
            }


    def get_events(self):
        """
        Function to get the events from the SQLite Database based on the query.sql and 
        query.param (built from QueryBuilder()) obtained from load_params().
        """
        conn, cursor = None, None
        try:
            conn, cursor = self.get_db_connection()

            if self.type == 'count':
                # Execute Parameterized query
                cursor.execute(self.query['sql'], self.query['param'])
                
                # Fetch count results
                result = cursor.fetchone()

                # Set final count
                self.final_count = {
                    'early_mission': result[0] if result else 0,
                    'late_mission': result[1] if result else 0
                }
                return True

            elif self.type == 'events':
                # Execute main query
                cursor.execute(self.query['sql'], self.query['param'])
                
                # Convert to tuples
                spectral_results = [tuple(row) for row in cursor.fetchall()]

                # NOTE: Execute el_de query not needed for now
                # cursor.execute(self.query['el_de_sql'], self.query['param'])
                # el_de_results = [tuple(row) for row in cursor.fetchall()]

                if not spectral_results:
                    return False

                # Set final events
                self.events = {
                    'spectral': spectral_results,
                    # 'el_de'   : el_de_results
                }
                return True

            return False

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        
        finally:
            if conn:
                cursor.close()
                conn.close()


    def compute_statistics(self):
        """
        Function to compute statistics and normalization if needed. Here are possible combination of statistics
        (Mean, +1 sigma, -1 sigma, Median, 25%, 75%) which can be calculated depending on the selected requirements. 
        """
        if not self.events:
            return

        if self.normalization != "Raw":
            self.compute_normalization()
        else:
            # Extract raw spectral values, skipping first 3 columns
            self.normalized_data = [
                [float(value) for value in event[3:]]
                for event in self.events['spectral']
            ]
            self.mean_energy_flux = 1

        # Initialize statistics dictionary
        computed_stats = {stat: [] for stat in self.statistics}

        # Compute statistics for each energy bin
        for bin_values in zip(*self.normalized_data):
            bin_values = np.array(bin_values)
            
            for stat in self.statistics:
                if stat == "Mean":
                    computed_stats[stat].append(np.mean(bin_values) * self.mean_energy_flux)
                elif stat == "+1σ":
                    computed_stats[stat].append((np.mean(bin_values) + np.std(bin_values)) * self.mean_energy_flux)
                elif stat == "-1σ":
                    computed_stats[stat].append((np.mean(bin_values) - np.std(bin_values)) * self.mean_energy_flux)
                elif stat == "Median":
                    computed_stats[stat].append(np.median(bin_values) * self.mean_energy_flux)
                elif stat == "25%":
                    computed_stats[stat].append(np.percentile(bin_values, 25) * self.mean_energy_flux)
                elif stat == "75%":
                    computed_stats[stat].append(np.percentile(bin_values, 75) * self.mean_energy_flux)

        self.final_statistics = {'yAxis': computed_stats}


    def compute_normalization(self):
        """
        Function to compute normalization (energy or number flux) before statistical computation. 
        """ 
        normalized_data, energy_fluxes = [], []

        dict_bins  = {lst[0]: lst[3:] for lst in self.events['spectral']}
        dict_el_de = {lst[0]: lst[3:] for lst in self.events['el_de']}

        # Process each event using matching time_ids
        for time_id in dict_bins.keys() & dict_el_de.keys():
            
            bins = np.array(dict_bins[time_id])    # Spectral values
            dE   = np.array(dict_el_de[time_id])   # Energy bin widths
            E    = np.array(self.mission_values)   # Energy values

            # Compute flux
            bins_dE = np.multiply(bins, dE)
            flux = np.multiply(bins_dE, E) if self.normalization == 'Number Flux' else bins_dE
            total_energy = np.sum(flux)
            
            energy_fluxes.append(total_energy)
            
            # Normalize bins
            normalized = np.divide(bins, total_energy, out=np.zeros_like(bins), where=total_energy!=0)
            normalized_data.append(normalized)

        self.normalized_data = normalized_data
        self.mean_energy_flux = np.mean(energy_fluxes)


    def get_final_statistics(self) -> dict:
        """Return final statistics for frontend visualization."""
        return self.final_statistics


    def get_final_count(self) -> dict:
        """Return event counts for both mission periods."""
        return self.final_count


    @staticmethod
    def get_db_connection():
        """Create a database connection and return the connection and cursor."""
        conn = sqlite3.connect('./db/database.db')
        return conn, conn.cursor()
    


