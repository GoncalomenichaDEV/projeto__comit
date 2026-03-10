from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "slb_sempre" # Obrigatório para o flash()

# --- FUNÇÃO AUXILIAR PARA A BASE DE DADOS ---
def iniciar_db():
    with sqlite3.connect("teste.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username TEXT, 
                email TEXT UNIQUE, 
                n_socio TEXT, 
                senha TEXT NOT NULL
            )
        """)
        conn.commit()

# --- ROTAS DE NAVEGAÇÃO (GET) ---

@app.route("/")
def pagina_registo():
    # Esta é a página que abre primeiro
    return render_template("register.html")

@app.route("/login")
def pagina_login():
    # Rota para abrir o login.html
    return render_template("login.html")

@app.route("/index")
def index_page():
    # Rota para onde o utilizador vai quando tem sucesso
    return render_template("index.html")

# --- ROTAS DE AÇÃO (POST) ---

@app.route("/register", methods=["POST"])
def registrar():
    nome = request.form.get("nome")
    email = request.form.get("email")
    socio = request.form.get("nsocio")
    senha = request.form.get("senhaa")

    try:
        with sqlite3.connect("teste.db") as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO usuarios (username, email, n_socio, senha) VALUES (?, ?, ?, ?)", 
                       (nome, email, socio, senha))
            conn.commit()
        flash("Registo feito com sucesso! Faz login.")
        return redirect(url_for("pagina_login"))
    except:
        flash("Erro: Este email já está registado!")
        return redirect(url_for("pagina_registo"))

@app.route("/auth", methods=["POST"])
def auth():
  
    e = request.form.get("email")
    s = request.form.get("senha")

    with sqlite3.connect("teste.db") as conn:
        cur = conn.cursor()
       
        cur.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (e, s))
        utilizador = cur.fetchone()

        if utilizador:
            return redirect(url_for("index_page")) 
        else:
            flash("Email ou Senha incorretos!")
            return redirect(url_for("pagina_login")) 

if __name__ == "__main__":
    iniciar_db() 
    app.run(debug=True)