from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, extract, func
from typing import Optional, List
from Entities.models import Despesa, Categoria
from datetime import datetime


class DespesaRepository:

    def create(self, db: Session, despesa: Despesa) -> Despesa:
        try:
            db.add(despesa)
            db.commit()
            db.refresh(despesa)
            return despesa
        except IntegrityError as e:
            db.rollback()
            raise ValueError("Erro ao criar despesa: " + str(e))
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError("Erro ao criar despesa: " + str(e))

    def update(self, db: Session, despesa: Despesa) -> Optional[Despesa]:
        try:
            merged = db.merge(despesa)
            db.commit()
            db.refresh(merged)
            return merged
        except IntegrityError as e:
            db.rollback()
            raise ValueError("Erro ao atualizar despesa: " + str(e))
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError("Erro ao atualizar despesa: " + str(e))
    
    def delete(self, db: Session, id_: int) -> bool:
        try:
            despesa = db.get(Despesa, id_)
            if despesa is None:
                return False
            
            if not despesa.Excluido:
                despesa.Excluido = True
                db.merge(despesa)
                db.commit()
                
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError("Erro ao excluir despesa: " + str(e))

    def get(self, db: Session, id_: int) -> Optional[Despesa]:
        try:
            stmt = select(Despesa).where(Despesa.id == id_, Despesa.Excluido.is_(False))
            return db.scalars(stmt).first()
        except SQLAlchemyError as e:
            raise RuntimeError("Erro ao buscar despesa: " + str(e))

    def get_all(self, db: Session, IdUsuario: int, despesaDeHoje: bool) -> List[Despesa]:
        try:
            stmt = select(Despesa).where(Despesa.Excluido.is_(False), Despesa.IdUsuario == IdUsuario).order_by(Despesa.DiaCobranca, Despesa.IdCategoria, Despesa.Descricao)
            if despesaDeHoje:
                stmt = stmt.where(Despesa.DiaCobranca == datetime.now().day)
                
            return list(db.scalars(stmt))
        except SQLAlchemyError as e:
            raise RuntimeError("Erro ao buscar despesas: " + str(e))
        
    def get_quantidade_despesas_por_categoria(self, db: Session, user_id: int):
        try:    
            query = (
                db.query(
                    Categoria.Descricao.label('categoria'),
                    func.count(Despesa.id).label('quantidade')
                )
                .join(Categoria, Despesa.IdCategoria == Categoria.id)
                .filter(
                    Despesa.Excluido == False,
                    Despesa.IdUsuario == user_id
                )
                .group_by(Categoria.Descricao)
                .order_by(func.count(Despesa.id).desc(), Categoria.Descricao.asc())
            )

            results = query.all()

            return [
                {"categoria": r.categoria, "quantidade": int(r.quantidade or 0)}
                for r in results
            ]
        except SQLAlchemyError as e:
            raise ValueError("Erro ao calcular quantidade de despesas por categoria: " + str(e))
        
    def usuario_has_despesa(self, db: Session, id_: int, idUsuario: int) -> bool:
        try:
            stmt = select(Despesa).where(Despesa.id == id_, Despesa.IdUsuario == idUsuario, Despesa.Excluido.is_(False))
            return db.scalars(stmt).first() is not None
        except SQLAlchemyError as e:
            raise RuntimeError("get: Erro ao buscar a despesa: " + str(e)) 