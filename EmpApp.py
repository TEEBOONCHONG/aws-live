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


@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    emp_image_file = request.files['emp_image_file']
    salary = request.form['salary']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location, salary))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=emp_name)



def showimage(bucket):
    s3_client = boto3.client('s3')
    public_urls = []
    emp_id = request.args['emp_id']
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 100)
            public_urls.append(presigned_url)
    except Exception as e:
        pass
    # print("[INFO] : The contents inside show_image = ", public_urls)
    return public_urls



@app.route("/fetchdata", methods=['GET'])
def GetEmp():
    emp_id = request.args['emp_id']
    mycursor = db_conn.cursor()
    getempdata = "select * from employee WHERE emp_id = %s"
    mycursor.execute(getempdata,(emp_id))
    result = mycursor.fetchall()
    (emp_id,first_name,last_name,pri_skill,location,salary) = result[0]
    image_url = showimage(bucket)

    return render_template('GetEmpOutput.html', id=emp_id,fname=first_name,lname=last_name,interest=pri_skill,location=location,salary=salary,image_url=image_url)




@app.route("/applyleave", methods=['POST'])
def ApplyLeave():
    emp_id = request.form['emp_id']
    date_leave = request.form['str(date_leave)']
    reason_leave = request.form['reason_leave']
    support_doc_file = request.files['leave_document']

    insert_sql = "INSERT INTO empLeave VALUES (%s, %s, %s)"
    cursor = db_conn.cursor()

    if support_doc_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (emp_id, date_leave, reason_leave))
        db_conn.commit()
        # Uplaod image file in S3 #
        support_doc_file_in_s3 = "emp-id-" + str(emp_id) + "_support_doc_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading evidence to S3...")
            s3.Bucket(custombucket).put_object(Key=support_doc_file_in_s3, Body=support_doc_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                support_doc_file_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('GetLeaveOutput.html', id=emp_id, date=date_leave, reason=reason_leave)



@app.route("/payroll", methods=['GET', 'POST'])
def Payroll():
    emp_id = request.form['emp_id']
    salary = request.form['salary']
    deduct = request.form['deduct']

    select_sql = "SELECT (%s) FROM employee WHERE emp_id=emp_id"
    insert_sql = "INSERT INTO employee VALUES (%s) WHERE emp_id=emp_id"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (salary))
        cursor.execute(insert_sql, (deduct))
        db_conn.commit()
        new_salary = salary - deduct

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('GetPayrollOutput.html', id=emp_id, salary=salary, deduct=deduct, new_salary=new_salary)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
