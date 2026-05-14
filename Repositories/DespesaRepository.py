from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from typing import Optional, List
from Entities.models import Despesa


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

    def get_all(self, db: Session) -> List[Despesa]:
        try:
            stmt = select(Despesa).where(Despesa.Excluido.is_(False)).order_by(Despesa.DiaCobranca, Despesa.IdCategoria, Despesa.Descricao)
            return list(db.scalars(stmt))
        except SQLAlchemyError as e:
            raise RuntimeError("Erro ao buscar despesas: " + str(e))