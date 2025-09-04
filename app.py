from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
from werkzeug.utils import secure_filename
from database import init_db
from models import Usuario, Pet
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # IMPORTANTE: mude isso em produção

# Configurações de upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Criar pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Inicializar banco - CORRIGIDO para Flask versões mais recentes
@app.before_request
def before_first_request():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

# ==========================================
# ROTAS
# ==========================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        telefone = request.form['telefone']
        
        # Verificar se email já existe
        if Usuario.buscar_por_email(email):
            flash('Email já cadastrado!', 'error')
            return render_template('cadastro.html')
        
        # Criar novo usuário
        usuario = Usuario(nome, sobrenome, email, telefone)
        user_id = usuario.salvar()
        
        if user_id:
            session['user_id'] = user_id
            session['user_name'] = nome
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Erro ao cadastrar usuário!', 'error')
    
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        
        user = Usuario.buscar_por_email(email)
        if user:
            session['user_id'] = user[0]  # id_usuario
            session['user_name'] = user[1]  # nome
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email não encontrado!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/anunciar', methods=['GET', 'POST'])
def anunciar():
    if 'user_id' not in session:
        flash('Você precisa estar logado para anunciar um pet!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Processar upload de arquivo
        foto_filename = None
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Adicionar timestamp para evitar conflitos
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                foto_filename = filename
        
        # Criar objeto Pet
        pet = Pet(
            nome=request.form['nome_pet'],
            especie=request.form['especie'],
            raca=request.form.get('raca', ''),
            situacao=request.form['situacao'],
            foto=foto_filename,
            data=request.form['data'],
            sexo=request.form['sexo'],
            # REMOVIDO: cidade e bairro
            descricao=request.form['descricao'],
            mensagem_dono=request.form.get('mensagem_dono', ''),
            nome_tutor=request.form['nome_tutor'],
            telefone_tutor=request.form['telefone_tutor'],
            visto_em=request.form['visto_em'],
            id_usuario=session['user_id']
        )
        
        pet_id = pet.salvar()
        if pet_id:
            flash('Pet anunciado com sucesso!', 'success')
            return redirect(url_for('pet_perdido'))
        else:
            flash('Erro ao anunciar pet!', 'error')
    
    return render_template('anunciar.html')

@app.route('/pet-perdido')
def pet_perdido():
    return render_template('pet-perdido.html')

@app.route('/api/pets')
def api_pets():
    pets = Pet.listar_todos()
    pets_json = []
    
    for pet in pets:
        # ATENÇÃO: Os índices da tupla 'pet' mudaram!
        pets_json.append({
            'id': pet[0],
            'nome': pet[1],
            'especie': pet[2],
            'raca': pet[3],
            'situacao': pet[4],
            'foto': pet[5] if pet[5] else 'default-pet.jpg',
            'data': pet[6].strftime('%d/%m/%Y') if pet[6] else '',
            'sexo': pet[7],
            # cidade (era 8) e bairro (era 9) foram removidos
            'descricao': pet[8],      # <-- era 10
            'mensagem_dono': pet[9],  # <-- era 11
            'nome_tutor': pet[10],     # <-- era 12
            'telefone_tutor': pet[11], # <-- era 13
            'visto_em': pet[12],       # <-- era 14
            'nome_usuario': pet[14] if len(pet) > 14 else '' # <-- era 16
        })
    
    return jsonify(pets_json)

@app.route('/verpet/<int:pet_id>')
def ver_pet(pet_id):
    pet = Pet.buscar_por_id(pet_id)
    if not pet:
        flash('Pet não encontrado!', 'error')
        return redirect(url_for('pet_perdido'))
    
    return render_template('verpet.html', pet=pet)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)