# -*- coding: utf-8 -*-
from flask import Flask, flash, render_template, request, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_mysqldb import MySQL
from datetime import date
from users import User

import pygal
import sys
import os
import cgi

reload(sys)  # Reload is a hack
sys.setdefaultencoding('UTF8')

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

#CADASTROS:

@app.route("/cadastroGRE", methods=["GET", "POST"])
def cadastroGRE():
    print(sys.getdefaultencoding())
    print(sys.getfilesystemencoding())

    cur = mysql.connection.cursor()
    cadastroGRE = 0

    cur.execute("SELECT tipo_defeito FROM defeito")
    row = cur.fetchall()
    defeitos = []
    for r in row:
        defeitos.append(
            dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

    cur.execute("SELECT id_onibus FROM onibus")
    row = cur.fetchall()
    onibus = []
    for r in row:
        onibus.append(
            dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

    cur.execute("SELECT num_serie FROM validadores")
    row = cur.fetchall()
    validadores = []
    for r in row:
        validadores.append(
            dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

    if request.method =="POST":
        data_envio = request.form["cd_date_envio"]
        data_retorno = request.form["cd_date_retorno"]
        id_onibus = request.form["cd_onibus"]
        pick = request.form["cd_onibus"]
        remessa = request.form["cd_remessa"]
        id_validador = request.form["cd_validador"]
        tipo_defeito = request.form["defeito"]
        observacoes = request.form["observacoes"]
        try:
            cur.execute("INSERT INTO gre (data_envio, data_retorno, id_onibus, remessa, id_validador) VALUES ('{}','{}', '{}', '{}', '{}');".format(data_envio, data_retorno, id_onibus, remessa, id_validador))
            cur.execute("SELECT Max(id_gre) FROM gre;")
            tup = cur.fetchone()
            id_gre = tup[0]
            cur.execute("INSERT INTO lista_defeitos(id_gre, tipo_defeito, observacoes) VALUES ('{}', '{}', '{}');".format(id_gre, tipo_defeito, observacoes))
            mysql.connection.commit()
            cadastroGRE = 1
        except mysql.connection.IntegrityError:
            cadastroGRE = 3
        finally:
            cur.close()


    return render_template("cadastroGRE.html", defeitos = defeitos, onibus = onibus , validadores = validadores , cadastro = cadastroGRE)

@app.route("/cadastroOnibus", methods=["GET", "POST"])
def cadastroOnibus():
    cur = mysql.connection.cursor()
    cadastroOnibus = 0

    cur.execute("SELECT num_serie FROM validadores")
    row = cur.fetchall()
    validadores = []
    for r in row:
        validadores.append(
            dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

    if request.method =="POST":
        id_onibus = request.form["cd_onibus"]
        id_validador = request.form["cd_validador"]
        try:
            cur.execute("INSERT INTO onibus(id_onibus,id_validador) VALUES ('{}','{}');".format(id_onibus,id_validador))
            mysql.connection.commit()
            cadastroOnibus = 1
        except mysql.connection.IntegrityError:
            cadastroOnibus = 3
        finally:
            cur.close()

    return render_template("cadastroOnibus.html",validadores=validadores, cadastro=cadastroOnibus)

@app.route("/cadastroDefeito", methods=["GET", "POST"])
def cadastroDefeito():
    cur = mysql.connection.cursor()
    cadastroDefeito = 0

    if request.method =="POST":
        tipo_defeito = request.form["cd_defeito"].encode('utf-8')
        try:
            cur.execute("INSERT INTO defeito(tipo_defeito) VALUES ('{}');".format(tipo_defeito))
            mysql.connection.commit()
            cadastroDefeito = 1
        except mysql.connection.IntegrityError:
            cadastroDefeito = 3
        finally:
            cur.close()

    return render_template("cadastroDefeito.html", cadastro=cadastroDefeito)

@app.route("/cadastroValidador", methods=["GET", "POST"])
def cadastroValidador():
    cur = mysql.connection.cursor()
    cadastroValidador = 0

    if request.method =="POST":
        id_validador = request.form["cd_validador"]
        try:
            cur.execute("INSERT INTO validadores(num_serie) VALUES ('{}');".format(id_validador))
            mysql.connection.commit()
            cadastroValidador = 1
        except mysql.connection.IntegrityError:
            cadastroValidador = 3
        finally:
            cur.close()

    return render_template("cadastroValidador.html", cadastro = cadastroValidador)

#CONSULTAS:

@app.route('/consulta')
def goToConsulta():
    return render_template("consulta.html")

@app.route('/consultaValidador', methods=["GET", "POST"])
def consultaValidador():
    cur = mysql.connection.cursor()
    consulta = 0

    if request.method =="POST":
        id_validador = request.form["cons"]

        cur.execute("SELECT * FROM validadores WHERE num_serie = '{}';".format(id_validador))
        tup1 = cur.fetchall()
        validador = []
        for r in tup1:
            validador.append(
                dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

        if not tup1:
            return render_template("consulta.html", consulta = 1)
        else:
            cur.execute("SELECT * FROM onibus WHERE id_validador = '{}'".format(id_validador))
            tup2 = cur.fetchall()
            onibus = []
            for r in tup2:
                onibus.append(
                    dict((cur.description[idx][0], value) for idx, value in enumerate(r)))


            cur.execute("SELECT * FROM gre WHERE id_validador = '{}'".format(id_validador))
            tup3 = cur.fetchall()
            gre = []
            for r in tup3:
                gre.append(
                    dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

            return render_template ("consulta.html", consulta = 2, validador = validador, onibus = onibus, gre = gre)

    return render_template("consulta.html")

@app.route('/consultaOnibus', methods=["GET", "POST"])
def consultaOnibus():
    cur = mysql.connection.cursor()
    consulta = 0

    if request.method =="POST":
        id_onibus = request.form["cons"]

        cur.execute("SELECT * FROM onibus WHERE id_onibus = '{}';".format(id_onibus))
        tup1 = cur.fetchall()
        onibus = []
        for r in tup1:
            onibus.append(
                dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

        if not tup1:
            return render_template("consulta.html", consulta = 1)
        else:
            cur.execute("SELECT * FROM gre WHERE id_onibus = '{}'".format(id_onibus))
            tup2 = cur.fetchall()
            gre = []
            for r in tup2:
                gre.append(
                    dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

            return render_template ("consulta.html", consulta = 2, onibus = onibus, gre = gre)

    return render_template("consulta.html")

@app.route('/consultaGRE', methods=["GET", "POST"])
def consultaGRE():
    cur = mysql.connection.cursor()
    consulta = 0

    if request.method =="POST":
        data_envio = request.form["cons"]

        cur.execute("SELECT * FROM gre WHERE data_envio = '{}';".format(data_envio))
        tup1 = cur.fetchall()

        if not tup1:
            return render_template("consulta.html", consulta = 1)
        else:
            gre = []
            for r in tup1:
                gre.append(
                    dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

            return render_template ("consulta.html", consulta = 2, gre = gre)

    return render_template("consulta.html")


@app.route('/graph/<int:type>', methods=["GET", "POST"])
def viewGraph(type):
    cur = mysql.connection.cursor()
    graph = pygal.Bar()
    graph_data = graph.render_data_uri()

    if type == 0:
        #cur.execute("SELECT * FROM gre WHERE data_envio = '{}';".format(data_envio))
        #tup1 = cur.fetchall()
        graph = pygal.Bar()
        graph_data = graph.render_data_uri()

    elif type == 1:
        graph = pygal.Bar()
        graph.title = 'Browser usage evolution (in %)'
        graph.x_labels = map(str, range(2002, 2013))
        graph.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
        graph.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
        graph.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
        graph.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
        graph_data = graph.render_data_uri()
    else:
        pass

    return render_template("graph.html", graph_data = graph_data )

#DEBUG:
@app.route('/busview')
def dbBus():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM onibus")
    row = cur.fetchall()

    onibus = []
    for r in row:
        onibus.append(
            dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

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

    return render_template("valview.html", validadores=validadores)

@app.route('/greview')
def dbGRE():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM gre")
    row1 = cur.fetchall()

    gre = []
    for r in row1:
        gre.append(
            dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

    cur.execute("SELECT * FROM lista_defeitos")
    row2 = cur.fetchall()
    defeitos = []
    for r in row2:
        defeitos.append(
            dict((cur.description[idx][0], value) for idx, value in enumerate(r)))

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
