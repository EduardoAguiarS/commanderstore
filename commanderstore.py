from flask import Flask, make_response, render_template, request, send_from_directory

app = Flask(__name__)

# link to css
@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Sign up page
@app.route('/signup')
def signup():
    return render_template('signup.html', title='Cadastro')

# Sign up success page
@app.route('/signupsuccess', methods=['POST'])
def signupsuccess():
    return request.form

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