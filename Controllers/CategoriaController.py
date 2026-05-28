from fastapi import APIRouter, Depends, HTTPException, status, responses
from DTOs.CategoriaDTO import CategoriaOut, CategoriaCreate, CategoriaUpdate
from Services.CategoriaService import CategoriaServide  
from Repositories.CategoriaRepository import CategoriaRepository
from sqlalchemy.orm import Session
from database import get_db
from typing import List

router = APIRouter(prefix="/categoria", tags=["Categoria"])

_service = CategoriaServide(CategoriaRepository())

@router.post("/", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
def create_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    try:
        dto = _service.create(db, categoria)
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
    
@router.put("/", response_model=CategoriaOut)
def update_categoria(categoria: CategoriaUpdate, db: Session = Depends(get_db)):
    try:
        dto = _service.update(db, categoria)
        if not dto:
            raise HTTPException(status_code=404, detail=f"Categoria com id {categoria.id} não encontrada.")
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(id: int, db: Session = Depends(get_db)):
    try:
        ok = _service.delete(db, id)
        if not ok:
            raise HTTPException(status_code=404, detail=f"Categoria com id {id} não encontrada.")
        return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))

@router.get("/{id}", response_model=CategoriaOut)
def get_categoria(id: int, db: Session = Depends(get_db)):
    try:
        return _service.get(db, id)
    except ValueError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))
    
    
@router.get("/", response_model=List[CategoriaOut])
def list_categorias(db: Session = Depends(get_db)):
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
