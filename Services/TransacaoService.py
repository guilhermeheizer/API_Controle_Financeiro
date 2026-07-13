from datetime import date

from sqlalchemy.orm import Session
from Repositories.TransacaoRepository import TransacaoRepository
from DTOs.TransacaoDTO import TransacaoCreate, TransacaoUpdate, TransacaoOut
from DTOs.GraficoDTO import EntradasSaidaMes, Resumo, GastoMes, GastoCategoria
from Entities.models import Transacao
from typing import Optional, List


class TransacaoService:
    def __init__(self, repo: TransacaoRepository):
        self.repo = repo

    def create(self, db: Session, transacaoCreate: TransacaoCreate, user_id: int) -> Optional[TransacaoOut]:
        entity = Transacao(**transacaoCreate.model_dump(), IdUsuario = user_id)
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
    
    def get_all(self, db: Session, user_id: int) -> List[TransacaoOut]:
        transacoes = self.repo.get_all(db, user_id)
        return [TransacaoOut.model_validate(c).model_copy(
            update={
                "CategoriaDescricao": c.Categoria.Descricao if c.Categoria else None,
                "DespesaDescricao": c.Despesa.Descricao if c.Despesa else None
            }
        ) for c in transacoes]
    
    def get_resumo(self, db: Session,  datainicio: date, datafim: date, user_id: int) -> Resumo:
        quantidade_entradas = self.repo.get_quantidade_entradas(db, datainicio, datafim, user_id)
        quantidade_saidas = self.repo.get_quantidade_saidas(db, datainicio, datafim, user_id)
        despesa_mensal = self.repo.get_despesa_mensal(db, user_id)
        return Resumo(
            quantidade_entradas=quantidade_entradas,
            quantidade_saidas=quantidade_saidas,
            despesa_mensal=despesa_mensal
        )
    
    def get_entradas_saida_por_mes(self, db: Session,  datainicio: date, datafim: date, user_id: int) -> List[EntradasSaidaMes]:
        entradasSaidasMesDict = self.repo.get_entradas_saidas_por_mes(db, datainicio, datafim, user_id)
        return [EntradasSaidaMes(**item) for item in entradasSaidasMesDict] # Jogando o resultado do dicionário mapeando para o DTO EntradasSaidaMes
    
    def get_gastos_por_mes(self, db: Session,  datainicio: date, datafim: date, user_id: int) -> List[GastoMes]:
        gastosPorMesDict = self.repo.get_gastos_por_mes(db, datainicio, datafim, user_id)
        return [GastoMes(**item) for item in gastosPorMesDict] # Jogando o resultado do dicionário mapeando para o DTO GastoMes
    
    def get_gastos_por_categoria(self, db: Session,  datainicio: date, datafim: date, user_id: int) -> List[GastoCategoria]:
        gastosPorCategoriaDict = self.repo.get_gastos_por_categoria(db, datainicio, datafim, user_id)
        return [GastoCategoria(**item) for item in gastosPorCategoriaDict] # Jogando o resultado do dicionário mapeando para o DTO GastoCategoria
    
    def usuario_has_transacao(self, db: Session, id_: int, idUsuario: int) -> bool:
        return self.repo.usuario_has_transacao(db, id_, idUsuario)