import psycopg2
from config import Config

def get_db_connection():
    """Estabelece conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(Config.DB_CONNECTION_STRING)
        print("✅ Conexão com PostgreSQL estabelecida com sucesso!")
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Erro ao conectar com o PostgreSQL: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None

def init_db():
    """Inicializa o banco de dados e cria as tabelas se não existirem."""
    print("🚀 Inicializando banco de dados PostgreSQL...")
    conn = get_db_connection()
    if not conn:
        print("❌ Abortando: Não foi possível conectar ao banco de dados.")
        return False
        
    try:
        cursor = conn.cursor()
        
        # --- Criar Tabela 'usuario' ---
        print("📝 Verificando e criando tabela 'usuario'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario      INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                nome            VARCHAR(255) NOT NULL,
                sobrenome       VARCHAR(255) NOT NULL,
                e_mail          VARCHAR(100) NOT NULL UNIQUE,
                telefone        VARCHAR(20) NOT NULL
            );
        """)
        
        # --- Criar Tabela 'pet' ---
        print("📝 Verificando e criando tabela 'pet'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pet (
                id_pet              INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                nome                VARCHAR(100) NOT NULL,
                especie             VARCHAR(30) NOT NULL CHECK (especie IN ('Cachorro', 'Gato', 'Outros')),
                raca                VARCHAR(100) NULL,
                situacao            VARCHAR(15) NOT NULL CHECK (situacao IN ('Achado', 'Perdido')),
                foto                VARCHAR(255) NULL,
                data                DATE NOT NULL,
                sexo                VARCHAR(15) NOT NULL CHECK (sexo IN ('Macho', 'Fêmea')),
                descricao           TEXT NOT NULL,
                mensagem_dono       TEXT NULL,
                nome_tutor          VARCHAR(255) NOT NULL,
                telefone_tutor      VARCHAR(20) NOT NULL,
                visto_em            VARCHAR(255) NOT NULL,
                id_usuario          INTEGER NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
            );
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Banco de dados inicializado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar tabelas: {e}")
        if conn:
            conn.rollback() # Desfaz a transação em caso de erro
            conn.close()
        return False

if __name__ == "__main__":
    print("🧪 Executando inicialização do banco de dados a partir do script...")
    init_db()