# -*- coding: utf-8 -*-
from flask import Flask, flash, render_template, request, session
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
app.config['MYSQL_DB'] = 'trampolim'
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
mysql = MySQL(app)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/", methods=["GET", "POST"])
def hello():
    if not current_user.is_anonymous:
        return render_template("home.html")
    else:
        return render_template("home.html")

@app.route("/cadastroGRE", methods=["GET", "POST"])
def cadastroGRE():
    cur = mysql.connection.cursor()

    if request.method =="POST":
        data_envio = request.form["cd_date"]
        id_onibus = request.form["cd_onibus"]
        remessa = request.form["cd_remessa"]
        id_validador = request.form["cd_validador"]

        cur.execute("INSERT INTO GRE (data_envio, id_onibus, remessa, id_validador) VALUES ('{}', '{}', '{}', '{}');".format(data_envio, id_onibus, remessa, id_validador))
        flash("Cadastro realizado com sucesso!")


    return render_template("cadastroGRE.html")

@app.route("/cadastroOnibus", methods=["GET", "POST"])
def cadastroOnibus():
    cur = mysql.connection.cursor()

    if request.method =="POST":
        id_onibus = request.form["cd_onibus"]
        id_validador = request.form["cd_validador"]

        cur.execute("INSERT INTO Onibus(id_onibus,id_validador) VALUES ('{}','{}');".format(id_onibus,id_validador))
        flash("Cadastro realizado com sucesso!")


    return render_template("cadastroOnibus.html")

@app.route("/cadastroValidador", methods=["GET", "POST"])
def cadastroValidador():
    cur = mysql.connection.cursor()

    if request.method =="POST":
        id_onibus = request.form["cd_onibus"]
        id_validador = request.form["cd_validador"]

        if id_onibus != "":
            cur.execute("INSERT INTO Validadores(num_serie,id_onibus) VALUES ('{}','{}');".format(id_validador, id_onibus))
            flash("Cadastro realizado com sucesso!")
        else:
            cur.execute("INSERT INTO Validadores(num_serie) VALUES ('{}');".format(id_validador))
            flash("Cadastro realizado com sucesso!")



    return render_template("cadastroValidador.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    login = 0  # 0 - login / 1 - login com sucesso/ 2 - login invalido/ 3 - senha invalida
    cur = mysql.connection.cursor()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cur.execute("SELECT username, password FROM admin WHERE username = '{}';".format(username))
        tup = cur.fetchone()

        if not tup:
            login = 2
        else:
            if tup[1] != password:
                login = 3
            else:
                login = 1
                user = User(tup[0],tup[1])
                login_user(user)
                return render_template("home.html")

    return render_template("home.html")

@login_manager.user_loader
def load_user(user_id):
    username = user_id
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password FROM admin WHERE username = '{}';".format(username))
        tup = cur.fetchone()
        return User(tup[0], tup[1])
    except mysql.connection.IntegrityError:
        return None

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("home.html")




if __name__ == "__main__":
    app.run(threaded=True, debug=True, host="0.0.0.0")
