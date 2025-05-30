from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'pet-carinho'
global LOGADO
LOGADO = 999
global HOJE
HOJE = date.today()

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
      'data_nascimento': '2000-09-19',
      'endereco': 'N/A',
      'cep': 'N/A',
      'telefone': 'N/A',
      'senha': 'Maria@1'
    },
    {'tipo': 2,
      'codigo': 2,
      'nome': 'Gustavo',
     'email': 'gustavo@vet.com',
      'data_nascimento': '1999-03-06',
      'endereco': 'N/A',
      'cep': 'N/A',
      'telefone': 'N/A',
      'senha': 'Gustavo@1'
    }
]
animais = [
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
agendamentos = []


@app.route('/')
def index():
    global LOGADO
    LOGADO = 999
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    global LOGADO
    try:
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            for usuario in usuarios:
                if usuario['email'] == email and usuario['senha'] == senha:
                    flash(f'Usuário {email} logado com sucesso!', 'sucesso')
                    if usuario['tipo'] == 0:
                        LOGADO = 0
                        return redirect('/dashboard')
                    elif usuario['tipo'] == 1:
                        LOGADO = 1
                        return redirect(url_for('pagina_usuario', codigo=usuario['codigo']))
                    elif usuario['tipo'] == 2:
                        LOGADO = 2
                        return redirect(url_for('pagina_veterinario', codigo=usuario['codigo']))
            else:
                flash('Nome e/ou senha incorretos. Tente novamente.', 'erro')
                return render_template('login.html')
        else:
            return render_template('login.html')
    except:
        flash(f'Um erro inesperado aconteceu', 'erro')
        return redirect('/login')

@app.route('/sair')
def sair():
    global LOGADO
    LOGADO = 999
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    try:
        global LOGADO
        LOGADO = 0
        tutores = []
        veterinarios = []
        animais_ativos = []

        for a in agendamentos:
            if a['datahora'] == HOJE:
                a['remarcavel'] = False

        print(agendamentos)

        for usuario in usuarios:
            if usuario['tipo'] == 1 and usuario['nome'] != "":
                animais_do_usuario = []
                for animal in animais:
                    if animal['tutor'] == usuario['codigo'] and animal['nome'] != '':
                        animais_do_usuario.append(animal['nome'])
                tutor = {
                    'nome': usuario['nome'],
                    'codigo': usuario['codigo'],
                    'animais': animais_do_usuario
                }
                tutores.append(tutor)

            elif usuario['tipo'] == 2 and usuario['nome'] != "":
                veterinarios.append(usuario)

        for animal in animais:
            if animal['nome'] != '':
                animais_ativos.append(animal)

        return render_template('dashboard.html', tutores=tutores, veterinarios=veterinarios, animais=animais_ativos, LOGADO=LOGADO, codigo=0, agendamentos=agendamentos)
    except:
        flash(f'Ocorreu um erro ao carregar o dashboard do administrador', 'erro')
        return redirect('/')

@app.route('/pagina_veterinario/<int:codigo>')
def pagina_veterinario(codigo):
    try:
        global LOGADO
        LOGADO = 2
        for u in usuarios:
            if u['codigo'] == codigo:
                usuario = u
        agendamentos_vet = []
        animais_vet = []
        for a in agendamentos:
            if a['datahora'] == HOJE:
                a['remarcavel'] = False
            if a['nomevet'] == codigo:
                agendamentos_vet.append(a)
            for an in animais:
                if a['codigopet'] == an['codigo']:
                    animais_vet.append(an)
        return render_template('pagina_veterinario.html', codigo=codigo, usuario=usuario, LOGADO=LOGADO, animais_vet=animais_vet, agendamentos_vet=agendamentos_vet)
    except:
        flash(f'Ocorreu um erro inesperado', 'erro')
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
            especiais = "!@#$%^&*()-_+=<>?/|\\{}[]"
            maiuscula = False
            minuscula = False
            especial = False
            numero = False
            for s in senha:
                if s.isupper():
                    maiuscula = True
                elif s.islower():
                    minuscula = True
                elif s.isdigit():
                    numero = True
                elif s in especiais:
                    especial = True
            if maiuscula == True and minuscula == True and numero == True and especial == True:
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
                flash('Utilize uma senha forte', 'erro')
                return render_template('cadastro_usuario.html', LOGADO=LOGADO)
        else:
            return render_template('cadastro_usuario.html', LOGADO=LOGADO)
    except:
        flash(f'Não foi possível criar esse usuário', 'erro')
        return render_template('cadastro_usuario.html', LOGADO=LOGADO)

@app.route('/edicao_usuario/<int:codigo>', methods=['GET', 'POST'])
def edicao_usuario(codigo):
    try:
        for u in usuarios:
            if u['codigo'] == codigo:
                usuario = u
                break

        if request.method == 'POST':
            senha = request.form.get('senha')
            especiais = "!@#$%^&*()-_+=<>?/|\\{}[]"
            maiuscula = False
            minuscula = False
            especial = False
            numero = False
            for s in senha:
                if s.isupper():
                    maiuscula = True
                elif s.islower():
                    minuscula = True
                elif s.isdigit():
                    numero = True
                elif s in especiais:
                    especial = True
            if maiuscula == True and minuscula == True and numero == True and especial == True:
                usuario['nome'] = request.form.get('nome')
                usuario['email'] = request.form.get('email')
                usuario['data_nascimento'] = request.form.get('data-nascimento')
                usuario['endereco'] = request.form.get('endereco')
                usuario['cep'] = request.form.get('cep')
                usuario['telefone'] = request.form.get('telefone')
                usuario['senha'] = request.form.get('senha')
                flash(f'Usuário {usuario["nome"]} editado com sucesso!', 'sucesso')
                if LOGADO == 0:
                    return redirect(url_for('dashboard'))
                elif LOGADO == 1:
                    return redirect(url_for('pagina_usuario', codigo=codigo))
                else:
                    return redirect('/')
            else:
                flash(f'Não foi possível editar esse usuário', 'erro')
                return render_template('edicao_usuario.html', usuario=usuario, LOGADO=LOGADO)
        return render_template('edicao_usuario.html', usuario=usuario, codigo=codigo, LOGADO=LOGADO)

    except:
        flash(f'Não foi possível editar esse usuário', 'erro')
        return render_template('edicao_usuario.html', usuario=usuario, LOGADO=LOGADO)

@app.route('/cadastro_animal/<int:codigo>', methods=['GET', 'POST'])
def cadastro_animal(codigo):
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            data_nascimento = request.form['data-nascimento']
            especie = request.form['especie']
            raca = request.form['raca']
            peso = float(request.form['peso'])
            sexo = request.form['sexo']
            codigoA = len(animais)
            animal = {
                'tutor': codigo,
                'codigo': codigoA,
                'nome': nome,
                'data_nascimento': data_nascimento,
                'especie': especie,
                'raca': raca,
                'peso': peso,
                'sexo': sexo
            }
            animais.append(animal)
            flash(f'Pet {nome} cadastrado com sucesso!', 'sucesso')
            if LOGADO == 0:
                return redirect(url_for('dashboard'))
            elif LOGADO == 1:
                return redirect(url_for('pagina_usuario', codigo=codigo))
            else:
                return redirect('/')
        else:
            if LOGADO == 1:
                usuario = usuarios[codigo]
            else:
                usuario = usuarios[0]
            tutores = []
            for u in usuarios:
                if u['tipo'] == 1:
                    tutores.append(u)
            return render_template('cadastro_animal.html', codigo=codigo, LOGADO=LOGADO, tutores=tutores, usuario=usuario)
    except:
        flash(f'Não foi possível cadastrar esse pet', 'erro')
        return redirect(url_for('pagina_usuario', codigo=codigo))

@app.route('/edicao_animal/<int:codigo>', methods=['POST', 'GET'])
def edicao_animal(codigo):
    try:
        for a in animais:
            if a['codigo'] == codigo:
                animal = a
                break
        if request.method == 'POST':
            animal['nome'] = request.form.get('nome')
            animal['data_nascimento'] = request.form.get('data_nascimento')
            animal['especie'] = request.form.get('especie')
            animal['raca'] = request.form.get('raca')
            animal['sexo'] = request.form.get('sexo')
            flash(f'Pet {animal["nome"]} editado com sucesso!', 'sucesso')
            if LOGADO == 0:
                return redirect(url_for('dashboard'))
            elif LOGADO == 1:
                return redirect(url_for('pagina_usuario', codigo=codigo))
            else:
                return redirect('/')
        return render_template('edicao_animal.html', animal=animal, codigo=codigo, LOGADO=LOGADO)
    except:
        flash(f'Ocorreu um erro inesperado', 'erro')
        return render_template('edicao_animal.html', animal=animal, codigo=codigo, LOGADO=LOGADO)

@app.route('/cadastro_veterinario', methods=['GET', 'POST'])
def cadastro_veterinario():
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            numero_registro = request.form['numeroderegistro']
            telefone = request.form['telefone']
            email = request.form['email']
            senha = request.form['senha']
            especiais = "!@#$%^&*()-_+=<>?/|\\{}[]"
            maiuscula = False
            minuscula = False
            especial = False
            numero = False
            for s in senha:
                if s.isupper():
                    maiuscula = True
                elif s.islower():
                    minuscula = True
                elif s.isdigit():
                    numero = True
                elif s in especiais:
                    especial = True
            if maiuscula == True and minuscula == True and numero == True and especial == True:
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
            return render_template('cadastro_veterinario.html', LOGADO=LOGADO)
    except:
        flash(f'Não foi possível cadastrar esse veterinário')
        return redirect('/dashboard')

@app.route('/edicao_veterinario/<int:codigo>', methods=['GET', 'POST'])
def edicao_veterinario(codigo):
    try:
        for u in usuarios:
            if u['codigo'] == codigo:
                usuario = u
                break

        if request.method == 'POST':
            senha = request.form.get('senha')
            especiais = "!@#$%^&*()-_+=<>?/|\\{}[]"
            maiuscula = False
            minuscula = False
            especial = False
            numero = False
            for s in senha:
                if s.isupper():
                    maiuscula = True
                elif s.islower():
                    minuscula = True
                elif s.isdigit():
                    numero = True
                elif s in especiais:
                    especial = True
            if maiuscula == True and minuscula == True and numero == True and especial == True:
                usuario['nome'] = request.form.get('nome')
                usuario['email'] = request.form.get('email')
                usuario['numero_registro'] = request.form.get('numeroderegistro')
                usuario['telefone'] = request.form.get('telefone')
                usuario['senha'] = request.form.get('senha')
                flash(f'Veterinário {usuario["nome"]} editado com sucesso!', 'sucesso')
                if LOGADO == 0:
                    return redirect(url_for('dashboard'))
                elif LOGADO == 1:
                    return redirect(url_for('pagina_usuario', codigo=codigo))
                else:
                    return redirect('/')
            else:
                flash(f'Não foi possível editar esse veterinário', 'erro')
                return render_template('edicao_veterinario.html', usuario=usuario, LOGADO=LOGADO)
        return render_template('edicao_veterinario.html', usuario=usuario, codigo=codigo, LOGADO=LOGADO)

    except:
        flash(f'Não foi possível editar esse veterinário', 'erro')
        return render_template('edicao_veterinario.html', usuario=usuario, LOGADO=LOGADO)

@app.route('/exclusao_veterinario/<int:codigo>', methods=['GET', 'POST'])
def exclusao_veterinario(codigo):
    try:
        usuario = ''
        for u in usuarios:
            if u['codigo'] == codigo:
                usuario = u
                break
        if request.method == 'POST':
            usuarios[codigo] = {
                'tipo': 2,
                'codigo': codigo,
                'nome': '',
                'numero_registro': '',
                'email': '',
                'telefone': '',
                'senha': ''
            }
            flash(f'Veterinário excluído com sucesso!', 'sucesso')
            return redirect(url_for('dashboard'))
        return render_template('exclusao_veterinario.html', codigo=codigo, usuario=usuario, LOGADO=LOGADO)
    except:
        flash(f'Ocorreu um erro inesperado', 'erro')
        return redirect('/dashboard')
@app.route('/pagina_usuario/<int:codigo>')
def pagina_usuario(codigo):
    try:
        global LOGADO
        LOGADO = 1
        for usuario in usuarios:
            if usuario['codigo'] == codigo:
                animais_do_usuario = []
                for animal in animais:
                    if animal['tutor'] == codigo:
                        animais_do_usuario.append(animal)
                agendamentos_usuario = []
                for a in agendamentos:
                    if a['nometutor'] == usuario['codigo']:
                        if a['datahora'] == HOJE:
                            a['remarcavel'] = False
                        agendamentos_usuario.append(a)
                return render_template('pagina_usuario.html', usuario=usuario, animais=animais_do_usuario, codigo=usuario['codigo'], LOGADO=LOGADO, agendamentos_usuario=agendamentos_usuario)
        flash("Usuário não encontrado", 'erro')
        return redirect('/')
    except:
        flash(f'Ocorreu um erro inesperado', 'erro')
        return redirect('/')

@app.route('/exclusao_usuario/<int:codigo>', methods=['GET', 'POST'])
def exclusao_usuario(codigo):
    try:
        if request.method == 'POST':
            usuarios[codigo] = {
                'codigo': codigo,
                'tipo': "1",
                'nome': "",
                'email': "",
                'data_nascimento': "",
                'endereco': "",
                'cep': "",
                'telefone': "",
                'senha': "",
            }

            for animal in animais:
                if animal['tutor'] == codigo:
                    animal = {
                        'nome': "",
                        'data_nascimento': "",
                        'especie': "",
                        'raca': "",
                        'peso': 0,
                        'sexo': ""
                    }
            flash(f'Usuário excluído com sucesso!', 'sucesso')
            return redirect('/dashboard')

        usuario = ""
        for u in usuarios:
            if u['codigo'] == codigo:
                usuario = u
                animais_usuario = []
                break

        for animal in animais:
            if animal['tutor'] == codigo:
                animais_usuario.append(animal)
        return render_template('exclusao_usuario.html', usuario=usuario, animais=animais_usuario, codigo=usuario['codigo'], LOGADO=LOGADO)
    except:
        flash('Ocorreu um erro inesperado', 'erro')
        return redirect('/dashboard')

@app.route('/exclusao_animal/<int:codigo>', methods=['GET', 'POST'])
def exclusao_animal(codigo):
    try:
        animal = ''
        for a in animais:
            if a['codigo'] == codigo:
                animal = a
                break
        if request.method == 'POST':
            animais[codigo] = {
                'tutor': animal['tutor'],
                'codigo': codigo,
                'nome': '',
                'data_nascimento': '',
                'especie': '',
                'raca': '',
                'peso': 0,
                'sexo': ''
            }
            flash(f'Pet excluído com sucesso!', 'sucesso')
            if LOGADO == 0:
                return redirect(url_for('dashboard'))
            elif LOGADO == 1:
                return redirect(url_for('pagina_usuario', codigo=codigo))
            else:
                return redirect('/')
        return render_template('exclusao_animal.html', codigo=codigo, LOGADO=LOGADO, animal=animal)
    except:
        flash(f'Ocorreu um erro inesperado', 'erro')
        if LOGADO == 0:
            return redirect(url_for('dashboard'))
        elif LOGADO == 1:
            return redirect(url_for('pagina_usuario', codigo=codigo))
        else:
            return redirect('/')
        
@app.route('/prontuario/<int:codigo_agendamento>', methods=['POST'])
def prontuario(codigo_agendamento):
    try:
        if request.method == 'POST':
            receita = request.form.get('receita')
            if receita == "Soro":
                return redirect(url_for('prontuariosoro', codigo_agendamento=codigo_agendamento))
            elif receita == "Medicamento":
                return redirect(url_for('prontuariodose', codigo_agendamento=codigo_agendamento))
            else:
                return redirect(url_for('prontuario'))
        else:
            return render_template(url_for('prontuario.html', codigo_agendamento=codigo_agendamento))
    except:
        flash(f'Ocorreu um erro inesperado', 'erro')
        if LOGADO == 0:
            return redirect(url_for('dashboard'))
        elif LOGADO == 1:
            return redirect(url_for('pagina_usuario', codigo=codigo))
        else:
            return redirect('/')
@app.route('/prontuariosoro')
def pontuario_soro():
    return render_template('prontuariosoro.html')

@app.route("/calcular", methods=["POST"])
def calcular():

        desidratacao = float(request.form["desidratacao"])
        peso = float(request.form["peso"])
        resultado = desidratacao * peso
        return render_template("prontuariosoro.html", resultado=resultado)

@app.route("/calcular_dose", methods=["POST"])
def calcular_dose():

        dose_recomendada = float(request.form["dose_recomendada"])
        peso = float(request.form["peso"])
        resultado_dose = dose_recomendada * peso
        return render_template("prontuariodose.html", resultado_dose=resultado_dose)


@app.route('/agendamento/<int:codigo>', methods=["GET", "POST"])
def agendamento(codigo):
    try:
        if request.method == 'POST':
            codigopet = int(request.form["codigopet"])
            telefone = request.form["telefone"]
            nomevet = int(request.form["nomevet"])
            datahora = request.form["datahora"]
            sintomas = request.form["sintomas"]
            consulta = len(agendamentos)

            animal = animais[codigopet]
            nomeanimal = animal['nome']
            veterinario = usuarios[nomevet]
            tutor = animal['tutor']

            datahora_obj = datetime.fromisoformat(datahora)
            dia_da_semana = datahora_obj.weekday()
            hora_agendada = datahora_obj.hour
            datahora_obj = datetime.fromisoformat(datahora)
            datahora_formatada = datahora_obj.strftime("%d/%m/%Y às %H:%M")

            for a in agendamentos:
                if a['codigopet'] == codigopet:
                    flash("Este pet já possui um agendamento", "erro")
                    return redirect(url_for('agendamento', codigo=codigo))
                elif a['datahora'] == datahora and a['nomevet'] == nomevet:
                    flash("Este horário não está disponível", "erro")
                    return redirect(url_for('agendamento', codigo=codigo))

            if dia_da_semana == 6:
                flash("Desculpe, estamos fechados no domingo.", "erro")
                return redirect(url_for('agendamento', codigo=codigo))

            if dia_da_semana == 5:
                if hora_agendada < 8 or hora_agendada >= 14:
                    flash("O horário para sábado é das 08:00 às 14:00.", "erro")
                    return redirect(url_for('agendamento', codigo=codigo))
            else:
                if hora_agendada < 8 or hora_agendada >= 18:
                    flash("O horário para segunda a sexta é das 08:00 às 18:00.", "erro")
                    return redirect(url_for('agendamento', codigo=codigo))

            agendamento = {
                'codigo': int(consulta),
                'codigopet': codigopet,
                'nomepet': nomeanimal,
                'nometutor': int(tutor),
                'telefone': telefone,
                'nomevet': veterinario['nome'],
                'datahora': datahora,
                'sintomas': sintomas,
                'remarcavel': True,
                'datahora_obj': datahora_obj,
                'datahora_formatada': datahora_formatada
            }
            agendamentos.append(agendamento)

            flash(f'Agendamento de {animal["nome"]} realizado com sucesso! Sua consulta será {datahora_formatada} com {veterinario["nome"]}.','sucesso')
            print(agendamentos)
            if LOGADO == 0:
                return redirect(url_for('dashboard'))
            elif LOGADO == 1:
                return redirect(url_for('pagina_usuario', codigo=codigo))
            else:
                return redirect('/')

        else:
            tutores = []
            veterinarios = []
            animais_usuario = []

            if LOGADO == 1:
                usuario = usuarios[codigo]
                for a in animais:
                    if a['tutor'] == usuario['codigo']:
                        animais_usuario.append(a)
            else:
                usuario = usuarios[0]

            for u in usuarios:
                if u['tipo'] == 1:
                    tutores.append(u)
                elif u['tipo'] == 2:
                    veterinarios.append(u)


            return render_template('agendamento.html', tutores=tutores, veterinarios=veterinarios, animais=animais, LOGADO=LOGADO, usuario=usuario, animais_usuario=animais_usuario)
    except:
            flash(f'Ocorreu um erro inesperado', 'erro')
            if LOGADO == 0:
                return redirect(url_for('dashboard'))
            elif LOGADO == 1:
                return redirect(url_for('pagina_usuario', codigo=codigo))
            else:
                return redirect('/')


@app.route('/reagendamento/<int:codigo_agendamento>', methods=['GET', 'POST'])
def reagendamento(codigo_agendamento):
    try:
        agendamento = ''
        for ag in agendamentos:
            if ag['codigo'] == codigo_agendamento:
                agendamento = ag
                break
        # print(f' lista de agendamentos -> {agendamentos}')

        # print(f' um agendamento ->  {agendamento}')

        codigo = agendamento['nometutor']

        # print(f'aqui e o codigo -> {codigo}')

        if request.method == 'POST':
            datahora = request.form["datahora"]
            codigopet = int(request.form["nomepet"])
            nomevet = int(request.form["nomevet"])

            datahora_obj = datetime.fromisoformat(datahora)
            dia_da_semana = datahora_obj.weekday()
            hora_agendada = datahora_obj.hour
            datahora_obj = datetime.fromisoformat(datahora)
            datahora_formatada = datahora_obj.strftime("%d/%m/%Y às %H:%M")

            for a in agendamentos:
                if a['datahora'] == datahora and a['nomevet'] == nomevet and a['codigo'] != codigo_agendamento:
                    flash("Este horário não está disponível", "erro")
                    return redirect(url_for('agendamento', codigo=codigo))

            if dia_da_semana == 6:
                flash("Desculpe, estamos fechados no domingo.", "erro")
                return redirect(url_for('agendamento', codigo=codigo))

            if dia_da_semana == 5:
                if hora_agendada < 8 or hora_agendada >= 14:
                    flash("O horário para sábado é das 08:00 às 14:00.", "erro")
                    return redirect(url_for('agendamento', codigo=codigo))
            else:
                if hora_agendada < 8 or hora_agendada >= 18:
                    flash("O horário para segunda a sexta é das 08:00 às 18:00.", "erro")
                    return redirect(url_for('agendamento', codigo=codigo))

            agendamento['codigopet'] = int(request.form["nomepet"])
            agendamento['telefone'] = request.form["telefone"]
            agendamento['nomevet'] = int(request.form["nomevet"])
            agendamento['datahora'] = request.form["datahora"]
            agendamento['sintomas'] = request.form["sintomas"]
            agendamento['datahora_formatada'] = datahora_formatada
            agendamento['datahora_obj'] = datahora_obj
            agendamento['datahora'] = datahora

            flash(f'Agendamento do dia {agendamento['datahora']} editado com sucesso!', 'sucesso')
            if LOGADO == 0:
                return redirect(url_for('dashboard'))
            elif LOGADO == 1:
                return redirect(url_for('pagina_usuario', codigo=codigo))
            else:
                return redirect('/')

            flash(f'Não foi possível editar esse agendamento', 'erro')
            return render_template('reagendamento.html', agendamento=agendamento, tutores=tutores,
                                   veterinarios=veterinarios, animais=animais, LOGADO=LOGADO, usuario=usuario,
                                   animais_usuario=animais_usuario)
        else:
            tutores = []
            veterinarios = []
            animais_usuario = []

            if LOGADO == 1:
                usuario = usuarios[codigo]
                for a in animais:
                    if a['tutor'] == usuario['codigo']:
                        animais_usuario.append(a)
            else:
                usuario = usuarios[0]

            for u in usuarios:
                if u['tipo'] == 1:
                    tutores.append(u)
                elif u['tipo'] == 2:
                    veterinarios.append(u)
            return render_template('reagendamento.html', agendamento=agendamento, tutores=tutores,
                                   veterinarios=veterinarios, animais=animais, LOGADO=LOGADO, usuario=usuario,
                                   animais_usuario=animais_usuario)

    except:
        flash(f'Ocorreu um erro inesperado', 'erro')
        if LOGADO == 0:
            return redirect(url_for('dashboard'))
        elif LOGADO == 1:
            return redirect(url_for('pagina_usuario', codigo=codigo))
        else:
            return redirect('/')

@app.route('/exclusao_agendamentos/<int:codigo_agendamento>', methods=['GET', 'POST'])
def exclusao_agendamentos(codigo_agendamento):
    try:
        agendamento = ''
        for ag in agendamentos:
            if ag['codigo'] == codigo_agendamento:
                agendamento = ag
                break
        # print(f' lista de agendamentos -> {agendamentos}')

        # print(f' um agendamento ->  {agendamento}')

        codigo = agendamento['nometutor']

        # print(f'aqui e o codigo -> {codigo}')

        if request.method == 'POST':
            agendamentos[codigo_agendamento] = {
                'codigo': agendamento['codigo'],
                'codigopet': '',
                'nomepet': '',
                'nometutor': '',
                'telefone': '',
                'nomevet': '',
                'datahora': '',
                'sintomas': '',
                'remarcavel': False,
                'datahora_obj': '',
                'datahora_formatada': ''
            }
            print(agendamentos)

            flash(f'Agendamento excluído com sucesso!', 'sucesso')
            if LOGADO == 0:
                return redirect(url_for('dashboard'))
            elif LOGADO == 1:
                return redirect(url_for('pagina_usuario', codigo=codigo))
            else:
                return redirect('/')

            flash(f'Não foi possível excluir esse agendamento', 'erro')
            return render_template('exclusao_agendamentos.html', agendamento=agendamento, codigo=codigo, LOGADO=LOGADO)
        return render_template('exclusao_agendamentos.html', agendamento=agendamento, codigo=codigo, LOGADO=LOGADO)


    except:
        flash(f'Ocorreu um erro inesperado', 'erro')
        if LOGADO == 0:
            return redirect(url_for('dashboard'))
        elif LOGADO == 1:
            return redirect(url_for('pagina_usuario', codigo=codigo))
        else:
            return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)