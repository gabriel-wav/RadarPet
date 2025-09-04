import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class Config:
    # --- Configurações do PostgreSQL ---
    # Para o Render, esta será uma única variável de ambiente chamada DATABASE_URL.
    # Para desenvolvimento local, usaremos as variáveis individuais.
    
    DB_URL = os.getenv('DATABASE_URL')
    if DB_URL:
        # Se estiver em produção (Render), usa a URL de conexão completa
        DB_CONNECTION_STRING = DB_URL
    else:
        # Para desenvolvimento local, constrói a string a partir das partes
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'sua_senha_local')
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '5432')
        DB_DATABASE = os.getenv('DB_DATABASE', 'radar_pet')
        
        DB_CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"