from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "slb_melhor_do_mundo" # Necessário para o flash() funcionar

# Rota para a página de Login (falta-te esta!)
@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/")
def principal():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def registrar():
    username = request.form.get("nome")
    senha = request.form.get("senhaa")
    n_socio = request.form.get("nsocio")
    senha_confirm = request.form.get("senha2")
    email = request.form.get("email")
    
    # Validação simples
    if len(senha) < 8:
        flash("Senha pequena demais! Mínimo 8 caracteres.")
        return redirect(url_for('principal'))

    try:
        with sqlite3.connect("teste.db") as conn:
            cur = conn.cursor()
            # O nome da tabela deve ser 'usuarios' para bater certo com o create
            cur.execute("INSERT INTO usuarios (username, email, n_socio, senha) VALUES (?, ?, ?, ?)", 
                       (username, email, n_socio, senha))
            conn.commit()
    except Exception as e:
        flash(f"Erro ao registar: {e}")
        return redirect(url_for('principal'))

    return redirect(url_for('login_page')) # Redireciona para a função da página de login

if __name__ == "__main__":
    # Criar a tabela corretamente antes de correr o app
    with sqlite3.connect("teste.db") as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT, 
            email TEXT, 
            n_socio INTEGER UNIQUE, 
            senha TEXT NOT NULL)""")
    
    app.run(debug=True)