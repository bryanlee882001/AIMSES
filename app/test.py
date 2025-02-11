import sqlite3
from query_builder import QueryBuilder
from aimses import AIMSES

class TestSuite:
    def __init__(self, db_path="./db/database.db"):
        self.db_path = db_path

    def print_separator(self):
        print("\n" + "="*50 + "\n")

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
        
        filter_data = {
            "ILAT": {
                "Range": "Between",
                "minRange": "68",
                "maxRange": "72",
                "Hemisphere": "Either"
            },
            "MLT": {
                "Range": "Between",
                "minRange": "22:00:00",
                "maxRange": "00:00:00"
            },
            "MECHANISMS": ["Alf Only"]
        }

        try:
            qb = QueryBuilder(spectra_type="Downward", filter_data=filter_data)
            
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
        
        count_params = {
            'Mission': ['Both'],
            'MLT': {
                'Range': 'Between',
                'minRange': '12:00:00',
                'maxRange': '18:00:00'
            },
            'ILAT': {
                'Range': 'Between',
                'minRange': '60',
                'maxRange': '70',
                'Hemisphere': 'Northern Hemisphere'
            },
            'Spectra': ['Downward'],
            'Statistics': ['Mean', 'Median'],
            'Normalization': ['Raw']
        }
        
        try:
            aimses = AIMSES('count', count_params)
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
        
        spectral_params = {
            'Statistics': ['Mean', '+1σ', '-1σ', 'Median'],
            'Spectra': ['Downward'],
            'Normalization': ['Number Flux'],
            'Mission': ['Early Mission'],
            'MLT': {
                'Range': 'Between',
                'minRange': '12:00:00',
                'maxRange': '18:00:00'
            },
            'ILAT': {
                'Range': 'Between',
                'minRange': '60',
                'maxRange': '70',
                'Hemisphere': 'Northern Hemisphere'
            }
        }
        
        try:
            aimses = AIMSES('events', spectral_params)
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
        
        raw_params = {
            'Statistics': ['Mean'],
            'Spectra': ['Downward'],
            'Normalization': ['Raw'],
            'Mission': ['Early Mission'],
            'MLT': {
                'Range': 'Between',
                'minRange': '12:00:00',
                'maxRange': '18:00:00'
            }
        }
        
        try:
            aimses = AIMSES('events', raw_params)
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


if __name__ == "__main__":
    test_suite = TestSuite()
    test_suite.run_all_tests()