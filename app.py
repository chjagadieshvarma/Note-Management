from flask import Flask,redirect,render_template,request,session
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)
app.secret_key="Note_Management_System_key"

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="NoteManagement"
)

@app.route('/')
def home():
    return f"Welcome to Note Management System"

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']

        hashed_password=generate_password_hash(password)

        cursor=conn.cursor()
        cursor.execute("insert into users(email,username,password)values(%s,%s,%s)",
                       (email,username,hashed_password))
        conn.commit()
        cursor.close()
        return f"""Registration successful...<a href="/login">Login</a>"""
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        cursor=conn.cursor()
        cursor.execute("select * from users where username=%s",(username,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            hashed_password=user[3]
            if check_password_hash(hashed_password,password):
                session['login']=True
                session['user_id']=user[0]
                session['username']=user[1]
                return "Login successful...!"
            else:
                return """Invalid login details <a href="/login">Login</a> """
        else:
            return """user not found <a href="/register">Register</a> """
    return render_template('login.html')



app.run(debug=True)
