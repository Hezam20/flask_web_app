from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
import psycopg2
import os
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

conn = psycopg2.connect(dbname=os.getenv("dbname"), user=os.getenv("user"), port=os.getenv("port"), password=os.getenv('user_auth'))
cur = conn.cursor()


@app.route("/")
@app.route("/home")
def index(name=None):
    return render_template("index.html", name=name)


@app.route("/about")
def about():
    return "TODO"

@app.route("/register", methods=["GEt", "POST"])
def register():
    if request.method == "GET":
        name = request.args.get("first_name")
        return render_template("register.html")
    form = request.form.to_dict(flat=True)
    if form['password'] != form['confirm_password']:
        return render_template("register.html", error='confirm_password')
    cur.execute("SELECT id FROM people WHERE email = %s", (form['email'],))
    if cur.fetchone():
        return render_template("register.html", exist='email', email=form['email'])
    password = generate_password_hash(form['password'])
    cur.execute("INSERT INTO people (first_name, last_name, email, password, confirm_password) VALUES (%s, %s, %s, %s, %s)",  
    (form['first_name'], form['last_name'], form['email'], password, password))
    conn.commit() 
    cur.close()
    conn.close()
    return render_template("index.html", name=form["first_name"])
