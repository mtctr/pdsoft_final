# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_mysqldb import MySQL
from datetime import date
from users import User

import sys
import os
import cgi

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

# MySQL configuration variables
app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'include'
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
mysql = MySQL(app)

# Upload configuration variables
app.config['PICTURES_FOLDER'] = 'static/users/pictures'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg'])

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route("/", methods=["GET", "POST"])
def hello():
    if not current_user.is_anonymous:
        return render_template("home.html", pic=current_user.picture)
    else:
        return render_template("home.html")


@app.route('/', methods=["GET", "POST"])
def login():
    login = 0  # 0 - login / 1 - login com sucesso/ 2 - login invalido/ 3 - senha invalida
    cur = mysql.connection.cursor()
    if request.method == "POST":
        username = request.form["lg_username"]
        password = request.form["lg_password"]
        cur.execute("SELECT login, password, picture FROM members WHERE login = '{}';".format(username))
        tup = cur.fetchone()

        if not tup:
            login = 2
        else:
            if tup[1] != password:
                login = 3
            else:
                login = 1
                user = User(tup[0],tup[1],tup[2])
                login_user(user)
                return render_template("home.html", pic = current_user.picture)

    return render_template("home.html")

@login_manager.user_loader
def load_user(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT login, password, picture FROM members WHERE login = '{}';".format(user_id))
        tup = cur.fetchone()
        return User(tup[0], tup[1], tup[2])
    except mysql.connection.IntegrityError:
        return None

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("home.html")




if __name__ == "__main__":
    app.run(threaded=True, debug=True, host="0.0.0.0")
