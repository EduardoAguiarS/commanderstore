from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:edu19961016@localhost:3306/commanderstore'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# App Context
db = SQLAlchemy(app)
app.app_context().push()

# Database models
class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('usr_id', db.Integer, primary_key=True)
    nome = db.Column('usr_nome', db.String(250))
    email = db.Column('usr_email', db.String(250))
    senha = db.Column('usr_senha', db.String(20))

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def __repr__(self):
        return f'Usuario {self.nome}'

# Link to css
@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

# Routes
# Home page
@app.route('/')
def index():
    return render_template('index.html', usuarios=Usuario.query.all())

# Sign up page
@app.route('/signup')
def signup():
    return render_template('signup.html', title='Cadastro')

# Sign up success page
@app.route('/signupsuccess', methods=['POST'])
def signupsuccess():
    usuario = Usuario(
        request.form.get('name'),
        request.form.get('email'),
        request.form.get('password')
    )
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('signin'))

# Sign in page
@app.route('/signin')
def signin():
    return render_template('signin.html', title='Entrar')

@app.route('/produtos')
def produtos():
    return render_template('produtos.html', title='Produtos')

@app.route('/produtos/<id>')
def produto(id):
    return render_template('produto.html', id=id, title='Produto')

@app.route('/favoritos')
def favoritos():
    return render_template('favoritos.html', title='Favoritos')

# Run app
if __name__ == 'commanderstore':
    print("Rodando...")
    db.create_all()
