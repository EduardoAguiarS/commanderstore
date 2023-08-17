from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (current_user, LoginManager,
                         login_user, logout_user,
                         login_required)
import hashlib


# Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:edu19961016@localhost:3306/commanderstore'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# App Context
db = SQLAlchemy(app)
app.app_context().push()


# Login manager
app.secret_key = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'


# Database models
class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('usr_id', db.Integer, primary_key=True)
    nome = db.Column('usr_nome', db.String(250))
    email = db.Column('usr_email', db.String(250))
    senha = db.Column('usr_senha', db.String(250))

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def __repr__(self):
        return f'Usuario {self.nome}'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    desc = db.Column('cat_desc', db.String(256))

    def __init__(self, nome, desc):
        self.nome = nome
        self.desc = desc


class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    nome = db.Column('anu_nome', db.String(256))
    desc = db.Column('anu_desc', db.String(256))
    preco = db.Column('anu_preco', db.Float)
    cat_id = db.Column('cat_id', db.Integer, db.ForeignKey("categoria.cat_id"))
    usr_id = db.Column('usr_id', db.Integer, db.ForeignKey("usuario.usr_id"))

    def __init__(self, nome, desc, preco, cat_id, usr_id):
        self.nome = nome
        self.desc = desc
        self.preco = preco
        self.cat_id = cat_id
        self.usr_id = usr_id


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('notfound.html'), 404


# Link to css
@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


# link to js bootstrap
@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


# Routes
# Home page
@app.route('/')
def index():
    # Query last 5 anuncios
    anuncios = Anuncio.query.order_by(Anuncio.id.desc()).limit(5).all()
    return render_template('index.html', usuarios=Usuario.query.all(), anuncios=anuncios, title='Home')


# Sign up page
@app.route('/signup')
def signup():
    return render_template('signup.html', title='Cadastro')


# New user
@app.route('/usuario/criar', methods=['POST'])
def criarusuario():
    hash = hashlib.sha512(str(request.form.get('password'))
                          .encode('utf-8')).hexdigest()
    usuario = Usuario(
        request.form.get('name'),
        request.form.get('email'),
        hash
    )
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('signin'))


# User details
@app.route('/usuario/detalhes/<int:id>')
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome


# Edit user
@app.route('/usuario/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editarusuario(id):
    hash = hashlib.sha512(str(request.form.get('password'))
                          .encode('utf-8')).hexdigest()

    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('name')
        usuario.email = request.form.get('email')
        usuario.senha = hash
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editarusuario.html', usuario=usuario, title='Editar')


# Delete user
@app.route('/usuario/deletar/<int:id>')
@login_required
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)


# Sign in page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    hash = hashlib.sha512(str(request.form.get('password'))
                          .encode('utf-8')).hexdigest()

    if request.method == 'POST':
        usuario = Usuario.query.filter_by(
            email=request.form.get('email')).first()
        if usuario and usuario.senha == hash:
            login_user(usuario)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            return redirect(url_for('signin'))
    return render_template('signin.html', title='Login')


# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Categories page
@app.route('/config/categorias')
@login_required
def categorias():
    return render_template('categorias.html', title='Categorias', categorias=Categoria.query.all())


# New category
@app.route('/categorias/criar', methods=['POST'])
@login_required
def categorias_novo():
    categoria = Categoria(
        request.form.get('name'),
        request.form.get('desc')
    )
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categorias'))


# Edit category
@app.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.nome = request.form.get('name')
        categoria.desc = request.form.get('desc')
        db.session.commit()
        return redirect(url_for('categorias'))
    return render_template('editarcategoria.html', categoria=categoria, title='Editar')


# Delete category
@app.route('/categorias/deletar/<int:id>')
@login_required
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categorias'))


# Products page
@app.route('/anuncios')
@login_required
def anuncios():
    return render_template(
        'anuncios.html',
        title='Anuncios',
        anuncios=Anuncio.query.all(),
        categorias=Categoria.query.all()
    )


# New product
@app.route('/anuncios/criar', methods=['POST'])
@login_required
def anuncios_novo():
    anuncio = Anuncio(
        request.form.get('name'),
        request.form.get('desc'),
        request.form.get('preco'),
        request.form.get('cat'),
        request.form.get('usr')
    )
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncios'))


# Ver produto
@app.route('/anuncios/detalhes/<int:id>')
def anuncio_detalhes(id):
    anuncio = Anuncio.query.get(id)
    return anuncio.nome


# Edit product
@app.route('/anuncios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editaranuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method == 'POST':
        anuncio.nome = request.form.get('name')
        anuncio.desc = request.form.get('desc')
        anuncio.preco = request.form.get('preco')
        anuncio.cat_id = request.form.get('cat')
        db.session.commit()
        return redirect(url_for('anuncios'))
    return render_template('editaranuncio.html', anuncio=anuncio, categorias=Categoria.query.all(), title=anuncio.nome)


# Delete product
@app.route('/anuncios/deletar/<int:id>')
@login_required
def deletaranuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('anuncios'))


@app.route('/produtos/<id>')
@login_required
def produto(id):
    return render_template('produto.html', id=id, title='Produto')


@app.route('/favoritos')
@login_required
def favoritos():
    return render_template('favoritos.html', title='Favoritos')


# Run app
if __name__ == 'COMMANDERSTORE':
    print("Rodando...")
    db.create_all()
