from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import yaml

app= Flask(__name__)

#Configer db
db=yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']

mysql=MySQL(app)
@app.route('/',methods=['GET', 'POST'])
@app.route('/home',methods=['GET', 'POST'])
def home_page():

    return render_template('home.html')

@app.route('/addAdmin',methods=['GET', 'POST'])
def addAdmin():
    if request.method=='POST':
        userDetails=request.form
        name=userDetails['name']
        email=userDetails['email']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO admin (name,email) VALUES(%s, %s)",(name,email))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('addAdmin'))
    return render_template('adminForm.html')
@app.route('/showAdmins',methods=['GET', 'POST'])
def showAdmins():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT user_id,name,email FROM admin")
    if resultValue > 0:
        adminDetails = cur.fetchall()
    if request.method=='POST':
        uid=int(request.form.get('remove'))
        if uid>0:
            cur.execute(f"DELETE FROM admin WHERE user_id={uid}")
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdmins'))


    return render_template('adminTable.html',adminDetails=adminDetails)

@app.route('/complains',methods=['GET', 'POST'])
def complains():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM complain")
    if resultValue > 0:
        complainDetails = cur.fetchall()
    if request.method == 'POST':
        issue_no = int(request.form.get('submit'))
        if issue_no > 0:
            userDetails = request.form
            reply = userDetails['reply']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE complain SET reply= (%s) WHERE issue_no=(%s)",(reply,issue_no))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('complains'))

    return render_template('complain.html',complainDetails=complainDetails)



if __name__=='__main__':
    app.run(debug=True)
