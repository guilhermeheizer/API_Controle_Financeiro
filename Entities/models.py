from database import Base # Importar a classe Base do módulo database
from sqlalchemy.orm import Mapped, mapped_column, relationship # Importar os tipos de dados para as colunas do banco de dados
from sqlalchemy import Integer, String, ForeignKey, Numeric, DateTime, Boolean, text, func, CheckConstraint, Identity # Importar os tipos de dados para as colunas do banco de dados
from decimal import Decimal
from datetime import datetime


class TipoCategoria(Base): # Definir a classe TipoCategoria que herda de Base
    __tablename__ = "TipoCategoria" # Nome da tabela no banco de dados

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, index=True) # Coluna id como chave primária
    Descricao: Mapped[str] = mapped_column(String(50), unique=True, nullable=False) # Coluna descricao para o tipo de categoria

    Categorias = relationship("Categoria", back_populates="TipoCategoria") # Relacionamento com a classe Categoria

class Categoria(Base): # Definir a classe Categoria que herda de Base
    __tablename__ = "Categoria" # Nome da tabela no banco de dados

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, index=True) # Coluna id como chave primária, a partir a versão 2.0 do sqlalchemy, o autoincrement é True por padrão para colunas inteiras que são chaves primárias
    IdTipoCategoria: Mapped[int] = mapped_column(Integer, ForeignKey("TipoCategoria.id"), nullable=False) # Coluna para armazenar o id do tipo de categoria
    Descricao: Mapped[str] = mapped_column(String(50), unique=True, nullable=False) # Coluna descricao para a categoria
    Excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false")) # Coluna para indicar se a categoria está excluída
    IdUsuario: Mapped[int] = mapped_column(Integer, ForeignKey("Usuario.Id"), nullable=False) # Coluna para armazenar o id do usuário que criou a categoria
    
    Usuario = relationship("Usuario", back_populates="Categorias") # Relacionamento com a classe Usuario
    TipoCategoria = relationship("TipoCategoria", back_populates="Categorias") # Relacionamento com a classe TipoCategoria
    Despesas = relationship("Despesa", back_populates="Categoria") # Relacionamento com a classe Despesa
    Transacoes = relationship("Transacao", back_populates="Categoria") # Relacionamento com a classe Transacao

class Transacao(Base): # Definir a classe Transacao que herda de Base
    __tablename__ = "Transacao" # Nome da tabela no banco de dados

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, index=True) # Coluna id como chave primária
    IdCategoria: Mapped[int | None] = mapped_column(Integer, ForeignKey("Categoria.id"), nullable=True) # Coluna para armazenar o id da categoria
    IdDespesa: Mapped[int | None] = mapped_column(Integer, ForeignKey("Despesa.id"), nullable=True) # Coluna para armazenar o id da despesa
    Descricao: Mapped[str] = mapped_column(String(150), nullable=False) # Coluna para armazenar a descrição da transação
    Valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False) # Coluna para armazenar o valor da transação
    Data: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now()) # Coluna para armazenar a data da transação
    IdUsuario: Mapped[int] = mapped_column(Integer, ForeignKey("Usuario.Id"), nullable=False) # Coluna para armazenar o id do usuário que criou a transação
    
    Usuario = relationship("Usuario", back_populates="Transacoes") # Relacionamento com a classe Usuario
    Categoria = relationship("Categoria", back_populates="Transacoes") # Relacionamento com a classe Categoria
    Despesa = relationship("Despesa", back_populates="Transacoes") # Relacionamento com a classe Despesa
    Usuario = relationship("Usuario", back_populates="Transacoes") # Relacionamento com a classe Usuario
    Excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false")) # Coluna para indicar se a transação está excluída

    __table_args__ = (
        CheckConstraint(
            '"IdCategoria" IS NOT NULL OR "IdDespesa" IS NOT NULL',
            name="ck_at_least_one"
        ),
        CheckConstraint(
            'NOT ("IdCategoria" IS NOT NULL AND "IdDespesa" IS NOT NULL)',
            name="ck_at_most_one"
        )
    )

class Despesa(Base): # Definir a classe Despesa que herda de Base
    __tablename__ = "Despesa" # Nome da tabela no banco de dados

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, index=True) # Coluna id como chave primária
    IdCategoria: Mapped[int] = mapped_column(Integer, ForeignKey("Categoria.id"), nullable=False) # Coluna para armazenar o id da categoria
    Descricao: Mapped[str] = mapped_column(String(150), nullable=False) # Coluna para armazenar a descrição da despesa
    DiaCobranca: Mapped[int] = mapped_column(Integer, nullable=False) # Coluna para armazenar o dia de cobrança da despesa
    Valor: Mapped[Decimal] = mapped_column(Numeric(10, 2)) # Coluna para armazenar o valor da despesa
    Excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false")) # Coluna para indicar se a despesa está excluída
    IdUsuario: Mapped[int] = mapped_column(Integer, ForeignKey("Usuario.Id"), nullable=False) # Coluna para armazenar o id do usuário que criou a despesa
    
    Usuario = relationship("Usuario", back_populates="Despesas") # Relacionamento com a classe Usuario
    Categoria = relationship("Categoria", back_populates="Despesas") # Relacionamento com a classe Categoria
    Transacoes = relationship("Transacao", back_populates="Despesa") # Relacionamento com a classe Transacao

class Usuario(Base): # Definir a classe Usuario que herda de Base
    __tablename__ = "Usuario" # Nome da tabela no banco de dados

    Id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, index=True) # Coluna id como chave primária
    Nome: Mapped[str] = mapped_column(String(100), nullable=False) # Coluna para armazenar o nome do usuário
    Email: Mapped[str] = mapped_column(String(120), unique=True, index=True) # Coluna para armazenar o email do usuário
    PasswordHash: Mapped[str] = mapped_column(String(256), nullable=False) # Coluna para armazenar o hash da senha do usuário
    IsAdmin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false")) # Coluna para indicar se o usuário é administrador
    Excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false")) # Coluna para indicar se o usuário está excluído

    Categorias = relationship("Categoria", back_populates="Usuario") # Relacionamento com a classe Categoria
    Despesas = relationship("Despesa", back_populates="Usuario") # Relacionamento com a classe Despesa
    Transacoes = relationship("Transacao", back_populates="Usuario") # Relacionamento com a classe Transacao