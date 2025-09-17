from database import get_db_connection
from psycopg2.extras import RealDictCursor # Facilita o trabalho com os resultados como se fossem dicionários

class Usuario:
    # CORREÇÃO: O construtor agora aceita 'e_mail' para corresponder à coluna do banco de dados.
    def __init__(self, nome, sobrenome, e_mail, telefone, id_usuario=None, is_admin=False):
        self.id_usuario = id_usuario
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = e_mail  # O nome interno do atributo pode ser 'email'
        self.telefone = telefone
        self.is_admin = is_admin
    
    def salvar(self):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # A coluna no banco é 'e_mail'
                sql_query = """
                    INSERT INTO usuario (nome, sobrenome, e_mail, telefone)
                    VALUES (%s, %s, %s, %s) RETURNING id_usuario
                """
                cursor.execute(sql_query, (self.nome, self.sobrenome, self.email, self.telefone))
                user_id = cursor.fetchone()[0]
                conn.commit()
                cursor.close()
                conn.close()
                return user_id
            except Exception as e:
                print(f"Erro ao salvar usuário: {e}")
                if conn: conn.close()
                return None
        return None
    
    @staticmethod
    def buscar_por_email(email):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                # A busca é feita na coluna 'e_mail'
                cursor.execute("SELECT * FROM usuario WHERE e_mail = %s", (email,))
                user_data = cursor.fetchone()
                cursor.close()
                conn.close()
                if user_data:
                    # Retorna um objeto Usuario, que agora aceita 'e_mail'
                    return Usuario(**user_data)
                return None
            except Exception as e:
                print(f"Erro ao buscar usuário: {e}")
                if conn: conn.close()
                return None
        return None

class Pet:
    def __init__(self, nome, especie, raca, situacao, foto, data, sexo, 
                 descricao, mensagem_dono, nome_tutor, telefone_tutor, 
                 visto_em, id_usuario, id_pet=None):
        self.id_pet = id_pet
        self.nome = nome
        self.especie = especie
        self.raca = raca
        self.situacao = situacao
        self.foto = foto
        self.data = data
        self.sexo = sexo
        self.descricao = descricao
        self.mensagem_dono = mensagem_dono
        self.nome_tutor = nome_tutor
        self.telefone_tutor = telefone_tutor
        self.visto_em = visto_em
        self.id_usuario = id_usuario
    
    def salvar(self):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql_query = """
                    INSERT INTO pet (nome, especie, raca, situacao, foto, data, sexo, 
                                   descricao, mensagem_dono, nome_tutor, telefone_tutor, 
                                   visto_em, id_usuario)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_pet
                """
                params = (self.nome, self.especie, self.raca, self.situacao, self.foto, 
                          self.data, self.sexo, self.descricao,
                          self.mensagem_dono, self.nome_tutor, self.telefone_tutor, 
                          self.visto_em, self.id_usuario)
                cursor.execute(sql_query, params)
                pet_id = cursor.fetchone()[0]
                conn.commit()
                cursor.close()
                conn.close()
                return pet_id
            except Exception as e:
                print(f"Erro ao salvar pet: {e}")
                if conn: conn.close()
                return None
        return None
    
    @staticmethod
    def listar_todos():
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT p.*, u.nome AS nome_usuario
                    FROM pet p 
                    JOIN usuario u ON p.id_usuario = u.id_usuario
                    ORDER BY p.data DESC
                """)
                pets = cursor.fetchall()
                cursor.close()
                conn.close()
                return pets
            except Exception as e:
                print(f"Erro ao listar pets: {e}")
                if conn: conn.close()
                return []
        return []
    
    @staticmethod
    def buscar_por_id(pet_id):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT p.*, u.nome AS nome_usuario
                    FROM pet p 
                    JOIN usuario u ON p.id_usuario = u.id_usuario
                    WHERE p.id_pet = %s
                """, (pet_id,))
                pet = cursor.fetchone()
                cursor.close()
                conn.close()
                return pet
            except Exception as e:
                print(f"Erro ao buscar pet: {e}")
                if conn: conn.close()
                return None
        return None

    @staticmethod
    def deletar_por_id(pet_id):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM pet WHERE id_pet = %s", (pet_id,))
                conn.commit()
                cursor.close()
                conn.close()
                return True
            except Exception as e:
                print(f"Erro ao deletar pet: {e}")
                if conn: conn.close()
                return False
        return False

class Denuncia:
    def __init__(self, id_pet, id_usuario, motivo, id_denuncia=None, data_denuncia=None):
        self.id_denuncia = id_denuncia
        self.id_pet = id_pet
        self.id_usuario = id_usuario
        self.motivo = motivo
        self.data_denuncia = data_denuncia

    def salvar(self):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql_query = """
                    INSERT INTO denuncia (id_pet, id_usuario, motivo)
                    VALUES (%s, %s, %s) RETURNING id_denuncia
                """
                cursor.execute(sql_query, (self.id_pet, self.id_usuario, self.motivo))
                denuncia_id = cursor.fetchone()[0]
                conn.commit()
                cursor.close()
                conn.close()
                return denuncia_id
            except Exception as e:
                print(f"Erro ao salvar denúncia: {e}")
                if conn: conn.close()
                return None
        return None

    @staticmethod
    def listar_todas():
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                sql_query = """
                    SELECT 
                        d.id_denuncia, d.motivo, d.data_denuncia,
                        p.id_pet, p.nome AS pet_nome, p.foto,
                        u.id_usuario, u.e_mail AS usuario_email
                    FROM denuncia d
                    JOIN pet p ON d.id_pet = p.id_pet
                    JOIN usuario u ON d.id_usuario = u.id_usuario
                    ORDER BY d.data_denuncia DESC
                """
                cursor.execute(sql_query)
                denuncias = cursor.fetchall()
                cursor.close()
                conn.close()
                return denuncias
            except Exception as e:
                print(f"Erro ao listar denúncias: {e}")
                if conn: conn.close()
                return []
        return []