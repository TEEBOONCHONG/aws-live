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
def index():
    return render_template('index.html')

@app.route("/addEmp", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')

@app.route("/find", methods=['GET', 'POST'])
def findEmp():
    return render_template('GetEmp.html')

@app.route("/empLeave", methods=['GET', 'POST'])
def leave():
    return render_template('empLeave.html')

@app.route("/empAttendance", methods=['GET', 'POST'])
def empAttend():
    return render_template('empAttendance.html')


@app.route("/empPayroll", methods=['GET','POST'])
def empUpdate():
    return render_template('empPayroll.html')


@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('www.intellipaat.com')

@app.route("/deleteEmp", methods=['GET','POST'])
def empDelete():
    return render_template("DeleteEmp.html")

@app.route("/editEmp", methods=['GET','POST'])
def empEdit():
    return render_template("EditEmp.html")





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
    getempdata = "SELECT * FROM employee WHERE emp_id = %s"
    mycursor.execute(getempdata,(emp_id))
    result = mycursor.fetchall()
    (emp_id,first_name,last_name,pri_skill,location,salary) = result[0]
    image_url = showimage(bucket)

    return render_template('GetEmpOutput.html', id=emp_id,fname=first_name,lname=last_name,interest=pri_skill,location=location,salary=salary,image_url=image_url)




@app.route("/applyleave", methods=['POST'])
def ApplyLeave():
    emp_id = request.form['emp_id']
    date_leave = request.form['date_leave']
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


@app.route("/empattend", methods=['POST'])
def empAttendance():
    emp_id = request.form['emp_id']
    attstatus = request.form['attstatus']

    insert_sql = "INSERT INTO attendance VALUES (%s, %s)"
    cursor = db_conn.cursor()
    
    try:
        cursor.execute(insert_sql, (emp_id, attstatus))
        db_conn.commit()
        status = "Employee " + emp_id + " has checked in at the date 11 April 2020." 

    except Exception as e:
            return str(e)
    finally:
        cursor.close()
    return render_template('GetAttendanceOutput.html', status=status)



@app.route("/payupdate", methods=['GET','POST'])
def dirpay():
    emp_id = request.form['emp_id']
    salary = request.form['salary']

    updatesql = "UPDATE employee SET salary= %s WHERE emp_id = %s"
    mycursor = db_conn.cursor()
    changefield = (salary, emp_id)
    mycursor.execute(updatesql, (changefield))
    db_conn.commit()
    mycursor.close()
    return render_template("GetPayrollOutput.html")


@app.route("/deleteInfo", methods=['GET','POST'])
def DeleteEmp():
    emp_id = request.form['emp_id']
    mycursor = db_conn.cursor()
    del_emp = "DELETE FROM employee WHERE emp_id = %s"
    mycursor.execute(del_emp, (emp_id))
    db_conn.commit()

    return render_template('GetDeleteOutput.html', emp_id=emp_id)



@app.route("/editdetails", methods=['GET','POST'])
def empedit():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    emp_image_file = request.files['emp_image_file']
    salary = request.form['salary']
    
    update_sql = "UPDATE employee SET first_name = %s, last_name = %s, pri_skill = %s, location = %s, salary = %s WHERE emp_id = %s"
    cursor = db_conn.cursor()
    
    changeInfo = (first_name, last_name, pri_skill, location, salary, emp_id)
    cursor.execute(update_sql, (changeInfo))
    db_conn.commit()
    cursor.close()
    return render_template("GetEditOutput.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
