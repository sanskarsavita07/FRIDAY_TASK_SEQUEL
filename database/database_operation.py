# database_operation.py

# Import PostgreSQL database adapter for Python
import psycopg2
# Import database configuration from config file
from config.config import DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD


def connectDB():
    """Connect to the database and return connection and cursor"""
    try:
        print("Connecting to database...")
        # Establish connection to PostgreSQL database using credentials from config
        conn = psycopg2.connect(
            host=DB_HOST,        # Database server address
            database=DB_DATABASE, # Database name
            user=DB_USER,        # Database username
            password=DB_PASSWORD # Database password
        )
        # Create a cursor object to execute SQL commands
        cur = conn.cursor()
        print("Database connection established.")
        # Return both connection and cursor for use in other functions
        return conn, cur
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise  # Re-raise the exception to handle it in calling code


def createMainTable(cur, conn):
    """Create and clear main table"""
    try:
        # SQL statement to create main market data table if it doesn't exist
        createSql = """
        CREATE TABLE IF NOT EXISTS iex_main_market_table_final (
            exe_id SERIAL PRIMARY KEY,
            date VARCHAR(20),
            hour VARCHAR(20),
            time_block VARCHAR(50),
            purchase_bid DECIMAL(12, 2),
            sell_bid DECIMAL(12, 2),
            mcv DECIMAL(12, 2),
            final_scheduled_volume DECIMAL(12, 2),
            mcp DECIMAL(12, 2),
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        # Execute the CREATE TABLE SQL statement
        cur.execute(createSql)
        # Commit the transaction to make it permanent
        conn.commit()
        print("Main table is ready.")
        
        # Clear all existing data from the table using TRUNCATE
        cur.execute("TRUNCATE TABLE iex_main_market_table_final;")
        conn.commit()
        print("Main table cleared.")
    except Exception as e:
        print(f"Error creating main table: {e}")
        # Rollback transaction in case of error to maintain database consistency
        conn.rollback()
        raise


def createSummaryTable(cur, conn):
    """Create and clear summary table"""
    try:
        # SQL statement to create summary market data table
        createSql = """
        CREATE TABLE IF NOT EXISTS iex_summary_market_table_final (
            exe_id SERIAL PRIMARY KEY,
            date VARCHAR(20),
            summary VARCHAR(50),
            purchase_bid DECIMAL(12, 2),
            sell_bid DECIMAL(12, 2),
            mcv DECIMAL(12, 2),
            final_scheduled_volume DECIMAL(12, 2),
            mcp DECIMAL(12, 2),
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(createSql)
        conn.commit()
        print("Summary table is ready.")
        
        # Clear all existing data from summary table
        cur.execute("TRUNCATE TABLE iex_summary_market_table_final;")
        conn.commit()
        print("Summary table cleared.")
    except Exception as e:
        print(f"Error creating summary table: {e}")
        conn.rollback()
        raise


def createLogsTable(cur, conn):
    """Create and clear process logs table"""
    try:
        # SQL statement to create process logging table
        createSql = """
        CREATE TABLE IF NOT EXISTS process_logs (
            exe_id SERIAL PRIMARY KEY,
            process_name VARCHAR(100),
            task_name VARCHAR(100),
            log_type VARCHAR(20),
            log_message TEXT,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(createSql)
        conn.commit()
        print("Process_logs table is ready.")
        
        # Clear all existing logs (starting fresh for each run)
        cur.execute("TRUNCATE TABLE process_logs;")
        conn.commit()
        print("Process_logs table cleared.")
    except Exception as e:
        print(f"Error creating logs table: {e}")
        conn.rollback()
        raise


def insertMainData(cur, conn, mainData):
    """Insert data into main table"""
    try:
        print("\nInserting data into Main table...")
        # SQL statement for inserting data into main table
        # %s are placeholders for parameterized queries (prevents SQL injection)
        insertSql = """
        INSERT INTO iex_main_market_table_final
        (date, hour, time_block, purchase_bid, sell_bid, mcv, final_scheduled_volume, mcp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        # Loop through each row of mainData and insert into database
        for row in mainData:
            cur.execute(insertSql, row)  # Execute insert for each row
        
        # Commit all inserts as a single transaction
        conn.commit()
        print(f"Inserted {len(mainData)} rows into Main table.")
    except Exception as e:
        print(f"Error inserting main data: {e}")
        conn.rollback()  # Rollback all inserts if any fail
        raise


def insertSummaryData(cur, conn, summaryData):
    """Insert data into summary table"""
    try:
        print("\nInserting data into Summary table...")
        # SQL statement for inserting data into summary table
        insert_sql = """
        INSERT INTO iex_summary_market_table_final
        (date, summary, purchase_bid, sell_bid, mcv, final_scheduled_volume, mcp)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        
        # Loop through each row of summaryData and insert into database
        for row in summaryData:
            cur.execute(insert_sql, row)
        
        conn.commit()
        print(f"Inserted {len(summaryData)} rows into Summary table.")
    except Exception as e:
        print(f"Error inserting summary data: {e}")
        conn.rollback()
        raise


def insertLogData(conn, cur, task_name=None, process_name=None, log_type=None, log_message=None):
    """Insert data into process logs table"""
    print("\nInserting data to Log Table...")
    try:
        # SQL statement for inserting log entries
        insert_sql = """
        INSERT INTO process_logs
        (process_name, task_name, log_type, log_message)
        VALUES (%s, %s, %s, %s);
        """
        
        # Execute insert with the provided log parameters
        cur.execute(insert_sql, (process_name, task_name, log_type, log_message))
        conn.commit()
        print("Log Table data inserted successfully.")
    except Exception as e:
        print(f"Error inserting log data: {e}")
        conn.rollback()
        raise


def closeDB(conn, cur):
    """Close database connection"""
    try:
        # Close cursor if it exists
        if cur:
            cur.close()
        # Close database connection if it exists
        if conn:
            conn.close()
        print("\nDatabase connection closed.")
    except Exception as e:
        print(f"Error closing database connection: {e}")