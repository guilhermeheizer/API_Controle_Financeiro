from fastapi import APIRouter, Depends, HTTPException, status, responses
from DTOs.TransacaoDTO import TransacaoOut, TransacaoCreate, TransacaoUpdate
from Services.TransacaoService import TransacaoService
from Services.CategoriaService import CategoriaService
from Services.DespesaService import DespesaService
from Repositories.TransacaoRepository import TransacaoRepository
from Repositories.CategoriaRepository import CategoriaRepository
from Repositories.DespesaRepository import DespesaRepository
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from Utilities.dependecies import get_current_clains

router = APIRouter(prefix="/transacao", tags=["Transacao"])

_service = TransacaoService(TransacaoRepository())
_serviceCategoria = CategoriaService(CategoriaRepository())
_serviceDespesa = DespesaService(DespesaRepository())

@router.post("/", response_model=TransacaoOut, status_code=status.HTTP_201_CREATED)
def create_transacao(transacao: TransacaoCreate, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")
    
    user_id = int(user_id)
    if transacao.IdCategoria is not None:
        usuario_has_categoria = _serviceCategoria.usuario_has_categoria(db, transacao.IdCategoria, user_id)
        if not usuario_has_categoria:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Você não tem permissão para usar a categoria {transacao.IdCategoria}"
            )
        
    if transacao.IdDespesa is not None:
        usuario_has_despesa = _serviceDespesa.usuario_has_despesa(db, transacao.IdDespesa, user_id)
        if not usuario_has_despesa:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Você não tem permissão para usar a despesa {transacao.IdDespesa}"
            )
    
    try:
        dto = _service.create(db, transacao, user_id)
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
    
@router.put("/", response_model=TransacaoOut)
def update_transacao(transacao: TransacaoUpdate, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")
    
    if transacao.IdCategoria is not None:
        usuario_has_categoria = _serviceCategoria.usuario_has_categoria(db, transacao.IdCategoria, user_id)
        if not usuario_has_categoria:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Você não tem permissão para usar a categoria {transacao.IdCategoria}"
            )
        
    if transacao.IdDespesa is not None:
        usuario_has_despesa = _serviceDespesa.usuario_has_despesa(db, transacao.IdDespesa, user_id)
        if not usuario_has_despesa:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Você não tem permissão para usar a despesa {transacao.IdDespesa}"
            )
        
    user_id = int(user_id)
    usuario_has_transacao = _service.usuario_has_transacao(db, transacao.id, user_id)
    if not usuario_has_transacao:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não tem permissão para alterar esta transação.")
         
    if transacao.IdCategoria is not None:
        usuario_has_categoria = _serviceCategoria.usuario_has_categoria(db, transacao.IdCategoria, user_id)
        if not usuario_has_categoria:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Você não tem permissão para usar a categoria {transacao.IdCategoria}"
            )  
         
    try:
        dto = _service.update(db, transacao)
        if not dto:
            raise HTTPException(status_code=404, detail=f"Transacao com id {transacao.id} não encontrada.")
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transacao(id: int, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")

    user_id = int(user_id)
    usuario_has_transacao = _service.usuario_has_transacao(db, id, user_id)
    if not usuario_has_transacao:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não tem permissão para excluir esta transação.")
    
    try:
        ok = _service.delete(db, id)
        if not ok:
            raise HTTPException(status_code=404, detail=f"Transacao com id {id} não encontrada.")
        return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))

@router.get("/{id}", response_model=TransacaoOut)
def get_transacao(id: int, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")

    user_id = int(user_id)
    usuario_has_transacao = _service.usuario_has_transacao(db, id, user_id)
    if not usuario_has_transacao:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não tem permissão para visualizar esta transação.")
    
    try:
        return _service.get(db, id)
    except ValueError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
    
    
@router.get("/", response_model=List[TransacaoOut])
def list_transacaos(db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")
    
    try:
        user_id = int(user_id)
        dto = _service.get_all(db, user_id)
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
