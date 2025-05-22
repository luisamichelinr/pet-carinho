from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = 'pet-carinho'

usuarios = []
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perfil_usuario')
def perfil_usuario():
    return render_template('perfil_usuario.html')

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento = request.form['data-nascimento']
        endereco = request.form['endereco']
        cep = request.form['cep']
        telefone = request.form['telefone']
        senha = request.form['senha']
        codigo = len(usuarios)
        usuario = {
            'nome': codigo,
            'data_nascimento': data_nascimento,
            'endereco': endereco,
            'cep' : cep,
            'telefone': telefone,
            'senha': senha
        }
        usuarios.append(usuario)
        flash(f'Usuário {nome} criado com sucesso!')
        return redirect('/perfil_usuario')
    else:
        return render_template('cadastro_usuario.html')

if __name__ == '__main__':
    app.run(debug=True)