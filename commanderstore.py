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


# Routes
# Home page
@app.route('/')
def index():
    return render_template('index.html', usuarios=Usuario.query.all())


# Sign up page
@app.route('/signup')
def signup():
    return render_template('signup.html', title='Cadastro')


# New user
@app.route('/usuario/criar', methods=['POST'])
def criarusuario():
    usuario = Usuario(
        request.form.get('name'),
        request.form.get('email'),
        request.form.get('password')
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
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('name')
        usuario.email = request.form.get('email')
        usuario.senha = request.form.get('password')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editarusuario.html', usuario=usuario, title='Editar')


# Delete user
@app.route('/usuario/deletar/<int:id>')
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('index'))


# Sign in page
@app.route('/signin')
def signin():
    return render_template('signin.html', title='Entrar')


# Categories page
@app.route('/config/categorias')
def categorias():
    return render_template('categorias.html', title='Categorias', categorias=Categoria.query.all())


# New category
@app.route('/categorias/criar', methods=['POST'])
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
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categorias'))


# Products page
@app.route('/anuncios')
def anuncios():
    return render_template(
        'anuncios.html',
        title='Anuncios',
        anuncios=Anuncio.query.all(),
        categorias=Categoria.query.all()
    )


# New product
@app.route('/anuncios/criar', methods=['POST'])
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
def deletaranuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('anuncios'))


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
