import sqlite3
from .query_builder import QueryBuilder
from .aimses import AIMSES

class TestSuite:
    def __init__(self, params, db_path="./db/database.db"):
        self.db_path = db_path
        self.params  = params


    def print_separator(self):
        print("\n" + "="*50 + "\n")


    def execute_raw_query(self, query):
        """Execute a raw SQL query and return results"""
        print("Executing Raw Query")
        try:
            with sqlite3.connect(self.db_path) as conn:

                # Get both column names and values
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query)
                
                # Get column names
                column_names = [description[0] for description in cursor.description]
                max_col_length = max(len(col) for col in column_names) if column_names else 0
                
                # Fetch results
                results = cursor.fetchall()

                # Print Column names on left
                print("\nQuery Results:")
                print("-" * (max_col_length + 25))
                
                for row in results:
                    for i, col_name in enumerate(column_names):
                        print(f"{col_name.ljust(max_col_length)} | {row[i]}")
                    print("-" * (max_col_length + 25)) 

        except sqlite3.Error as e:
            print(f"Query error: {e}")


    def test_basic_db_connection(self):
        """Test basic database connectivity and simple query"""
        print("Testing Basic Database Connection...")
        try:
            with sqlite3.connect(self.db_path) as con:
                cursor = con.cursor()
                query = 'SELECT * FROM el_de LIMIT 1;'
                cursor.execute(query)
                result = cursor.fetchone()
                print(f"Basic query result: {result}")
                return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False


    def test_query_builder(self):
        """Test QueryBuilder functionality"""
        print("Testing QueryBuilder...")
        
        try:
            # Filter out list-type parameters and keep only filter data
            filter_data = {k: v for k, v in self.params.items() 
                        if k not in {'Statistics', 'Spectra', 'Normalization', 'Mission'}}
            
            # Get spectra type from params
            spectra_type = self.params.get('Spectra', ['Downward'])[0]
            
            qb = QueryBuilder(spectra_type=spectra_type, filter_data=filter_data)
            
            # Test mission query
            mission_query, mission_params = qb.create_query_for_mission()
            print("\nMission Query:")
            print(f"Query: {mission_query}")
            print(f"Parameters: {mission_params}")

            # Execute mission query
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(mission_query, mission_params)
                early_count, late_count = cursor.fetchone()
                print(f"\nResults:")
                print(f"Early Mission Count: {early_count}")
                print(f"Late Mission Count: {late_count}")

            # Test join query
            spec_query, el_de_query, spec_params = qb.create_join_query()
            print("\nSpectral Query:")
            print(f"Main Query: {spec_query}")
            print(f"EL_DE Query: {el_de_query}")
            print(f"Parameters: {spec_params}")
            print(f"Using Spectral Table: {qb.spectral_table}")
            return True

        except Exception as e:
            print(f"QueryBuilder test error: {e}")
            return False


    def test_mission_count(self):
        """Test AIMSES mission count functionality"""
        print("Testing Mission Count Query...")
        
        try:
            aimses = AIMSES('count', self.params)
            success = aimses.get_events()
            
            print(f"Query executed successfully: {success}")
            if success:
                counts = aimses.get_final_count()
                print(f"Early Mission Count: {counts['early_mission']}")
                print(f"Late Mission Count: {counts['late_mission']}")
            return success
        except Exception as e:
            print(f"Mission count test error: {e}")
            return False


    def test_spectral_statistics(self):
        """Test AIMSES spectral statistics functionality"""
        print("Testing Spectral Statistics Query...")
                
        try:
            aimses = AIMSES('events', self.params)
            success = aimses.get_events()
            
            print(f"Query executed successfully: {success}")
            if success:
                aimses.compute_statistics()
                stats = aimses.get_final_statistics()
                
                print("\nComputed Statistics:")
                print(f"Number of statistics computed: {len(stats['yAxis'])}")
                for stat_type, values in stats['yAxis'].items():
                    print(f"{stat_type}: {len(values)} values computed")
                    print(f"Sample values: {values[:3]}...")
            return success
        except Exception as e:
            print(f"Spectral statistics test error: {e}")
            return False


    def test_raw_data(self):
        """Test AIMSES raw data processing"""
        print("Testing Raw Data Processing...")
        
        try:
            aimses = AIMSES('events', self.params)
            success = aimses.get_events()
            
            print(f"Query executed successfully: {success}")
            if success:
                aimses.compute_statistics()
                stats = aimses.get_final_statistics()
                print("\nRaw Statistics:")
                if 'yAxis' in stats and 'Mean' in stats['yAxis']:
                    print(f"Number of mean values: {len(stats['yAxis']['Mean'])}")
                    print(f"Sample values: {stats['yAxis']['Mean'][:3]}...")
            return success
        except Exception as e:
            print(f"Raw data test error: {e}")
            return False


    def run_all_tests(self):
        """Run all test cases"""
        print("Starting Complete Test Suite\n")
        
        tests = [
            ("Database Connection", self.test_basic_db_connection),
            ("Query Builder", self.test_query_builder),
            ("Mission Count", self.test_mission_count),
            ("Spectral Statistics", self.test_spectral_statistics),
            ("Raw Data Processing", self.test_raw_data)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\nRunning {test_name} Test...")
            try:
                success = test_func()
                results.append((test_name, success))
            except Exception as e:
                print(f"Unexpected error in {test_name}: {str(e)}")
                results.append((test_name, False))
            self.print_separator()

        # Print summary
        print("\nTest Summary:")
        print("-" * 40)
        for test_name, success in results:
            status = "✓ PASSED" if success else "✗ FAILED"
            print(f"{test_name}: {status}")
        
        # Calculate success rate
        success_rate = (sum(1 for _, success in results if success) / len(results)) * 100
        print(f"\nOverall Success Rate: {success_rate:.1f}%")


    def export_spectral_data(self):
        """Test AIMSES raw data processing"""
        print("Testing Raw Data Processing...")
        
        try:
            aimses = AIMSES('events', params)
            success = aimses.get_events()
            
            if success and aimses.events:
                print("Successfully retrieved events. Exporting to CSV...")
                
                # Get the spectral data
                spectral_data = aimses.events['spectral']
                
                import csv
                print(len(spectral_data[0]))
                
                # Create the CSV file
                with open('raw_spectral_data.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write header row
                    header = ['TIME_ID', 'TIME', 'MLT'] + [f'bin_{i+1}' for i in range(47)]
                    writer.writerow(header)
                    
                    # Write data rows
                    for row in spectral_data:
                        writer.writerow(row)
                
                print(f"Raw data exported to raw_spectral_data.csv")
                print(f"Total number of events exported: {len(spectral_data)}")
                return True
                
            else:
                print("Failed to get events from database")
                return False
                
        except Exception as e:
            print(f"Raw data test error: {e}")
            return False


if __name__ == "__main__":

    # Testing specific conditions
    params = {
        'Statistics': ['Mean','+1σ','-1σ','Median','25%','75%'],
        'Spectra': ['Downward'],
        'Normalization': ['Raw'],
        'Mission': ['Early Mission'],
        'MLT': {
            'Range': 'Between',
            'minRange': '22:00:00',
            'maxRange': '23:00:00'
        },
        'ILAT': {
            'Hemisphere': 'Either',
            'Range': 'Between',
            'minRange': '69',
            'maxRange': '70'
        },
        'MECHANISMS' : ['QS Dominant'],
        'EFLUX': {
            'Range': 'Between',
            'minRange': '5',
            'maxRange': '7'
        },
    }
    test_suite = TestSuite(params=params)

    # 1. Run all tests
    # test_suite.run_all_tests()

    # 2. Export spectral data for event validation
    # test_suite.export_spectral_data()

    # 3. Execute Raw Query
    QUERY = """
            SELECT *
            FROM AIMSES_NORM 
            WHERE (AIMSES_NORM.MLT BETWEEN 22.0 AND 23.0) 
            AND   (ABS(AIMSES_NORM.ILAT) BETWEEN 69 AND 70) 
            AND   (AIMSES_NORM.MECHS = -1 OR AIMSES_NORM.MECHS = 1) 
            AND   (AIMSES_NORM.EFLUX BETWEEN 5 AND 7) 
            AND   (AIMSES_NORM.TIME BETWEEN 843419539 AND 1023754226)
            """
    test_suite.execute_raw_query(QUERY)
    

