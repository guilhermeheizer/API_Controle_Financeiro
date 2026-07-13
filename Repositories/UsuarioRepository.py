from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg2.errors import UniqueViolation
from sqlalchemy import select
from typing import Optional, List
from Entities.models import Usuario


class UsuarioRepository:

    def create(self, db: Session, usuario: Usuario) -> Usuario:
        try:
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
            return usuario
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError("create: Erro ao criar o usuário: " + str(e))

    def update(self, db: Session, usuario: Usuario) -> Optional[Usuario]:
        try:
            merged = db.merge(usuario)
            db.commit()
            db.refresh(merged)
            return merged
        except IntegrityError as e:
            db.rollback()
            if isinstance(e.orig, UniqueViolation):
                raise ValueError("Já existe um usuário com este email.")
            raise RuntimeError("Erro de integridade no banco: " + str(e))
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError("update: Erro ao atualizar o usuário: " + str(e))

    def delete(self, db: Session, usuario: Usuario) -> bool:
        try:
            usuario.Excluido = True
            db.merge(usuario)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError("delete: Erro ao excluir o usuário: " + str(e))

    def get(self, db: Session, id_: int) -> Optional[Usuario]:
        try:
            stmt = select(Usuario).where(Usuario.Id == id_, Usuario.Excluido.is_(False))
            return db.scalars(stmt).first()
        except SQLAlchemyError as e:
            raise RuntimeError("get: Erro ao buscar o usuário: " + str(e))

    def get_all(self, db: Session) -> List[Usuario]:
        try:
            stmt = select(Usuario).where(Usuario.Excluido.is_(False)).order_by(Usuario.Nome)
            return list(db.scalars(stmt))
        except SQLAlchemyError as e:
            raise RuntimeError("get_all: Erro ao buscar todos os usuários: " + str(e))

    # Metodo para verificar se existe algum regsitro na tabela Usuario, para criar o primeiro usuario admin   
    def existe_usuario(self, db: Session) -> bool:
        try:
            return db.query(Usuario).filter(Usuario.Excluido.is_(False)).first() is not None
        except SQLAlchemyError as e:
            raise RuntimeError("existe_usuario: Erro ao verificar existência do usuário: " + str(e))
        
    def get_by_email(self, db: Session, email: str) -> Optional[Usuario]:
        try:
            stmt = select(Usuario).where(Usuario.Email == email.lower(), Usuario.Excluido.is_(False))
            return db.scalars(stmt).first()
        except SQLAlchemyError as e:
            raise RuntimeError("get_by_email: Erro ao buscar usuário pelo email: " + str(e))