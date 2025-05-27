from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)
app.secret_key = 'pet-carinho'

usuarios = [
    { 'tipo': 0,
      'codigo': 0,
      'nome': 'adm_vet',
      'email': 'adm@vet.com',
      'data_nascimento': '--/--/----',
      'endereco': 'N/A',
      'cep': 'N/A',
      'telefone': 'N/A',
      'senha': 'AuMiau'
      },
    {'tipo': 1,
      'codigo': 1,
      'nome': 'Maria',
     'email': 'maria@gmail.com',
      'data_nascimento': '19/09/2000',
      'endereco': 'N/A',
      'cep': 'N/A',
      'telefone': 'N/A',
      'senha': 'Maria@1'
    },
    {'tipo': 2,
      'codigo': 2,
      'nome': 'Gustavo',
     'email': 'gustavo@vet.com',
      'data_nascimento': '05/12/1999',
      'endereco': 'N/A',
      'cep': 'N/A',
      'telefone': 'N/A',
      'senha': 'Gustavo@1'
    }
]
pacientes = [
    { 'tutor': 1,
      'codigo': 0,
      'nome': 'Kiara',
      'data_nascimento': '2021-04-30',
      'especie': 'cachorro',
      'raca': 'SRD',
      'peso': 7.0,
      'sexo': 'F'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            for usuario in usuarios:
                if usuario['email'] == email and usuario['senha'] == senha:
                    flash(f'Usuário {email} logado com sucesso!', 'sucesso')
                    if usuario['tipo'] == 0:
                        return redirect('/dashboard')
                    elif usuario['tipo'] == 1:
                        return redirect(url_for('pagina_usuario', codigo=usuario['codigo']))
                    elif usuario['tipo'] == 2:
                        return redirect('/perfil_veterinario')
            else:
                flash('Nome e/ou senha incorretos. Tente novamente.', 'erro')
                return render_template('login.html')
        else:
            return render_template('login.html')
    except:
        flash(f'Um erro inesperado aconteceu', 'erro')
        return redirect('/login')

@app.route('/dashboard')
def dashboard():
    try:
        tutores = []
        veterinarios = []

        for usuario in usuarios:
            if usuario['tipo'] == 1:
                pets_do_usuario = []
                for paciente in pacientes:
                    if paciente['tutor'] == usuario['codigo']:
                        pets_do_usuario.append(paciente['nome'])
                tutor = {
                    'nome': usuario['nome'],
                    'codigo': usuario['codigo'],
                    'pets': pets_do_usuario
                }
                tutores.append(tutor)

            elif usuario['tipo'] == 2:
                veterinarios.append(usuario)

        return render_template('dashboard.html', tutores=tutores, veterinarios=veterinarios, pacientes=pacientes)
    except:
        flash(f'Ocorreu um erro ao carregar o dashboard do administrador')
        return redirect('/')

@app.route('/perfil_veterinario')
def perfil_veterinario():
    try:
        return render_template('perfil_veterinario.html')
    except:
        flash(f'Ocorreu um erro insperado')
        return redirect('/')

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    try:
        if request.method == 'POST':
            nome = request.form.get('nome')
            email = request.form.get('email')
            data_nascimento = request.form.get('data-nascimento')
            endereco = request.form.get('endereco')
            cep = request.form.get('cep')
            telefone = request.form.get('telefone')
            senha = request.form.get('senha')
            if not (nome and email and senha):
                flash('Nome, email e senha são obrigatórios.', 'erro')
                return render_template('cadastro_usuario.html')
            codigo = len(usuarios)
            usuario = {
                'tipo': 1,
                'codigo': codigo,
                'nome': nome,
                'email': email,
                'data_nascimento': data_nascimento,
                'endereco': endereco,
                'cep': cep,
                'telefone': telefone,
                'senha': senha
            }
            usuarios.append(usuario)
            flash(f'Usuário {nome} criado com sucesso!', 'sucesso')
            return redirect('/login')
        else:
            return render_template('cadastro_usuario.html')
    except:
        flash(f'Não foi possível criar esse usuário', 'erro')
        return render_template('cadastro_usuario.html')

@app.route('/edicao_usuario/<int:codigo>', methods=['GET', 'POST'])
def edicao_usuario(codigo):
    try:
        usuario = None
        for u in usuarios:
            if u['codigo'] == codigo:
                usuario = u
                break
        if usuario is None:
            flash('Usuário não encontrado.', 'erro')
            return redirect('/dashboard')

        if request.method == 'POST':
            usuario['nome'] = request.form.get('nome')
            usuario['email'] = request.form.get('email')
            usuario['data_nascimento'] = request.form.get('data-nascimento')
            usuario['endereco'] = request.form.get('endereco')
            usuario['cep'] = request.form.get('cep')
            usuario['telefone'] = request.form.get('telefone')
            usuario['senha'] = request.form.get('senha')

            flash(f'Usuário {usuario["nome"]} editado com sucesso!', 'sucesso')
            return redirect(url_for('pagina_usuario', codigo=codigo))
        return render_template('edicao_usuario.html', usuario=usuario)

    except:
        flash(f'Não foi possível editar esse usuário', 'erro')
        return render_template('edicao_usuario.html', usuario=usuario if usuario else None)

@app.route('/cadastro_animal/<int:codigo>', methods=['GET', 'POST'])
def cadastro_animal(codigo):
    try:
        if request.method == 'POST':
            print("Dados recebidos:", request.form)
            nome = request.form['nome']
            data_nascimento = request.form['data-nascimento']
            especie = request.form['especie']
            raca = request.form['raca']
            peso = float(request.form['peso'])
            sexo = request.form['sexo']
            codigoA = len(pacientes)
            paciente = {
                'tutor': codigo,
                'codigo': codigoA,
                'nome': nome,
                'data_nascimento': data_nascimento,
                'especie': especie,
                'raca': raca,
                'peso': peso,
                'sexo': sexo
            }
            pacientes.append(paciente)
            flash(f'Pet {nome} cadastrado com sucesso!', 'sucesso')
            return redirect(url_for('pagina_usuario', codigo=codigo))
        else:
            return render_template('cadastro_animal.html', codigo=codigo)
    except:
        flash(f'Não foi possível cadastrar esse pet', 'erro')
        return redirect(url_for('pagina_usuario', codigo=codigo))

@app.route('/cadastro_veterinario', methods=['GET', 'POST'])
def cadastro_veterinario():
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            numero_registro = request.form['numeroderegistro']
            telefone = request.form['telefone']
            email = request.form['email']
            senha = request.form['senha']
            codigo = len(usuarios)
            usuario = {
                'tipo': 2,
                'codigo': codigo,
                'nome': nome,
                'numero_registro': numero_registro,
                'email': email,
                'telefone': telefone,
                'senha': senha
            }
            usuarios.append(usuario)
            flash(f'Veterinário {nome} cadastrado com sucesso!')
            return redirect('/dashboard')
        else:
            return render_template('cadastro_veterinario.html')
    except:
        flash(f'Não foi possível cadastrar esse veterinário')
        return redirect('/dashboard')

@app.route('/edicao_veterinario/<int:codigo>', methods=['GET', 'POST'])
def edicao_veterinario(codigo):
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            numero_registro = request.form['numeroderegistro']
            telefone = request.form['telefone']
            email = request.form['email']
            senha = request.form['senha']
            codigo = len(usuarios)
            usuario = {
                'tipo': 2,
                'codigo': codigo,
                'nome': nome,
                'numero_registro': numero_registro,
                'email': email,
                'telefone': telefone,
                'senha': senha
            }
            usuarios.append(usuario)
            flash(f'Veterinário {nome} editado com sucesso!')
            return redirect('/dashboard')
        else:
            flash(f'Não foi possível editar esse usuário. Tente novamente mais tarde.')
            return render_template('cadastro_usuario.html')
    except:
        flash(f'Não foi possível editar esse veterinário')
        return redirect('/dashboard')

@app.route('/pagina_usuario/<int:codigo>')
def pagina_usuario(codigo):
    try:
        for usuario in usuarios:
            if usuario['codigo'] == codigo:
                pets_do_usuario = []
                for paciente in pacientes:
                    if paciente['tutor'] == codigo:
                        pets_do_usuario.append(paciente)
                return render_template('pagina_usuario.html', usuario=usuario, pacientes=pets_do_usuario, codigo=usuario['codigo'])
        flash("Usuário não encontrado.")
        return redirect('/')
    except:
        flash(f'Ocorreu um erro inesperado')
        return redirect('/')

@app.route('/excluir_usuario/<int:codigo>')
def excluir_usuario(codigo):
        usuarios[codigo] = {
            'nome': ""
        }
        flash(f'Usuário excluído com sucesso!')
        return redirect('/dashboard')

@app.route('/excluir_pet/<int:codigo>')
def excluir_pet(codigo):
        pacientes[codigo] = {
            'nome': ""
        }
        flash(f'Pet excluído com sucesso!')
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)