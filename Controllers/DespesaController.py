from fastapi import APIRouter, Depends, HTTPException, status, responses
from DTOs.DespesaDTO import DespesaOut, DespesaCreate, DespesaUpdate
from Services.DespesaService import DespesaService
from Repositories.DespesaRepository import DespesaRepository
from sqlalchemy.orm import Session
from database import get_db
from typing import List

router = APIRouter(prefix="/despesa", tags=["Despesa"])

_service = DespesaService(DespesaRepository())

@router.post("/", response_model=DespesaOut, status_code=status.HTTP_201_CREATED)
def create_despesa(despesa: DespesaCreate, db: Session = Depends(get_db)):
    try:
        dto = _service.create(db, despesa)
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
    
@router.put("/", response_model=DespesaOut)
def update_despesa(despesa: DespesaUpdate, db: Session = Depends(get_db)):
    try:
        dto = _service.update(db, despesa)
        if not dto:
            raise HTTPException(status_code=404, detail=f"Despesa com id {despesa.id} não encontrada.")
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_despesa(id: int, db: Session = Depends(get_db)):
    try:
        ok = _service.delete(db, id)
        if not ok:
            raise HTTPException(status_code=404, detail=f"Despesa com id {id} não encontrada.")
        return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))

@router.get("/{id}", response_model=DespesaOut)
def get_despesa(id: int, db: Session = Depends(get_db)):
    try:
        return _service.get(db, id)
    except ValueError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
    
    
@router.get("/", response_model=List[DespesaOut])
def list_despesas(db: Session = Depends(get_db)):
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
