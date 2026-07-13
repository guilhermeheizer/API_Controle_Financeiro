from fastapi import APIRouter, Depends, HTTPException
from DTOs.TipoCategoriaDTO import TipoCategoriaOut
from Services.TipoCategoriaServices import TipoCategoriaServices
from Repositories.TipoCategoriaReposotory import TipoCategoriaRepository
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from Utilities.dependecies import get_current_clains


router = APIRouter(prefix="/tipo-categoria", tags=["TipoCategoria"])

_service = TipoCategoriaServices(TipoCategoriaRepository())

@router.get("/{id}", response_model=TipoCategoriaOut)
def get_tipo_categoria(id: int, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    try:
        dto = _service.get(db, id)
        return dto
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        print(f"Erro ao obter TipoCategoria: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
    
    
@router.get("/", response_model=List[TipoCategoriaOut])
def list_tipo_categoria(db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    try:
        return _service.get_all(db)
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        print(f"Erro ao obter TipoCategoria: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
