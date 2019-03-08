from flask import Flask,render_template,jsonify,request,redirect,url_for
import pymysql.cursors
#import pyodbc

app= Flask(__name__)

# connection = pymysql.connect(host='localhost',
#                              user='user',
#                              password='passwd',
#                              db='db',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)


class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "newuser"
        password = ""
        db = "training"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def list_student(self,roll):
    	sql="SELECT * FROM student where Roll_No=%s;"
    	val=(roll)
        self.cur.execute(sql,val)
        #self.con.commit()
        result = self.cur.fetchall()
        return result

    def store_student(self,roll,clas,fname,lname):

    	sql='CALL store_stud(%s,%s,%s,%s)'
    	val2=(roll,fname,lname,clas)
        self.cur.execute(sql,val2)
        self.con.commit()
        result = self.cur.fetchone()
        return result

   #PROC SYNTAX
    	
   #  	sqlodbc1= '''CREATE PROCEDURE store_stud(IN roll INT,IN fname VARCHAR(30),IN lname VARCHAR(30),IN clas VARCHAR(10))
   #  		BEGIN
   #  			IF EXISTS(SELECT * FROM student where Roll_No=roll) THEN
   #  				SELECT 'The Entry already exist!!';
    				
   #  			ELSE
   #  				INSERT into student(Roll_No,FName,LName,Class) values(roll,fname,lname,clas);
   #  				SELECT 'Successfully Stored!!';
   #  			END IF;
			# END;'''
    	
   #  	# val1=(roll,fname,lname,clas)
   #  	self.cur.execute(sqlodbc1)
		

@app.route('/retrieve/<roll>',methods=['GET'])
def retrieve(roll):
	db=Database()
	stu = db.list_student(roll)
	return jsonify(stu)

@app.route('/',  methods=['GET','POST'])
def home():
	return redirect(url_for('store'))

@app.route('/store', methods=['GET','POST'])
def store():
	db=Database()
	if request.method == 'POST':
		fname=request.form['firstname']
		lname=request.form['lastname']
		roll=request.form['rollno']
		clas=request.form['class']
		stu = db.store_student(roll,clas,fname,lname)
		print(stu)
		return str(stu.values()[0])
	return render_template('store.html')
