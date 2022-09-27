from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')

@app.route("/find", methods=['GET', 'POST'])
def findEmp():
    return render_template('GetEmp.html')

@app.route("/empLeave", methods=['GET', 'POST'])
def leave():
    return render_template('empLeave.html')

@app.route("/empPayroll", methods=['GET', 'POST'])
def emppayroll():
    return render_template('empPayroll.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')


@app.route("/fetchdata", methods=['POST'])
def GetEmp():
    emp_id = request.form['emp_id']

    select_sql = "SELECT (%s) FROM employee WHERE emp_id=emp_id"
    cursor = db_conn.cursor()

    try:

        cursor.execute(select_sql, (emp_id))
        db_conn.commit()
        #emp_name = "" + first_name + " " + last_name#
        # Uplaod image file in S3 #
        #emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"#
        s3 = boto3.resource('s3')

        try:
            print("Data selected from MySQL RDS...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            #object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(#
                #s3_location,#
                #custombucket,#
                #emp_image_file_name_in_s3)#

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('GetEmpOutput.html', id=emp_id, fname=first_name, lname=last_name, interest=pri_skill, location=location, image_url=object_url, salary=salary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
