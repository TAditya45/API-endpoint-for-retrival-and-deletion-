from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime
import sqlite3

#creating a Flask application and an API for the application using the Flask-RESTful 
app = Flask(__name__)
api = Api(app)

# connecting  to an SQLite database
def get_db():
    conn = sqlite3.connect('calls.db')
    return conn

#Creating a class which represents the resource of  RESTful API for Post method
class InitiateCall(Resource):
    def post(self):
        data = request.get_json()
        from_number = data['from_number']
        to_number = data['to_number']
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db()
        cursor = conn.cursor()

        query = "INSERT INTO calls(from_number, to_number, start_time) VALUES (?, ?, ?)"
        cursor.execute(query, (from_number, to_number, start_time))

        conn.commit()
        conn.close()

        return {"success": True}

#Creating another class which represents the resource of  RESTful APi for GET method
#The below code is an endpoint to retrive the details 
class CallReport(Resource):
    def get(self):
        phone = request.args.get('phone')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        conn = get_db()
        cursor = conn.cursor()

        query = "SELECT id, from_number, to_number, start_time FROM calls WHERE from_number = ? or to_number = ? LIMIT ? OFFSET ?"
        cursor.execute(query, (phone, phone, per_page, (page-1) * per_page))

        data = cursor.fetchall()
        calls = []
        for call in data:
            calls.append({
                "id": call[0],
                "from_number": call[1],
                "to_number": call[2],
                "start_time": call[3]
            })

        conn.commit()
        conn.close()

        return {"success": True, "data": calls}
#Creating a class for updating the record
class UpdateCall(Resource):
    def put(self, id):
        data = request.get_json()
        from_number = data.get('from_number')
        to_number = data.get('to_number')

        conn = get_db()
        cursor = conn.cursor()

        query = "UPDATE calls SET from_number=?, to_number=? WHERE id=?"
        cursor.execute(query, (from_number, to_number, id))

        conn.commit()
        conn.close()

        return {"success": True}

#Creating a class for deleting the record
class DeleteCall(Resource):
    def delete(self, id):
        conn = get_db()
        cursor = conn.cursor()

        query = "DELETE FROM calls WHERE id=?"
        cursor.execute(query, (id,))

        conn.commit()
        conn.close()

        return {"success": True}

#Mapping the resources to the respective end-points
api.add_resource(InitiateCall, '/initiate-call')
api.add_resource(CallReport, '/call-report')
api.add_resource(UpdateCall, '/update-call/<int:id>')
api.add_resource(DeleteCall, '/delete-call/<int:id>')


 
if __name__ == '__main__':
#setting up a database to store call information and running a Flask application which will use the above endpoints for the operations.
    conn = get_db()
    cursor = conn.cursor()

    query = "CREATE TABLE IF NOT EXISTS calls (id INTEGER PRIMARY KEY AUTOINCREMENT, from_number TEXT, to_number TEXT, start_time TEXT)"
    cursor.execute(query)

    conn.commit()
    conn.close()
    app.run(debug=True)
