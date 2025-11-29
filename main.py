# main.py

import os
from database.database_operation import createMainTable, createSummaryTable, createLogsTable, connectDB, insertMainData, insertSummaryData, insertLogData, closeDB
from config.config import FILE_PATH
from excel.excel_operation import clearWarning, loadExcel, extractMainData, extractSummaryData, closeWorkbook

def main():
    """Main function to extract data from Excel and insert into database"""
    conn = None
    cur = None
    workBook = None
    
    # 1. Check if Excel file exists before proceeding
    if not os.path.exists(FILE_PATH):
        print(f"Error: Excel file not found at path: {FILE_PATH}")
        print("Please ensure the file exists and the path is correct in config.py")
        return
    
    # 2. SetUp the Database Connection
    try:
        conn, cur = connectDB()
        if conn is None or cur is None:
            print("Database connection failed.")
            return
        insertLogData(conn, cur, task_name="Database Connection", process_name="Extraction Task", log_type="INFO", log_message="Database Connection Made Successfully")
    except Exception as e:
        print("Database Connection Error: ", e)
        if conn and cur:
            insertLogData(conn, cur, task_name="Database Connection", process_name="Extraction Task", log_type="ERROR", log_message=f"DB Connection Error: {str(e)}")
        return
    
    # 3. Check the File is Properly Loaded and is not Empty
    try:
        clearWarning()
        workBook, sheet = loadExcel(FILE_PATH)
        insertLogData(conn, cur, task_name="Loading Input File", process_name="Extraction Task", log_type="INFO", log_message="Excel File Loaded Successfully")
    except FileNotFoundError:
        error_msg = f"Excel file not found at path: {FILE_PATH}"
        print(f"Error: {error_msg}")
        insertLogData(conn, cur, task_name="Loading Input File", process_name="Extraction Task", log_type="ERROR", log_message=error_msg)
        closeDB(conn, cur)
        return
    except Exception as e:
        error_msg = f"File Loading Error: {str(e)}"
        print(f"Error: {error_msg}")
        insertLogData(conn, cur, task_name="Loading Input File", process_name="Extraction Task", log_type="ERROR", log_message=error_msg)
        closeDB(conn, cur)
        return
    
    # 4. Extract Main Data
    try:
        inputMainList = extractMainData(sheet)
        insertLogData(conn, cur, task_name="Extracting Main Data", process_name="Extraction Task", log_type="INFO", log_message="Main Data Extracted to List")
    except Exception as e:
        error_msg = f"Main Data Extraction Error: {str(e)}"
        print(f"Error: {error_msg}")    
        insertLogData(conn, cur, task_name="Extracting Main Data", process_name="Extraction Task", log_type="ERROR", log_message=error_msg)
        closeWorkbook(workBook)
        closeDB(conn, cur)
        return
    
    # 5. Extract Summary Data
    try:
        inputSumList = extractSummaryData(sheet)
        insertLogData(conn, cur, task_name="Extracting Summary Data", process_name="Extraction Task", log_type="INFO", log_message="Summary Data Extracted to List")
    except Exception as e:
        error_msg = f"Summary Data Extraction Error: {str(e)}"
        print(f"Error: {error_msg}")
        insertLogData(conn, cur, task_name="Extracting Summary Data", process_name="Extraction Task", log_type="ERROR", log_message=error_msg)
        closeWorkbook(workBook)
        closeDB(conn, cur)
        return
    
    # 6. Create Database Tables
    try: 
        createMainTable(cur, conn)
        createSummaryTable(cur, conn)
        createLogsTable(cur, conn)
        insertLogData(conn, cur, task_name="Creating Tables", process_name="Extraction Task", log_type="INFO", log_message="All Tables Created Successfully")
    except Exception as e:
        error_msg = f"Table Creation Error: {str(e)}"
        print(f"Error: {error_msg}")
        insertLogData(conn, cur, task_name="Creating Tables", process_name="Extraction Task", log_type="ERROR", log_message=error_msg)
        closeWorkbook(workBook)
        closeDB(conn, cur)
        return
    
    # 7. Insert Data into Tables
    try:
        insertMainData(cur, conn, inputMainList)
        insertSummaryData(cur, conn, inputSumList)
        insertLogData(conn, cur, task_name="Inserting Data", process_name="Extraction Task", log_type="INFO", log_message="Data Inserted Successfully")
    except Exception as e:
        error_msg = f"Data Insertion Error: {str(e)}"
        print(f"Error: {error_msg}")
        insertLogData(conn, cur, task_name="Inserting Data", process_name="Extraction Task", log_type="ERROR", log_message=error_msg)
        closeWorkbook(workBook)
        closeDB(conn, cur)
        return
    
    # 8. Close Connections
    try:
        insertLogData(conn, cur, task_name="Closing Connection", process_name="Extraction Task", log_type="INFO", log_message="Process Completed Successfully")
        closeWorkbook(workBook)
        closeDB(conn, cur)
        print("\nAll operations completed successfully!")
    except Exception as e:
        error_msg = f"Database Connection Termination Error: {str(e)}"
        print(f"Error: {error_msg}")

if __name__ == "__main__":
    main()