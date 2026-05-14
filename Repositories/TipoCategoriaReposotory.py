from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List
from Entities.models import TipoCategoria


class TipoCategoriaRepository:

    def get(self, db: Session, id_: int) -> Optional[TipoCategoria]:
        return db.get(TipoCategoria, id_)
    
    def get_all(self, db: Session) -> List[TipoCategoria]:
        stmt = select(TipoCategoria).order_by(TipoCategoria.Descricao)
        return list(db.scalars(stmt))
