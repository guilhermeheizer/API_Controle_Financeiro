from sqlalchemy.orm import Session
from Repositories.TransacaoRepository import TransacaoRepository
from DTOs.TransacaoDTO import TransacaoCreate, TransacaoUpdate, TransacaoOut
from Entities.models import Transacao
from typing import Optional, List


class TransacaoService:
    def __init__(self, repo: TransacaoRepository):
        self.repo = repo

    def create(self, db: Session, transacaoCreate: TransacaoCreate) -> Optional[TransacaoOut]:
        entity = Transacao(**transacaoCreate.model_dump())
        transacaoCriada = self.repo.create(db, entity)
        if not transacaoCriada:
            raise ValueError("Erro ao criar a transação.")
        
        dto = TransacaoOut.model_validate(transacaoCriada)
        return dto.model_copy(update={
            "CategoriaDescricao": transacaoCriada.Categoria.Descricao if transacaoCriada.Categoria else None,
            "DespesaDescricao": transacaoCriada.Despesa.Descricao if transacaoCriada.Despesa else None
        })
    
    def update(self, db: Session, transacaoUpdate: TransacaoUpdate) -> Optional[TransacaoOut]:
        if getattr(transacaoUpdate, 'id', None) is None:
            raise ValueError("O atributo Id é obrigatório.")
        
        transacao = self.repo.get(db, transacaoUpdate.id)
        if not transacao:
            raise ValueError(f"Transação com id {transacaoUpdate.id} não encontrada ou excluída.")
        
        entity = Transacao(**transacaoUpdate.model_dump())
        transacaoAlterada = self.repo.update(db, entity)
        if not transacaoAlterada:
            raise ValueError("Erro ao atualizar a transação.")
        dto = TransacaoOut.model_validate(transacaoAlterada)
        return dto.model_copy(update={
            "CategoriaDescricao": transacaoAlterada.Categoria.Descricao if transacaoAlterada.Categoria else None,
            "DespesaDescricao": transacaoAlterada.Despesa.Descricao if transacaoAlterada.Despesa else None
        })
    
    def delete(self, db: Session, id_: int) -> bool:
        transacao = self.repo.get(db, id_)
        if not transacao:
            raise ValueError(f"Transação com id {id_} não encontrada ou excluída.")
        
        if transacao.Excluido:
            raise ValueError(f"Transação com id {id_} já foi excluída.")
        
        return self.repo.delete(db, id_)
    
    def get(self, db: Session, id_: int) -> Optional[TransacaoOut]:
        transacao = self.repo.get(db, id_)
        if not transacao:
            raise ValueError(f"Transação com id {id_} não encontrada ou excluída.")
            
        dto = TransacaoOut.model_validate(transacao)
        return dto.model_copy(update={
            "CategoriaDescricao": transacao.Categoria.Descricao if transacao.Categoria else None,
            "DespesaDescricao": transacao.Despesa.Descricao if transacao.Despesa else None
        })
    
    def get_all(self, db: Session) -> List[TransacaoOut]:
        transacoes = self.repo.get_all(db)
        return [TransacaoOut.model_validate(c).model_copy(
            update={
                "CategoriaDescricao": c.Categoria.Descricao if c.Categoria else None,
                "DespesaDescricao": c.Despesa.Descricao if c.Despesa else None
            }
        ) for c in transacoes]
    