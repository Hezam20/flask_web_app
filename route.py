from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from forms import RegistrationForm, LoginForm
import psycopg2
import os
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '0e31e03058818ff1d3db6ec620545dcb'

conn = psycopg2.connect(dbname=os.getenv("dbname"), user=os.getenv("user"), port=os.getenv("port"), password=os.getenv('user_auth'))
cur = conn.cursor()

posts = [
    {
        'author': 'Lola ',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2020'
    },
    {
        'author': 'Ms piggy',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }

]

@app.route("/")
@app.route("/home")
def home(name=None):
    return render_template("home.html", title='Home', posts=posts)

@app.route("/about")
def about(name=None):
    return render_template("about.html", title="about")

@app.route("/register", methods=["GEt", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "GET":
        return render_template("register_form.html", title='Register', form=form)
    # if form['password'] != form['confirm_password']:
    #     return render_template("register_form.html", error='confirm_password')

    if form.validate_on_submit():
        cur.execute("SELECT email FROM people WHERE email = %s", (form.email.data,))
        is_email_exist = cur.fetchone()
        if is_email_exist:
            return render_template("register_form.html", form=form, is_email_exist=is_email_exist[0])
        password = generate_password_hash(form.password.data)
        cur.execute("INSERT INTO people (first_name, last_name, email, password, confirm_password) VALUES (%s, %s, %s, %s, %s)",  
        (form.first_name.data, form.last_name.data, form.email.data, form.password.data, form.confirm_password.data))
        conn.commit() 
        cur.close()
        conn.close()
        flash(f"Account created for {form.first_name.data}!", "success")
        return redirect("/login")
    return render_template("register_form.html", form=form)


@app.route("/login", methods=["GET", "Post"])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template("login_form.html", title='Login', form=form)
    cur.execute("SELECT * FROM people WHERE email = %s", (form.email.data,))
    is_email_exist = cur.fetchone()
    if not is_email_exist:
            flash(f"This user does not exist!. Please create an accout!", "danger")
            return render_template("login_form.html", title="Login", form=form)
    return redirect("/home", title='Home', posts=posts)