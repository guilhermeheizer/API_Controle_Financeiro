from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import Optional, List
from Entities.models import Transacao


class TransacaoRepository:

    def create(self, db: Session, transacao: Transacao) -> Transacao:
        try:
            db.add(transacao)
            db.commit()
            db.refresh(transacao)
            return transacao
        except IntegrityError:
            db.rollback()
            raise ValueError("Erro ao criar transação.")
        except SQLAlchemyError:
            db.rollback()
            raise ValueError("Erro ao salvar transação.")

    def update(self, db: Session, transacao: Transacao) -> Optional[Transacao]:
        try:
            merged = db.merge(transacao)
            db.commit()
            db.refresh(merged)
        except SQLAlchemyError:
            db.rollback()
            raise ValueError("Erro ao atualizar transação.")
        return merged
    
    def delete(self, db: Session, id_: int) -> bool:
        try:
            transacao = db.get(Transacao, id_)
            if transacao is None:
                return False
            
            if not transacao.Excluido:
                transacao.Excluido = True
                db.merge(transacao)
                db.commit()
            return True
        except SQLAlchemyError:
            db.rollback()
            raise ValueError("Erro ao excluir transação.")

    def get(self, db: Session, id_: int) -> Optional[Transacao]:
        try:
            stmt = select(Transacao).where(Transacao.id == id_, Transacao.Excluido.is_(False))
            return db.scalars(stmt).first()
        except SQLAlchemyError:
            raise ValueError("Erro ao buscar transação.")

    def get_all(self, db: Session) -> List[Transacao]:
        try:
            stmt = select(Transacao).where(Transacao.Excluido.is_(False)).order_by(Transacao.Descricao)
        except SQLAlchemyError:
            raise ValueError("Erro ao listar transações.")
        return list(db.scalars(stmt))