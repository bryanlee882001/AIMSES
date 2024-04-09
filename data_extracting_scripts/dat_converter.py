"""
Title: Dat Converter 
Author: Bryan Yen Sheng Lee
Description: This script extracts data from .dat files, processes it, and inserts it into a MySQL database.
"""

import struct
import glob, os
import mysql.connector
import time 
import csv 
import chardet
import db_info

# Database credentials
db_config = db_info.db_configuration

# A function that extracts all .cdf files in a given directory 
def GetFiles(path,file_extension):
    
    try:
        # Finding files with the file type .dat
        dat_files = glob.glob(os.path.join(path, file_extension))
    except Exception as e:
        print(f"An exception of type {type(e).__name__} occurred when searching for .dat Files: {e}")
        return None
    else: 
        if len(dat_files) == 0:
            print(f"No {file_extension} files detected in path: {path}")
            return None 
        
        for file in dat_files: 
            # Get File path 
            fileName = os.path.basename(file)

            if file_extension == "*.dat":
                start_time = time.time()
                print("\n")
                print(f"Reading {file_extension} file: {fileName}")
                ReadDatFile(path + fileName, os.path.splitext(fileName)[0])
                print(f'Total Time Taken for {fileName}: {time.time() - start_time}s')
                print("\n")
            elif file_extension == "*.csv":
                start_time = time.time()
                print("\n")
                print(f"Reading {file_extension} file: {fileName}")
                ReadCSVFile(path + fileName, os.path.splitext(fileName)[0])
                print(f'Total Time Taken for {fileName}: {time.time() - start_time}s')
                print("\n")


# A function that reads and extracts data from the .dat file and stores it in an array
def ReadDatFile(path,fileName):
    
    try: 
        # IMPORTANT! 
        # Define the format string based on the IDL structure 
        # I: Unsigned Integer (4 bytes)
        # q: Unsigned Long Long Integer (8 bytes)
        # d: Double-Precision Float (8 bytes)
        # f: Single-Precision Float (4 bytes)
        # totweak: 19084634 records
        # totmechs: 3055403 records
        format_string = "Idiffffffffffffffifffdffffdiffi"

        # Open the binary file for reading
        with open(path, 'rb') as file:
            # Read the binary data
            binary_data = file.read()

        # Calculate the number of records based on the size of the actual binary data and the structure size
        record_size = struct.calcsize(format_string)
        # length = 168 #Size of data with padding
        num_records = len(binary_data) // record_size

        # Unpack the Binary Data
        count = 0
        records = []
        for ii in range(num_records):
            # Slice the variable (from start to end of the binary data) using the information given from byte size
            record_data = binary_data[ii * record_size: (ii + 1) * record_size]

            # Unpack the data into a tuple format 
            record = struct.unpack(format_string, record_data)

            # Add the tuple with 35 variables into an array
            records.append(record)
        
        # Push Data to Database (Stored in an array of tuples)
        print(f"Successfully Extracted {count} rows of data From {fileName}. Pushing to Database...")
        # PushToDatabase(records,fileName)

    except Exception as e:
        print(f"An error occurred when reading {fileName}: {e}")


# A function that reads .csv file and extract its data
def ReadCSVFile(path, fileName):
    
    try:
        # Obtain the necessary encoding for reading .csv
        with open(path, 'rb') as f:
            result = chardet.detect(f.read())
        # Encoding should always be ASCII 
        encode = result['encoding']
    except Exception as e:
        print(f"An exception of type {type(e).__name__} occurred when determining the encoding for file {fileName}: {e}")
        return None
    
    try: 
        # Read CSV File 
        rowArr = []
        
        # Open file to read based on given encoding above
        with open(path, mode='r', encoding=encode) as file:
            csvFile = csv.reader(file)
            
            # Skips first row which contains column names
            next(csvFile)

            # Append all rows from .csv file into rowArr
            count = 1
            for row in csvFile: 
                rowArr.append(row)
                count += 1 
        
            # Push the extracted data to database
            print(f"Extracted {count} rows of data from {fileName}")
            print("Pushing Data into database .....")
            PushToDatabase(rowArr, fileName)
    except Exception as e:
        print(f"An exception of type {type(e).__name__} occurred when determining reading .CSV file {fileName}: {e}")
        return None  


# A function that pushes data from .dat files into the database
def PushToDatabase(records, fileName): 

    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        start_time = time.time()

        # Create Table in Database based on the 35 given variables for .dat file 
        create_table_query = f"""CREATE TABLE IF NOT EXISTS AIMSES_NORM (
            ID               INT AUTO_INCREMENT PRIMARY KEY, 
            ORBIT            INT UNSIGNED,
            TIME             DECIMAL(50,30),
            TIME_INDEX       INT,
            EFLUX            FLOAT,
            EFLUX_UP         FLOAT,
            EFLUX_DW         FLOAT,
            NFLUX_UP         DECIMAL(30,10),
            NFLUX_DW         DECIMAL(30,10),
            NFLUX            DECIMAL(30,10),
            MLT              FLOAT,
            ILAT             FLOAT,
            ALT              FLOAT,
            SZA              FLOAT,
            CONJUGATE_SZA    FLOAT,
            MAP_ILAT         FLOAT,
            MAP_SZA          FLOAT,
            MAP_MLT          FLOAT,
            TIME_WARNING     INT,
            F107             FLOAT,
            KP               FLOAT,
            AE               FLOAT,
            TIME_TO_AE_JUMP  DOUBLE,
            PRE_JUMP_AE      FLOAT,
            POST_JUMP_AE     FLOAT,
            DST              FLOAT,
            DST_PEAK         FLOAT,
            TIME_TO_DST_PEAK DOUBLE,
            BAD              INT,
            WHY_BAD          VARCHAR(255), 
            NEWELL_FLUX      FLOAT,
            NEWELL_CODE      TINYINT UNSIGNED,
            IN_ACCELDB       TINYINT UNSIGNED,
            LCA              FLOAT,
            MECHS            INT
            ); 
        """
        try: 
            cursor.execute(create_table_query)
            conn.commit()  
        except Exception as e:
            print(f"Error creating table: {str(e)}")
        
        # Insert Data into Database
        column_names = """
            ORBIT, TIME, TIME_INDEX, EFLUX, EFLUX_UP, EFLUX_DW, NFLUX_UP, 
            NFLUX_DW, NFLUX, MLT, ILAT, ALT, SZA, CONJUGATE_SZA, MAP_ILAT, 
            MAP_SZA, MAP_MLT, TIME_WARNING, F107, KP, AE, TIME_TO_AE_JUMP, 
            PRE_JUMP_AE, POST_JUMP_AE, DST, DST_PEAK, TIME_TO_DST_PEAK, 
            BAD, NEWELL_FLUX, NEWELL_CODE, IN_ACCELDB, LCA, MECHS
        """
        count = 0 
        for ii in range(len(records)):

            # Tracking iteration progress
            if ii % 100000 == 0:
                print(f"Inserted {ii} rows out of {len(records)} into database ({len(records)-ii} rows remaining)")

            # Replace 'NaN' with a suitable default value (e.g., None for NULL)
            cleaned_values = [value if 'NaN' not in value else None for value in records[ii]]

            # Split list into a string with comma             
            values = ', '.join([str(value) if value is not None else 'NULL' for value in cleaned_values])

            # Create Insert Query string
            insert_query = f"INSERT INTO AIMSES_Norm ({column_names}) VALUES ({values});"

            # Execute Query
            try: 
                cursor.execute(insert_query)
                conn.commit()
            except Exception as e:
                print(f"Error Inserting values at row {ii}: {str(e)}")

        print(f'Data extracted from {fileName} inserted into database successfully. Time Taken: {time.time() - start_time}s')

        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Error pushing to database: {err}")

    finally:
        # Ensure the connection is closed in case of an exception
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":

    # Extract all .dat files in a directory and push data to database (Not Working Properly)
    # Parameters: Directory, File_Extension 
    # GetFiles("/Users/Bryan/Desktop/","*.dat")

    # Extract all .csv files in a directory and push data to database 
    # Parameters: Your Directory, File_Extension 
    GetFiles("/Users/Bryan/Desktop/","*.csv")