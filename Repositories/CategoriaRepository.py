from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg2.errors import UniqueViolation
from sqlalchemy import select
from typing import Optional, List
from Entities.models import Categoria


class CategoriaRepository:

    def create(self, db: Session, categoria: Categoria) -> Categoria:
        try:
            db.add(categoria)
            db.commit()
            db.refresh(categoria)
            return categoria
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError("create: Erro ao criar a categoria: " + str(e))
    
    def update(self, db: Session, categoria: Categoria) -> Optional[Categoria]:
        try:
            merged = db.merge(categoria)
            db.commit()
            db.refresh(merged)
            return merged
        except IntegrityError as e:
            db.rollback()
            if isinstance(e.orig, UniqueViolation):
                raise ValueError("Já existe uma categoria com esta descrição.")
            raise RuntimeError("Erro de integridade no banco: " + str(e))
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError("update: Erro ao atualizar a categoria: " + str(e))

    def delete(self, db: Session, categoria: Categoria) -> bool:
        try:
            categoria.Excluido = True
            db.merge(categoria)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError("delete: Erro ao excluir a categoria: " + str(e))
            
    def get(self, db: Session, id_: int) -> Optional[Categoria]:
        try:
            stmt = select(Categoria).where(Categoria.id == id_, Categoria.Excluido.is_(False))
            return db.scalars(stmt).first()
        except SQLAlchemyError as e:
            raise RuntimeError("get: Erro ao buscar a categoria: " + str(e))
    
    def get_all(self, db: Session, idUsuario: int, idTipoCategoria: Optional[int]) -> List[Categoria]:
        try:
            stmt = select(Categoria).where(Categoria.Excluido.is_(False), Categoria.IdUsuario == idUsuario).order_by(Categoria.Descricao)
            if idTipoCategoria:
                stmt = stmt.where(Categoria.IdTipoCategoria == idTipoCategoria)
            return list(db.scalars(stmt))
        except SQLAlchemyError as e:
            raise RuntimeError("get_all: Erro ao buscar todas categorias: " + str(e))
        
    def get_by_descricao(self, db: Session, idTipoCategoria: int, descricao: str) -> Optional[Categoria]:
        try:
            # Buscar categoria por descrição, ignorando espaços em branco e considerando apenas categorias não excluídas
            descricao = descricao.strip()
            stmt = select(Categoria).where(Categoria.Descricao == descricao, Categoria.Excluido.is_(False), Categoria.IdTipoCategoria == idTipoCategoria)
            return db.scalars(stmt).first()
        except SQLAlchemyError as e:
            raise RuntimeError("get_by_descricao: Erro ao buscar a categoria por descrição: " + str(e))

    def get_by_descricao_contar(self, db: Session, idTipoCategoria: int, descricao: str) -> int:
        try:
            # Retorna quantas categorias existem com a mesma descrição, ignorando espaços em branco e considerando apenas categorias não excluídas
            descricao = descricao.strip().lower()
            stmt = (
                    select(Categoria)
                    .where(
                        Categoria.Descricao.ilike(descricao),
                        Categoria.Excluido.is_(False),
                        Categoria.IdTipoCategoria == idTipoCategoria
                    ))
            return len(list(db.scalars(stmt)))
        except SQLAlchemyError as e:
            raise RuntimeError("get_by_descricao_contar: Erro ao contar categorias por descrição: " + str(e))

    def usuario_has_categoria(self, db: Session, id_: int, idUsuario: int) -> bool:
        try:
            stmt = select(Categoria).where(Categoria.id == id_, Categoria.Excluido.is_(False), Categoria.IdUsuario == idUsuario)
            return db.scalars(stmt).first() is not None
        except SQLAlchemyError as e:
            raise RuntimeError("get: Erro ao buscar a categoria: " + str(e)) 