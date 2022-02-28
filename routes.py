import email
import sqlite3 as sql
import os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('formRegister.html')


@app.route('/escrever', methods=['POST', 'GET'])
def grava():
    email = request.form['email']
    nome = request.form['nome']
    senha = request.form['senha']

    if email and nome and senha:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO usuarios (email, nome, senha) VALUES (?,?,?)", (email, nome, senha))

            con.commit()
            msg = "Informações inseridas com sucesso"
            return render_template("formRegister.html", msg=msg)
            con.close()
    else:
        return("Algo saiu errado")


@app.route('/listar')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from usuarios")

    rows = cur.fetchall()
    return render_template("lista.html", rows=rows)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)
