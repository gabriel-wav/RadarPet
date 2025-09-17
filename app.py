from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
from werkzeug.utils import secure_filename
from database import init_db
from models import Usuario, Pet, Denuncia # IMPORTANTE: Adicionar a importação de Denuncia
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # IMPORTANTE: mude isso em produção

# Configurações de upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Criar pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================================
# DECORATORS DE AUTENTICAÇÃO
# ==========================================

# Um decorator é um padrão de projeto profissional para proteger rotas.
# Esta função irá verificar se um usuário é administrador antes de permitir o acesso.
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Acesso restrito a administradores.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==========================================
# INICIALIZAÇÃO DO BANCO
# ==========================================

@app.before_request
def before_first_request():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

# ==========================================
# ROTAS PÚBLICAS E DE USUÁRIO
# ==========================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    # ... (código existente sem alterações) ...
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        telefone = request.form['telefone']
        
        if Usuario.buscar_por_email(email):
            flash('Email já cadastrado!', 'error')
            return render_template('cadastro.html')
        
        usuario = Usuario(nome, sobrenome, email, telefone)
        user_id = usuario.salvar()
        
        if user_id:
            user_data = Usuario.buscar_por_email(email)
            session['user_id'] = user_data.id_usuario
            session['user_name'] = user_data.nome
            session['is_admin'] = user_data.is_admin # Armazena o status de admin na sessão
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
            # ATENÇÃO: Agora 'user' é um objeto, não uma tupla
            session['user_id'] = user.id_usuario
            session['user_name'] = user.nome
            # IMPORTANTE: Armazenar o status de admin na sessão no momento do login
            session['is_admin'] = user.is_admin
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email ou senha inválidos!', 'error') # Mensagem mais genérica por segurança
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/anunciar', methods=['GET', 'POST'])
def anunciar():
    # ... (código existente sem alterações) ...
    if 'user_id' not in session:
        flash('Você precisa estar logado para anunciar um pet!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        foto_filename = None
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                foto_filename = filename
        
        pet = Pet(
            nome=request.form['nome_pet'], especie=request.form['especie'],
            raca=request.form.get('raca', ''), situacao=request.form['situacao'],
            foto=foto_filename, data=request.form['data'], sexo=request.form['sexo'],
            descricao=request.form['descricao'], mensagem_dono=request.form.get('mensagem_dono', ''),
            nome_tutor=request.form['nome_tutor'], telefone_tutor=request.form['telefone_tutor'],
            visto_em=request.form['visto_em'], id_usuario=session['user_id']
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
        # CORREÇÃO: Acessando dados como um dicionário ('pet['chave']')
        # em vez de uma tupla ('pet[indice]').
        pets_json.append({
            'id': pet['id_pet'],
            'nome': pet['nome'],
            'especie': pet['especie'],
            'raca': pet['raca'],
            'situacao': pet['situacao'],
            'foto': pet['foto'] if pet['foto'] else 'default-pet.jpg',
            'data': pet['data'].strftime('%d/%m/%Y') if pet['data'] else '',
            'sexo': pet['sexo'],
            'descricao': pet['descricao'],
            'mensagem_dono': pet['mensagem_dono'],
            'nome_tutor': pet['nome_tutor'],
            'telefone_tutor': pet['telefone_tutor'],
            'visto_em': pet['visto_em'],
            'nome_usuario': pet['nome_usuario'] if 'nome_usuario' in pet else ''
        })
    
    return jsonify(pets_json)

@app.route('/verpet/<int:pet_id>')
def ver_pet(pet_id):
    pet = Pet.buscar_por_id(pet_id)
    if not pet:
        flash('Pet não encontrado!', 'error')
        return redirect(url_for('pet_perdido'))
    
    return render_template('verpet.html', pet=pet)

# ==========================================
# NOVAS ROTAS DE MODERAÇÃO
# ==========================================

@app.route('/denunciar/<int:pet_id>', methods=['GET', 'POST'])
def denunciar(pet_id):
    if 'user_id' not in session:
        flash('Você precisa estar logado para denunciar um anúncio.', 'error')
        return redirect(url_for('login'))

    pet = Pet.buscar_por_id(pet_id)
    if not pet:
        flash('Anúncio não encontrado.', 'error')
        return redirect(url_for('pet_perdido'))

    if request.method == 'POST':
        motivo = request.form.get('motivo')
        if not motivo:
            flash('O motivo da denúncia é obrigatório.', 'error')
            return render_template('denuncia.html', pet=pet)
        
        nova_denuncia = Denuncia(
            id_pet=pet_id, 
            id_usuario=session['user_id'], 
            motivo=motivo
        )
        denuncia_id = nova_denuncia.salvar()
        
        if denuncia_id:
            flash('Sua denúncia foi enviada com sucesso e será analisada.', 'success')
        else:
            flash('Ocorreu um erro ao enviar sua denúncia.', 'error')
        return redirect(url_for('pet_perdido'))

    return render_template('denuncia.html', pet=pet)

@app.route('/admin')
@admin_required # Protege a rota usando nosso decorator
def admin_panel():
    # Busca todas as denúncias com informações do pet e do usuário denunciante
    denuncias = Denuncia.listar_todas() 
    return render_template('admin.html', denuncias=denuncias)

# @app.route('/admin/deletar_pet/<int:pet_id>', methods=['POST'])
# @admin_required # Protege a rota
# def deletar_pet(pet_id):
#     pet = Pet.buscar_por_id(pet_id)
#     if pet and pet.foto:
#         try:
#             # Deleta o arquivo da imagem do servidor
#             os.remove(os.path.join(app.config['UPLOAD_FOLDER'], pet.foto))
#         except OSError as e:
#             # Se o arquivo não for encontrado, apenas loga o erro, não impede a operação
#             print(f"Erro ao deletar arquivo de imagem: {e}")
    
#     # Deleta o pet e suas denúncias (se configurado com ON DELETE CASCADE)
#     if Pet.deletar_por_id(pet_id):
#         flash(f'Anúncio do pet ID {pet_id} deletado com sucesso.', 'success')
#     else:
#         flash(f'Erro ao deletar anúncio do pet ID {pet_id}.', 'error')
        
#     return redirect(url_for('admin_panel'))

@app.route('/admin/deletar_pet/<int:pet_id>', methods=['POST'])
@admin_required # Protege a rota
def deletar_pet(pet_id):
    # buscar_por_id retorna um objeto RealDictRow (parecido com dicionário)
    pet = Pet.buscar_por_id(pet_id)
    
    # CORREÇÃO: Acessar o campo 'foto' usando a sintaxe de dicionário ['foto']
    if pet and pet['foto']:
        try:
            # Deleta o arquivo da imagem do servidor
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], pet['foto']))
        except OSError as e:
            # Se o arquivo não for encontrado, apenas loga o erro, não impede a operação
            print(f"Erro ao deletar arquivo de imagem: {e}")
    
    # Deleta o pet e suas denúncias (configurado com ON DELETE CASCADE no banco)
    if Pet.deletar_por_id(pet_id):
        flash(f'Anúncio do pet ID {pet_id} deletado com sucesso.', 'success')
    else:
        flash(f'Erro ao deletar anúncio do pet ID {pet_id}.', 'error')
        
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)