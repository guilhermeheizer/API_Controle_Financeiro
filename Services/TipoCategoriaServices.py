from sqlalchemy.orm import Session
from Repositories.TipoCategoriaReposotory import TipoCategoriaRepository
from DTOs.TipoCategoriaDTO import TipoCategoriaOut
from typing import Optional, List
from fastapi import HTTPException


class TipoCategoriaServices:
    def __init__(self, repo: TipoCategoriaRepository):
        self.repo = repo

    def get(self, db: Session, id_: int) -> Optional[TipoCategoriaOut]:
        e = self.repo.get(db, id_)
        if not e:
             raise HTTPException(status_code=404, detail=f"TipoCategoria com id {id_} não encontrado.")
        
        return None if not e else TipoCategoriaOut.model_validate(e)

    def get_all(self, db: Session) -> List[TipoCategoriaOut]:
        e = self.repo.get_all(db)
        if not e:
             raise HTTPException(status_code=404, detail="Nenhum Tipo Categoria encontrado.")
        
        return [TipoCategoriaOut.model_validate(e) for e in e]