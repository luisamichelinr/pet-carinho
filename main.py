from flask import Flask, render_template, request, redirect, flash, url_for

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
      'senha': 'AuMiau'
      },
    {'tipo': 1,
      'codigo': 1,
      'nome': 'Maria',
      'data_nascimento': '19/09/2000',
      'endereco': 'N/A',
      'cep': 'N/A',
      'telefone': 'N/A',
      'senha': 'Maria@1'
    }
]
pacientes = [
    { 'tutor': 1,
      'codigo': 0,
      'nome': 'Kiara',
      'data_nascimento': '30/04/2021',
      'especie': 'cachorro',
      'raca': 'SRD',
      'peso': 7,
      'sexo': 'F'
    }
]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login',  methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            senha = request.form['senha']
            for usuario in usuarios:
                if usuario['nome'] == nome and usuario['senha'] == senha:
                    print(f"{usuario['nome']}")
                    if usuario['tipo'] == 0:
                        return redirect('/dashboard')
                    elif usuario['tipo'] == 1:
                        return redirect(url_for('pagina_usuario', codigo=usuario['codigo']))
                    elif usuario['tipo'] == 2:
                        return redirect('/perfil_veterinario')
            flash(f'Nome e/ou senha incorretos. Tente novamente.')
            return render_template('login.html')
        else:
            return render_template('login.html')
    except:
        flash(f'Um erro inesperado aconteceu. Tente novamente')
        return redirect('/login')

@app.route ('/dashboard')
def dashboard():
    tutores = []
    veterinarios = []

    for usuario in usuarios:
        if usuario['tipo'] == 1:
            pets_do_usuario = []
            for paciente in pacientes:
                if paciente['tutor'] == usuario['codigo']:
                    pets_do_usuario.append(paciente)
            tutor = {
                'nome': usuario['nome'],
                'pets': pets_do_usuario
            }
            tutores.append(tutor)

        elif usuario['tipo'] == 2:
            veterinarios.append(usuario)

    return render_template('dashboard.html', tutores=tutores, veterinarios=veterinarios, pacientes=pacientes)
@app.route('/perfil_veterinario')
def perfil_veterinario():
    return render_template('perfil_veterinario.html')

@app.route('/quem_somos')
def quem_somos():
    return render_template('index.html')

@app.route('/servicos')
def servicos():
    return render_template('index.html')

@app.route('/depoimentos')
def depoimentos():
    return render_template('index.html')

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

@app.route('/edicao_usuario/<int:codigo>', methods=['GET', 'POST'])
def edicao_usuario(codigo):
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
            flash(f'Usuário {nome} editado com sucesso!')
            return redirect('/login')
        else:
            flash(f'Não foi possível editar esse usuário. Tente novamente mais tarde.')
            return render_template('cadastro_usuario.html')
    except:
        flash(f'Não foi possível editar esse usuário. Tente novamente mais tarde.')
        return render_template('cadastro_usuario.html')

@app.route('/cadastro_animal<int:codigo>', methods=['GET', 'POST'])
def cadastro_animal(codigo):
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            data_nascimento = request.form['data-nascimento']
            especie = request.form['especie']
            raca = request.form['raca']
            peso = request.form['peso']
            sexo = request.form['sexo']
            codigoA = len(pacientes)
            paciente = {
                'tutor': codigo,
                'codigo': codigoA,
                'nome': nome,
                'data_nascimento': data_nascimento,
                'especie': especie,
                'raca' : raca,
                'peso': peso,
                'sexo': sexo
            }
            pacientes.append(paciente)
            flash(f'Pet {nome} cadastrado com sucesso!')
            return redirect('/pagina_usuario')
        else:
            flash(f'Não foi possível cadastrar esse pet. Tente novamente mais tarde.')
            return render_template('pagina_usuario.html')
    except:
        flash(f'Um erro inesperado aconteceu. Tente novamente mais tarde.')
        return render_template('cadastro_usuario.html')

@app.route('/pagina_usuario/<int:codigo>')
@app.route('/pagina_usuario/<int:codigo>')
def pagina_usuario(codigo):
    for usuario in usuarios:
        if usuario['codigo'] == codigo:
            pets_do_usuario = []
            for paciente in pacientes:
                if paciente['tutor'] == codigo:
                    pets_do_usuario.append(paciente)
            return render_template('pagina_usuario.html', usuario=usuario, pacientes=pets_do_usuario)
    flash("Usuário não encontrado.")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)