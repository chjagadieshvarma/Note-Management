from flask import Flask
import mysql.connector

app=Flask(__name__)

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="NoteManagement"
)

@app.route('/')
def home():
    return f"Welcome to Note Management System"

app.run(debug=True)
