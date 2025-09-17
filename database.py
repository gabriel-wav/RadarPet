import psycopg2
from config import Config

def get_db_connection():
    """Estabelece conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(Config.DB_CONNECTION_STRING)
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Erro ao conectar com o PostgreSQL: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None

def init_db():
    """Inicializa o banco de dados e cria/atualiza as tabelas necessárias."""
    print("🚀 Inicializando banco de dados PostgreSQL...")
    conn = get_db_connection()
    if not conn:
        print("❌ Abortando: Não foi possível conectar ao banco de dados.")
        return False
        
    try:
        cursor = conn.cursor()
        
        print("📝 Verificando e criando tabela 'usuario'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario      INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                nome            VARCHAR(255) NOT NULL,
                sobrenome       VARCHAR(255) NOT NULL,
                e_mail          VARCHAR(100) NOT NULL UNIQUE,
                telefone        VARCHAR(20) NOT NULL,
                is_admin        BOOLEAN DEFAULT FALSE
            );
        """)

        # Adiciona a coluna is_admin se ela não existir (para bancos de dados antigos)
        cursor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='usuario' AND column_name='is_admin') THEN
                    ALTER TABLE usuario ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;
                END IF;
            END$$;
        """)
        
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
                FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario) ON DELETE CASCADE
            );
        """)
        
        print("📝 Verificando e criando tabela 'denuncia'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS denuncia (
                id_denuncia     INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                id_pet          INTEGER NOT NULL REFERENCES pet(id_pet) ON DELETE CASCADE,
                id_usuario      INTEGER NOT NULL REFERENCES usuario(id_usuario) ON DELETE CASCADE,
                motivo          TEXT NOT NULL,
                data_denuncia   TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
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
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    init_db()