#====================================================================================================================#
# Filename   : unitTestByCommands.py
# Author     : Ahmad Ragab Mohamed
# Description: this file contains a set of curl commands for interacting with a RESTful API related to test case management.
#              Each command corresponds to a specific action such as creating, retrieving, updating, or deleting test cases.
# Created on : Feb 25, 2024                                  
#====================================================================================================================#



# Create Test Case: Sends a POST request to create a new test case with the provided details.
''' 
# with authentication :
curl -X POST http://localhost:5000/createTestCase \
-H "Content-Type: application/json" \
-u "GEMINDZ:123456" \
-d '{
    "Name": "Test Case Name",
    "Description": "Test Case Description",
    "Preconditions": "Test Case Preconditions",
    "Steps": "Test Case Steps",
    "ExpectedResult": "Test Case Expected Result",
    "Priority": "High",
    "Status": "Pending"
}'

'''

# Get All Test Cases: Sends a GET request to retrieve all test cases.
''' 
# with authentication :
curl -X GET http://localhost:5000/getAllTestCases -u "GEMINDZ:123456"

'''


# Get a Single Test Case: Sends a GET request to retrieve a specific test case by its ID.
''' 
# with authentication :
curl -X GET http://localhost:5000/getTestCase/1 -u "GEMINDZ:123456"

'''


# Update a Test Case: Sends a PUT request to update an existing test case with new details.
'''
# with authentication :
curl -X PUT http://localhost:5000/updateTestCase/1 \
-H "Content-Type: application/json" \
-u "GEMINDZ:123456" \
-d '{
        "Name": "Test Case Name",
        "Description": "Test Case Description",
        "Preconditions": "Test Case Preconditions",
        "Steps": "Test Case Steps",
        "ExpectedResult": "Test Case Expected Result",
        "Priority": "Low",
        "Status": "Completed"
}'

'''

# Delete a Test Case: Sends a DELETE request to delete a specific test case by its ID.
'''
# with authentication :
curl -X DELETE http://localhost:5000/deleteTestCase/1 -u "GEMINDZ:123456"

'''

# Record a Test Case Result: Sends a POST request to record the execution result of a test case,
# including details such as the actual result, date executed, pass/fail status, and comments.
'''
# with authentication :
curl -X POST http://localhost:5000/testCases/1/executionResult \
-H "Content-Type: application/json" \
-u "GEMINDZ:123456" \
-d '{
    "TestCaseID": 1,
    "TestAsset": "TestAsset1",
    "ActualResult": "Success",
    "DateExecuted": "2022-02-25",
    "PassFail": "Pass",
    "Comments": "Test case passed successfully."
}'
'''

# Retrieve Execution Results for a Specific Test Asset: Sends a GET request to retrieve the execution results
# of all test cases associated with a specific test asset.
'''
# with authentication :
curl -X GET http://localhost:5000/testCases/executionResult/TestAsset1 -u "GEMINDZ:123456" 

'''


'''
Notes : 
# my private local host is : 127.0.0.1
# ex: curl -X DELETE http://localhost:5000/deleteTestCase/<id>
# username: GEMINDZ
# password: 123456
'''
