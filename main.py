from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = 'pet-carinho'

usuarios = [
    { 'tipo': 0,
      'codigo': 0,
      'nome': 'adm_vet',
      'data_nascimento': '--/--/----',
      'endereco': 'N/A',
      'cep': 'N/A',
      'telefone': 'N/A',
      'senha': 'AuAuMiauMiau'
      }
]
pacientes = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/perfil_usuario')
def perfil_usuario():
    return render_template('perfil_usuario.html')

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            data_nascimento = request.form['data-nascimento']
            endereco = request.form['endereco']
            cep = request.form['cep']
            telefone = request.form['telefone']
            senha = request.form['senha']
            codigo = len(usuarios)
            usuario = {
                'tipo': 1,
                'codigo': codigo,
                'nome': nome,
                'data_nascimento': data_nascimento,
                'endereco': endereco,
                'cep' : cep,
                'telefone': telefone,
                'senha': senha
            }
            usuarios.append(usuario)
            flash(f'Usuário {nome} criado com sucesso!')
            return redirect('/login')
        else:
            flash(f'Não foi possível criar esse usuário. Tente novamente mais tarde.')
            return render_template('cadastro_usuario.html')
    except:
        flash(f'Não foi possível criar esse usuário. Tente novamente mais tarde.')
        return render_template('cadastro_usuario.html')

if __name__ == '__main__':
    app.run(debug=True)