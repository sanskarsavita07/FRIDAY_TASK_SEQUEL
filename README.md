# FRIDAY_TASK_FINAL_PROJECT

## Project Overview

A Python-based data pipeline that extracts market data from Excel files and stores it in a PostgreSQL database. This project demonstrates ETL (Extract, Transform, Load) operations with robust error handling, logging, and modular architecture.

## Project Structure
FRIDAY_TASK_FINAL_PROJECT/
│
├── config/
│ └── config.py # Configuration settings and constants
├── database/
│ └── database_operation.py # Database connection and operations
├── excel/
│ └── excel_operation.py # Excel file operations and data extraction
├── main.py # Main script orchestrating the entire process
├── files/
│ └── DAM_Market Snapshot.xlsx # Input Excel file (should be placed here)
└── README.md # Project documentation

text

## Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.7+**
- **PostgreSQL** database server
- **Git** (for cloning the repository)

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/FRIDAY_TASK_FINAL_PROJECT.git
cd FRIDAY_TASK_FINAL_PROJECT
2. Install Python Dependencies
bash
pip install psycopg2 openpyxl
3. Database Setup
Create a PostgreSQL database named iex_market_db_task

Update database credentials in config/config.py with your actual database credentials:

4. File Preparation
Create a files/ directory in the project root if it doesn't exist

Place your Excel file named DAM_Market Snapshot.xlsx in the files/ directory

Usage
Run the main script to execute the entire ETL pipeline:

bash
python main.py
The application will automatically:

Connect to the database

Load the Excel file

Extract data from predefined ranges

Create necessary tables

Insert extracted data

Log all operations

Clean up resources

Code Architecture
config/config.py
Purpose: Central configuration management for the entire application

Key Components:

Database connection parameters (host, database name, user, password)

Excel file path configuration

Cell range definitions for main and summary data tables in Excel

Constants for row and column boundaries to specify data extraction areas

database/database_operation.py
Purpose: Handles all database interactions and operations

Main Functions:

connectDB() - Establishes connection to PostgreSQL

createMainTable(), createSummaryTable(), createLogsTable() - Table management

insertMainData(), insertSummaryData() - Data insertion

insertLogData() - Audit logging

closeDB() - Proper connection cleanup

Key Features:

Database connection management with error handling

Table creation for main data, summary data, and process logs

Data insertion functions with transaction management

Comprehensive error handling with rollback capabilities

excel/excel_operation.py
Purpose: Handles Excel file operations and data extraction

Main Functions:

loadExcel() - Loads and parses Excel files

extractMainData() - Extracts main market data table

extractSummaryData() - Extracts summary statistics table

closeWorkbook() - Proper file handle cleanup

Key Features:

Excel file loading with warning suppression

Data extraction from predefined cell ranges

Empty row filtering during data extraction

Proper resource management with workbook cleanup

main.py
Purpose: Main orchestrator that coordinates the entire ETL process

Process Flow:

Database connection establishment

Excel file loading and validation

Main data extraction from Excel

Summary data extraction from Excel

Database table creation

Data insertion into respective tables

Resource cleanup and completion

Key Features:

Sequential workflow management

Comprehensive error handling at each step

Resource cleanup in all scenarios

Detailed logging throughout the process

Database Schema
iex_main_market_table_final
Stores detailed market data with time-series information:

exe_id - Auto-incrementing primary key

date, hour, time_block - Temporal information

purchase_bid, sell_bid - Bid prices

mcv, final_scheduled_volume - Volume metrics

mcp - Market clearing price

upload_timestamp - Automatic timestamp

iex_summary_market_table_final
Stores aggregated summary statistics:

Similar structure to main table with summary description field

process_logs
Audit trail for process execution:

process_name, task_name - Process identification

log_type, log_message - Log details and severity

upload_timestamp - When the log was created

Configuration
Update the following in config/config.py according to your setup:

Database Configuration
python
DB_HOST = "localhost"
DB_DATABASE = "iex_market_db_task"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
File Path Configuration
python
FILE_PATH = "./files/DAM_Market Snapshot.xlsx"
Excel Data Ranges
python
# Main Table Ranges
MAIN_MIN_ROW = 6
MAIN_MAX_ROW = 101
MAIN_MIN_COL = 1
MAIN_MAX_COL = 8

# Summary Table Ranges
SUMMARY_MIN_ROW = 103
SUMMARY_MAX_ROW = 106
SUMMARY_MIN_COL = 1
SUMMARY_MAX_COL = 7
Features
Error Handling
Comprehensive try-catch blocks throughout the application

Automatic rollback of failed database transactions

Detailed logging of errors and successful operations

Proper resource cleanup in error scenarios

Graceful application termination on critical errors

Logging System
The system maintains detailed audit logs in the process_logs table:

INFO logs for successful operations

ERROR logs for failures with detailed messages

Timestamped records for process monitoring

Task-specific logging for debugging

Modular Architecture
Separated concerns with dedicated modules for database, Excel, and configuration

Easy to maintain and extend individual components

Centralized configuration management

Customization
To adapt for different Excel formats:

Update cell ranges in config/config.py

Modify table schemas in database_operation.py if needed

Adjust data extraction logic in excel_operation.py

Troubleshooting
Common Issues:
Database Connection Errors

Verify PostgreSQL is running

Check credentials in config/config.py

Ensure database exists

File Not Found Errors

Verify Excel file path in config/config.py

Check if file exists in the files/ directory

Ensure file name matches DAM_Market Snapshot.xlsx

Module Not Found Errors

Ensure all dependencies are installed: pip install psycopg2 openpyxl

Verify Python path and virtual environment

Permission Errors

Ensure database user has necessary privileges

Check file read permissions for Excel file

Contributing
Fork the repository

Create a feature branch: git checkout -b feature/your-feature

Commit your changes: git commit -m 'Add some feature'

Push to the branch: git push origin feature/your-feature

Open a Pull Request

License
This project is licensed under the MIT License - see the LICENSE file for details.

Author
Your Name

GitHub: @your-username

Acknowledgments
Thanks to the open-source community for the libraries used in this project

Inspired by real-world ETL pipeline requirements

text

This README.md file includes all the essential information that developers typically store in GitHub repositories:

**What's included:**
- **Project title and overview** - Clear description of what the project does
- **Visual project structure** - Easy-to-understand directory layout
- **Prerequisites** - What needs to be installed before running
- **Step-by-step installation** - Detailed setup instructions
- **Usage instructions** - How to run the application
- **Technical documentation** - Detailed explanation of each component
- **Database schema** - Table structures and relationships
- **Configuration guide** - How to customize for different environments
- **Features list** - Key capabilities of the system
- **Troubleshooting** - Common issues and solutions
- **Contributing guidelines** - How others can contribute
- **License information** - Legal usage terms
- **Author information** - Project creator details
- **Acknowledgments** - Credits and references

This README follows GitHub best practices and provides everything needed for other developers to understand, use, and contribute to your project.
