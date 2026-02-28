from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Rota Principal - Serve o HTML para o Browser
@app.route('/')
def home():
    # O Flask procura automaticamente na pasta /templates
    return render_template('register.html')

# Rota de Processamento - Recebe os dados do formulário
@app.route('/register', methods=['POST'])
def register():
    nome = request.form.get('nome_completo')
    email = request.form.get('email')
    password = request.form.get('password')

    # Guardar no Banco de Dados
    with sqlite3.connect('utilizadores.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO usuarios (nome, email, password) VALUES (?, ?, ?)", 
                    (nome, email, password))
        con.commit()
    
    # Redireciona de volta para a página inicial após sucesso
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Cria a tabela se não existir
    with sqlite3.connect('utilizadores.db') as con:
        con.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, password TEXT)''')
    
    # Inicia o servidor web
    app.run(debug=True)