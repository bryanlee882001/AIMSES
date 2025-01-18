# import sqlite3

# # Create a SQL connection to our SQLite database
# con = sqlite3.connect("db/database.db")

# cur = con.cursor()

# query = 'SELECT COUNT(*) FROM AIMSES_NORM JOIN DOWNGOING ON AIMSES_NORM.ID = DOWNGOING.TIME_ID WHERE (AIMSES_NORM.MLT BETWEEN 22.0 AND 24.0) AND (AIMSES_NORM.ILAT BETWEEN 68 AND 72) AND (AIMSES_NORM.MECHS = -2)'

# # The result of a "cursor.execute" can be iterated over by row
# for row in cur.execute(query):
#     print(row)

# # Be sure to close the connection
# con.close()



# from query_builder import QueryBuilder
# import sqlite3

# def main():
#     # Example filter data with your specific parameters
#     filter_data = {
#         "ILAT": {
#             "Range": "Between",
#             "minRange": "68",
#             "maxRange": "72",
#             "Hemisphere": "Either"
#         },
#         "MLT": {
#             "Range": "Between",
#             "minRange": "22:00:00",
#             "maxRange": "00:00:00"
#         },
#         "MECHANISMS": ["Alf Only"]
#     }

#     # Initialize QueryBuilder with spectra type and filter data
#     qb = QueryBuilder(spectra_type="Downward", filter_data=filter_data)

#     try:
#         # Create mission query - no need to pass filter_data
#         mission_query, mission_params = qb.create_query_for_mission()
#         print("\nMission Query:")
#         print("Query:", mission_query)
#         print("Parameters:", mission_params)

#         # Execute mission query
#         with sqlite3.connect('./db/database.db') as conn:
#             cursor = conn.cursor()
#             cursor.execute(mission_query, mission_params)
#             early_count, late_count = cursor.fetchone()
#             print(f"\nResults:")
#             print(f"Early Mission Count: {early_count}")
#             print(f"Late Mission Count: {late_count}")

#         # Create join query - no need to pass filter_data
#         spec_query, el_de_query, spec_params = qb.create_join_query()
#         print("\nSpectral Query:")
#         print("Main Query:", spec_query)
#         print("EL_DE Query:", el_de_query)
#         print("Parameters:", spec_params)
#         print("Using Spectral Table:", qb.spectral_table)

#     except sqlite3.Error as e:
#         print(f"Database error: {e}")
#     except ValueError as e:
#         print(f"Validation error: {e}")
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     main()



from aimses import AIMSES
import json

def print_separator():
    print("\n" + "="*50 + "\n")

def test_mission_count():
    """Test getting mission counts with filters"""
    print("Testing Mission Count Query...")
    
    # Test parameters for counting events
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
        'Spectra': 
            ['Downward'], 
        'Statistics':
            ['Mean','Median'],
        'Mission' : ['Both'],
        'Normalization': ['Raw']
    }
    
    # Initialize AIMSES for count
    aimses = AIMSES('count', count_params)
    success = aimses.get_events()
    
    print(f"Query executed successfully: {success}")
    if success:
        counts = aimses.get_final_count()
        print(f"Early Mission Count: {counts['early_mission']}")
        print(f"Late Mission Count: {counts['late_mission']}")

def test_spectral_statistics():
    """Test getting spectral statistics with normalization"""
    print("Testing Spectral Statistics Query...")
    
    # Test parameters for spectral analysis
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
    
    # Initialize AIMSES for events
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
            # Print first few values as sample
            print(f"Sample values: {values[:3]}...")

def test_raw_data():
    """Test processing raw data without normalization"""
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

def main():
    """Run all tests"""
    print("Starting AIMSES Class Tests\n")
    
    try:
        test_mission_count()
        print_separator()
        
        test_spectral_statistics()
        print_separator()
        
        test_raw_data()
        print_separator()
        
        print("All tests completed!")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    main()