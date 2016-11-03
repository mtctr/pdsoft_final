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
    cadastro = 0
    cur.execute("SELECT * FROM defeito")
    row = cur.fetchall()

    defeitos = []
    for r in row:
        defeitos.append(
            dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

    if request.method =="POST":
        data_envio = request.form["cd_date"]
        id_onibus = request.form["cd_onibus"]
        remessa = request.form["cd_remessa"]
        id_validador = request.form["cd_validador"]
        tipo_defeito = request.form["defeito"]
        try:
            cur.execute("INSERT INTO gre (data_envio, id_onibus, remessa, id_validador) VALUES ('{}', '{}', '{}', '{}');".format(data_envio, id_onibus, remessa, id_validador))
            cur.execute("SELECT id_gre FROM gre WHERE remessa = '{}';".format(remessa))
            tup = cur.fetchone()
            id_gre = tup[0]
            print tipo_defeito
            cur.execute("INSERT INTO lista_defeitos(id_gre, tipo_defeito) VALUES ('{}', '{}');".format(id_gre, tipo_defeito))
            mysql.connection.commit()
            cadastro = 1
        except mysql.connection.IntegrityError:
            cadastro = 3
        finally:
            cur.close()


    return render_template("cadastroGRE.html", defeitos = defeitos, cadastro = cadastro)

@app.route("/cadastroOnibus", methods=["GET", "POST"])
def cadastroOnibus():
    cur = mysql.connection.cursor()
    cadastro = 0

    if request.method =="POST":
        id_onibus = request.form["cd_onibus"]
        id_validador = request.form["cd_validador"]
        try:
            cur.execute("INSERT INTO onibus(id_onibus,id_validador) VALUES ('{}','{}');".format(id_onibus,id_validador))
            cur.execute("UPDATE validadores SET id_onibus = '{}' WHERE num_serie = '{}';".format(id_onibus,id_validador))
            mysql.connection.commit()
            cadastro = 1
        except mysql.connection.IntegrityError:
            cadastro = 3
        finally:
            cur.close()

    return render_template("cadastroOnibus.html", cadastro=cadastro)

@app.route("/cadastroValidador", methods=["GET", "POST"])
def cadastroValidador():
    cur = mysql.connection.cursor()
    cadastro = 0
    if request.method =="POST":
        id_onibus = request.form["cd_onibus"]
        id_validador = request.form["cd_validador"]
        try:
            if id_onibus != "":
                cur.execute("SELECT id_onibus FROM onibus WHERE id_onibus = '{}';".format(id_onibus))
                tup = cur.fetchone()
                #verifica se o onibus já está cadastrado, caso não estiver, será cadastrado
                if not tup:
                    cur.execute("INSERT INTO validadores(num_serie) VALUES ('{}');".format(id_validador))
                    cur.execute("INSERT INTO onibus VALUES ('{}','{}')".format(id_onibus, id_validador))
                    cur.execute("UPDATE validadores SET id_onibus = '{}' WHERE num_serie = '{}';".format(id_onibus, id_validador))
                else:
                    cur.execute("INSERT INTO validadores(num_serie,id_onibus) VALUES ('{}','{}');".format(id_validador, id_onibus))
                    cur.execute("UPDATE onibus SET id_validador = '{}' WHERE id_onibus = '{}';".format(id_validador,id_onibus))
            else:
                cur.execute("INSERT INTO validadores(num_serie) VALUES ('{}');".format(id_validador))

            mysql.connection.commit()
            cadastro = 1
        except mysql.connection.IntegrityError:
            cadastro = 3
        finally:
            cur.close()

    return render_template("cadastroValidador.html", cadastro = cadastro)

@app.route('/busview')
def dbBus():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM onibus")
    row = cur.fetchall()

    onibus = []
    for r in row:
        onibus.append(
            dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

    print onibus
    return render_template("busview.html", onibus=onibus)

@app.route('/valview')
def dbValidador():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM validadores")
    row = cur.fetchall()

    validadores = []
    for r in row:
        validadores.append(
            dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

    print validadores
    return render_template("valview.html", validadores=validadores)

@app.route('/greview')
def dbGRE():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM gre")
    row1 = cur.fetchall()

    cur.execute("SELECT * FROM lista_defeitos")
    row2 = cur.fetchall()

    gre = []
    for r in row1:
        gre.append(
            dict((cur.description[idx][0], value) for idx, value in enumerate(r)))
    defeitos = []
    for r in row2:
        defeitos.append(
            dict((cur.description[idx][0], value) for idx, value in enumerate(r)))
    print gre
    print defeitos
    return render_template("greview.html", gre=gre, defeitos = defeitos)

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
