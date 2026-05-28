from fastapi import APIRouter, Depends, HTTPException, status, responses
from DTOs.TransacaoDTO import TransacaoOut, TransacaoCreate, TransacaoUpdate
from Services.TransacaoService import TransacaoService
from Repositories.TransacaoRepository import TransacaoRepository
from sqlalchemy.orm import Session
from database import get_db
from typing import List

router = APIRouter(prefix="/transacao", tags=["Transacao"])

_service = TransacaoService(TransacaoRepository())

@router.post("/", response_model=TransacaoOut, status_code=status.HTTP_201_CREATED)
def create_transacao(transacao: TransacaoCreate, db: Session = Depends(get_db)):
    try:
        dto = _service.create(db, transacao)
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
    
@router.put("/", response_model=TransacaoOut)
def update_transacao(transacao: TransacaoUpdate, db: Session = Depends(get_db)):
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
def delete_transacao(id: int, db: Session = Depends(get_db)):
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
def get_transacao(id: int, db: Session = Depends(get_db)):
    try:
        return _service.get(db, id)
    except ValueError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
    
    
@router.get("/", response_model=List[TransacaoOut])
def list_transacaos(db: Session = Depends(get_db)):
    try:
        dto = _service.get_all(db)
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
