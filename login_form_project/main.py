import random
from flask import Flask, render_template,request,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySql Configurations:
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Abhi@mysql8055"
app.config["MYSQL_DB"] = "test"

mysql = MySQL()
mysql.init_app(app)



@app.route("/")
def index():
    return render_template("/index.html.j2")



# login server - side validator:
def login_validate(email: str, password: str):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM second WHERE email = %s AND password = %s", (email, password))
    data_full = cur.fetchone()
    cur.close()

    if data_full:
        return True, data_full
    else:
        return False, None

    

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        truth_value, data_full = login_validate(email, password)
        
        if truth_value:
            return render_template("success.html.j2", data_full=data_full)
        else:
            return render_template("login.html.j2", error="Check your email and password")

    return render_template("/login.html.j2")


@app.route("/signup",methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        # fetch values from form:
        randomNum = random.randint(1000,9999)
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
        dob = request.form['dob']
        contact_number = request.form['contact_number']
        # ------------------------------------
        cur = mysql.connection.cursor()
        cur.execute(f"insert into second values ({randomNum},'{name}','{email}','{password}',{age},'{gender}','{dob}',{contact_number})")
        mysql.connection.commit()
        cur.close()
        return render_template('success.html.j2')
    
    else:
        return render_template('signup.html.j2')


    


if __name__ == "__main__":
    app.run(debug=True)