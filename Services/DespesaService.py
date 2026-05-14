from Repositories.DespesaRepository import DespesaRepository
from sqlalchemy.orm import Session
from DTOs.DespesaDTO import DespesaCreate, DespesaUpdate, DespesaOut
from typing import Optional, List
from Entities.models import Despesa


class DespesaService:
    def __init__(self, repo: DespesaRepository):
        self.repo = repo

    def create(self, db: Session, despesaCreate: DespesaCreate) -> Optional[DespesaOut]:
        entity = Despesa(**despesaCreate.model_dump())
        despesaCriada = self.repo.create(db, entity)
        if not despesaCriada:
            raise ValueError("Erro ao criar a despesa.")
        
        dto = DespesaOut.model_validate(despesaCriada)
        return dto.model_copy(update={
            "CategoriaDescricao": despesaCriada.Categoria.Descricao if despesaCriada.Categoria else None
        })
    
    def update(self, db: Session, despesaUpdate: DespesaUpdate) -> Optional[DespesaOut]:
        if getattr(despesaUpdate, 'id', None) is None:
            raise ValueError("O atributo Id é obrigatório.")
        
        despesa = self.repo.get(db, despesaUpdate.id)
        if not despesa:
            raise ValueError(f"Despesa com id {despesaUpdate.id} não encontrada ou excluída.")
        
        entity = Despesa(**despesaUpdate.model_dump())
        despesaAlterada = self.repo.update(db, entity)
        if not despesaAlterada:
            raise ValueError(f"Despesa com id {despesaUpdate.id} não encontrada.")
         
        dto = DespesaOut.model_validate(despesaAlterada)
        return dto.model_copy(update={
            "CategoriaDescricao": despesaAlterada.Categoria.Descricao if despesaAlterada.Categoria else None
        })
    
    def delete(self, db: Session, id_: int) -> bool:
        despesa = self.repo.get(db, id_)
        if not despesa:
            raise ValueError(f"Despesa com id {id_} não encontrada ou excluída.")
        
        if despesa.Excluido:
            raise ValueError(f"Despesa com id {id_} já foi excluída.")
        
        return self.repo.delete(db, id_)

    def get(self, db: Session, id_: int) -> Optional[DespesaOut]:
        despesa = self.repo.get(db, id_)
        if not despesa:
            raise ValueError(f"Despesa com id {id_} não encontrada ou excluída.")
        
        dto = DespesaOut.model_validate(despesa)
        return dto.model_copy(update={
            "CategoriaDescricao": despesa.Categoria.Descricao if despesa.Categoria else None
        })
    
    def get_all(self, db: Session) -> List[DespesaOut]:
        despesas = self.repo.get_all(db)
        return [
            DespesaOut(
                id=d.id,
                IdCategoria=d.IdCategoria,
                Descricao=d.Descricao,
                DiaCobranca=d.DiaCobranca,
                Valor=d.Valor,
                CategoriaDescricao=d.Categoria.Descricao if d.Categoria else None,
            )
            for d in despesas
        ]