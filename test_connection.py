from database import get_db_connection

def test_connection():
    conn = get_db_connection()
    if conn:
        print("✅ Conexão com banco estabelecida!")
        cursor = conn.cursor()
        cursor.execute("SELECT @@version")
        version = cursor.fetchone()
        print(f"Versão SQL Server: {version[0]}")
        conn.close()
    else:
        print("❌ Erro na conexão com banco")

if __name__ == "__main__":
    test_connection()