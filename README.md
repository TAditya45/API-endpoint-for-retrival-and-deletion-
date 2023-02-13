# API-endpoint-for-retrival-and-deletion-

The above code is a Python script for building a RESTful API using Flask and Flask-RESTful. The script implements two classes, InitiateCall and CallReport, which handle post and get requests respectively. The InitiateCall class handles the post request to create a new call record in an SQLite database. The call information, including the calling number (from_number), the called number (to_number), and the start time of the call, are stored in the database.

The CallReport class handles the get request to retrieve call records for a given phone number from the database. The phone number, the page number, and the number of items per page are passed as parameters in the get request. The class retrieves the call records from the database and returns the data as a JSON response.

The resources are added to the API and mapped to their respective endpoints, i.e., /initiate-call and /call-report. and you will be able to update and delete a call record using the PUT and DELETE methods respectively. You can access the updated call record by sending a PUT request to /update-call/<id>, where id is the identifier of the call record that you want to update. Similarly, you can delete a call record by sending a DELETE request to /delete-call/<id>, where id is the identifier of the call record that you want to delete.

The if __name__ == '__main__': block is used to set up the database and start the Flask application, which listens for incoming requests to the API. The database table, calls, is created if it does not already exist.
