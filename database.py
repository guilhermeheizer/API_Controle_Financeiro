from sqlalchemy import create_engine # Para configurar a conexão com o banco de dados
from sqlalchemy.orm import sessionmaker, declarative_base # Para criar sessões de banco de dados
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) # Carregar as variáveis de ambiente do arquivo .env

# DATABASE_URL = "sqlite:///./financas.db" # URL de conexão com o banco de dados SQLite
db_url = os.environ["DATABASE_URL"] # URL de conexão com o banco de dados PostgreSQL, obtida a partir de uma variável de ambiente
print(f"Conectando ao banco de dados em: {db_url}")
 # Criar o engine de conexão com o banco de dados
engine = create_engine(db_url, 
                       pool_pre_ping=True
                       )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Criar uma classe de sessão local para interagir com o banco de dados
Base = declarative_base() # Criar a classe base para os modelos do banco de dados

# Função para obter uma sessão de banco de dados
def get_db():   
    db = SessionLocal() # Criar uma nova sessão de banco de dados
    try:
        yield db # Retornar a sessão para uso
    finally:
        db.close() # Fechar a sessão após o uso