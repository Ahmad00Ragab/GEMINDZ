#====================================================================================================================#
# Filename   : app.py
# Author     : Ahmad Ragab Mohamed
# Description: This Python code defines a RESTful API using Flask for managing test cases and their execution results,
#              and also Creates two SQLite database tables named TestCases and Results using the sqlite3 module
# Created on : Feb 25, 2024                                  
#====================================================================================================================#


'''' 
    # =========================================================== #
    #       Our Database will have the following two tables       #
    # =========================================================== #
   
    
    # Testcases Table and this how it looks like :
    CREATE TABLE IF NOT EXISTS TestCases (
                        TestCaseID INTEGER PRIMARY KEY,
                        Name            TEXT ,
						Description	    TEXT,
						Preconditions	TEXT,
						Steps	        TEXT,
						ExpectedResult	TEXT,
						Priority	    TEXT,
						Status	        TEXT 
    
    # Results Table and this how it looks like :
    CREATE TABLE IF NOT EXISTS Results (
                        ResultID INTEGER PRIMARY KEY,
                        TestCaseID INTEGER,
                        Test_Asset TEXT,
                        ActualResult TEXT,
                        DateExecuted	TEXT,
                        PassFail	TEXT, 
                        Comments	TEXT,
                        FOREIGN KEY (TestCaseID) REFERENCES TestCases(TestCaseID)
    
    
    
    # =========================================================== #
    #                      Routes  used in our APP                #
    # =========================================================== #

/                        : This route returns a simple HTML response indicating that the Flask API is for test case management.
/createTestCase          : This is a POST endpoint for creating a new test case. It expects JSON data containing various attributes of a test case and inserts it into the database.
/getAllTestCases         : This is a GET endpoint for retrieving all test cases from the database.
/getTestCase/<int:id>    : This is a GET endpoint for retrieving a single test case by its ID.
/updateTestCase/<int:id> : This is a PUT endpoint for updating an existing test case by its ID.
/deleteTestCase/<int:id> : This is a DELETE endpoint for deleting a test case by its ID.
/testCases/<int:id>/executionResult : This is a POST endpoint for recording the execution result of a test case for a specific test asset.
/testCases/executionResult/<testAsset> : This is a GET endpoint for retrieving the execution results of all test cases for a specific test asset.        


'''


#====================================================================================================================#
                                                   # Imports #
#====================================================================================================================#
# imports necessary modules including:
# Flask  : for creating the web application, 
# request: for handling HTTP requests,
# jsonify: for creating JSON responses, and
# sqlite3: for interacting with an SQLite database. 
# wraps  : used when defining decorators to preserve the metadata (such as function name, docstring, etc.) of the original function being decorated
from   flask import Flask,request,jsonify
import sqlite3 
from   functools import wraps


#====================================================================================================================#
                                        # Creating DataBase #
#====================================================================================================================#

# Function to create the database tables
def createTables():
    conn = sqlite3.connect('testCases.db') # create a database [if not created] called 'testCases.db' and connect with it 
    cursor = conn.cursor() # cursor to execute SQL commands and interact with the database

    # Create TestCases table
    cursor.execute('''CREATE TABLE IF NOT EXISTS TestCases (
                        TestCaseID INTEGER PRIMARY KEY,
                        Name TEXT ,
						Description	TEXT,
						Preconditions	TEXT,
						Steps	TEXT,
						ExpectedResult	TEXT,
						Priority	TEXT,
						Status	TEXT                 	
                    )''')

    # Create Results table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Results (
                        ResultID INTEGER PRIMARY KEY,
                        TestCaseID INTEGER,
                        TestAsset TEXT,
                        ActualResult TEXT,
                        DateExecuted	TEXT,
                        PassFail	TEXT, 
                        Comments	TEXT,
                        FOREIGN KEY (TestCaseID) REFERENCES TestCases(TestCaseID)             
                    )''')
    conn.commit()
    conn.close()

# Call createTables To create te Database Tables : TestCase & Results
createTables()


#====================================================================================================================#
                                    # Initialization and Setting Password & Username #
#====================================================================================================================#
# The Flask application is initialized, and a variable DATABASE is set to 'testCases.db',
# indicating the SQLite database file to be used.
app = Flask(__name__)
DATABASE = 'testCases.db'

# Hardcoded username and password
USERNAME = "GEMINDZ"
PASSWORD = "123456"


#====================================================================================================================#
                                 # Endpoints Creation & Assoiciative Function Definitions  #
#====================================================================================================================#

# Python decorator used in Flask to define the root endpoint
@app.route('/') 
# welcoming Function
def index(): # This function will be executed when a client accesses the root URL of the Flask application. 
    return '<center><b>Welecome to Our Flask API for Test Case Management</b></center>'


# Function to verify username and password
def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

# Decorator for authentication
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not authenticate(auth.username, auth.password):
            return jsonify({'message': 'Authentication failed!'}), 401
        return f(*args, **kwargs)
    return decorated


# Function to get a database connection
def get_DB_connection(): 
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Endpoint to create a new test case
@app.route('/createTestCase', methods=['POST'])
@requires_auth
def createTestCase():
    try:
        data           = request.get_json()
        Name           = data['Name']
        Description    = data['Description']
        Preconditions  = data['Preconditions']
        Steps	       = data['Steps']
        ExpectedResult = data['ExpectedResult']
        Priority	   = data['Priority']
        Status	       = data['Status']
        # Validate data
        if not Name or not Description or not Preconditions or not Steps or not ExpectedResult or not Priority or not Status:
            return jsonify({'error': 'Name, Description, Preconditions, Steps, ExpectedResult, Priority, Status are required.'}), 400

        conn = get_DB_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO TestCases (Name, Description, Preconditions, Steps, ExpectedResult, Priority, Status) VALUES (?, ?, ?, ?, ?, ?, ?)", (Name, Description, Preconditions, Steps, ExpectedResult, Priority, Status))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Test case created successfully.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint to retrieve all test cases
@app.route('/getAllTestCases', methods=['GET'])
@requires_auth
def getAllTestCases():
    try:
        conn = get_DB_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TestCases")
        rows = cursor.fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint to retrieve a single test case by its ID
@app.route('/getTestCase/<int:id>', methods=['GET'])
@requires_auth
def getTestCase(id):
    try:
        conn = get_DB_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TestCases WHERE TestCaseID = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return jsonify(dict(row))
        else:
            return jsonify({'error': 'Test case not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
# Endpoint to update an existing test case
@app.route('/updateTestCase/<int:id>', methods=['PUT'])
@requires_auth
def updateTestCase(id):
    try:
        conn = get_DB_connection()
        cursor = conn.cursor()
        
        # Check if the test case exists
        cursor.execute("SELECT * FROM TestCases WHERE TestCaseID = ?", (id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Test case not found.'}), 404
        
        # parsing the incoming request       
        data           = request.get_json()
        Name           = data['Name']
        Description    = data['Description']
        Preconditions  = data['Preconditions']
        Steps	       = data['Steps']
        ExpectedResult = data['ExpectedResult']
        Priority	   = data['Priority']
        Status	       = data['Status']

        # Validate data
        if not Name or not Description or not Preconditions or not Steps or not ExpectedResult or not Priority or not Status:
            return jsonify({'error': 'Name, Description, Preconditions, Steps, ExpectedResult, Priority, Status are required.'}), 400

        # if Valid Data , Update
        cursor.execute("UPDATE TestCases SET Name = ?, Description = ? , Preconditions = ?, Steps = ? , ExpectedResult = ? , Priority = ?, Status = ? WHERE TestCaseID = ?", (Name, Description, Preconditions, Steps, ExpectedResult, Priority, Status, id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Test case updated successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint to delete a test case by its ID
@app.route('/deleteTestCase/<int:id>', methods=['DELETE'])
@requires_auth
def deleteTestCase(id):
    try:
        conn = get_DB_connection()
        cursor = conn.cursor()

        # Check if the test case exists
        cursor.execute("SELECT * FROM TestCases WHERE TestCaseID = ?", (id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Test case not found.'}), 404

        # Delete the test case
        cursor.execute("DELETE FROM TestCases WHERE TestCaseID = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Test case deleted successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint to record the execution result of a test case for a specific TestAsset
@app.route('/testCases/<int:id>/executionResult', methods=['POST'])
@requires_auth
def recordExecutionResult(id):
    try:
        # connect to the database
        conn = get_DB_connection()
        cursor = conn.cursor()    
        # parsing the data 
        data = request.get_json()
        TestCaseID    = data['TestCaseID']
        TestAsset     = data['TestAsset']
        ActualResult  = data['ActualResult']
        DateExecuted  = data['DateExecuted']
        PassFail      = data['PassFail']
        Comments      = data['Comments']
        
        # Validate data
        if not TestCaseID or not TestAsset or not ActualResult or not DateExecuted or not Comments or PassFail not in ['Pass', 'Fail']:
            return jsonify({'error': 'TestCaseID, TestAsset, ActualResult, DateExecuted, Comments, PassFail are required.'}), 400
        
        #if Valid Data, insert the data into the Result Table 
        cursor.execute("INSERT INTO Results (TestCaseID, TestAsset, ActualResult, DateExecuted, PassFail, Comments) VALUES (?, ?, ?, ?, ?, ?)", (id, TestAsset, ActualResult, DateExecuted, PassFail, Comments))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Execution Result recorded successfully.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint to retrieve the execution results of all test cases for a specific TestAsset
@app.route('/testCases/executionResult/<testAsset>', methods=['GET'])
@requires_auth
def getExecutionResults(testAsset):
    try:
        conn = get_DB_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Results WHERE TestAsset = ?", (testAsset,))
        rows = cursor.fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Ensure that the script is run only if it is the main module being executed and run the application
if __name__ == '__main__':
    app.run(debug=True)

