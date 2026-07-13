from fastapi import APIRouter, Depends, HTTPException, status, responses, Query
from DTOs.DespesaDTO import DespesaOut, DespesaCreate, DespesaUpdate
from Services.DespesaService import DespesaService
from Services.CategoriaService import CategoriaService
from Repositories.DespesaRepository import DespesaRepository
from Repositories.CategoriaRepository import CategoriaRepository
from sqlalchemy.orm import Session
from database import get_db
from typing import List, Optional
from Utilities.dependecies import get_current_clains


router = APIRouter(prefix="/despesa", tags=["Despesa"])

_service = DespesaService(DespesaRepository())
_serviceCategoria = CategoriaService(CategoriaRepository())

@router.post("/", response_model=DespesaOut, status_code=status.HTTP_201_CREATED)
def create_despesa(despesa: DespesaCreate, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")
    
    categoria = _serviceCategoria.get(db, despesa.IdCategoria)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")
    
    if categoria.IdTipoCategoria == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo categoria informando é de entrada, informe um tipo que seja saída.")

    user_id = int(user_id)
    usuario_has_categoria = _serviceCategoria.usuario_has_categoria(db, despesa.IdCategoria, user_id)
    if not usuario_has_categoria:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Você não tem permissão para usar a categoria {despesa.IdCategoria}")
    
    try:
        dto = _service.create(db, despesa, user_id)
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))
    
@router.put("/", response_model=DespesaOut)
def update_despesa(despesa: DespesaUpdate, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")
    
    categoria = _serviceCategoria.get(db, despesa.IdCategoria)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")
    
    if categoria.IdTipoCategoria == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo categoria informando é de entrada, informe um tipo que seja saída.")
    
    user_id = int(user_id)
    usuario_has_despesa = _service.usuario_has_despesa(db, despesa.id, user_id)
    if not usuario_has_despesa:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não tem permissão para atualizar esta despesa.")
    usuario_has_categoria = _serviceCategoria.usuario_has_categoria(db, despesa.IdCategoria, user_id)
    if not usuario_has_categoria:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Você não tem permissão para usar a categoria {despesa.IdCategoria}")
    
    try:
        dto = _service.update(db, despesa)
        if not dto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Despesa com id {despesa.id} não encontrada.")
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_despesa(id: int, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")

    user_id = int(user_id)
    usuario_has_despesa = _service.usuario_has_despesa(db, id, user_id)
    if not usuario_has_despesa:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não tem permissão para excluir esta despesa.")
    try:
        ok = _service.delete(db, id)
        if not ok:
            raise HTTPException(status_code=404, detail=f"Despesa com id {id} não encontrada.")
        return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))

@router.get("/{id}", response_model=DespesaOut)
def get_despesa(id: int, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")

    user_id = int(user_id)
    usuario_has_categoria = _service.usuario_has_despesa(db, id, user_id)
    if not usuario_has_categoria:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não tem permissão para visualizar esta despesa.")

    try:
        return _service.get(db, id)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))
    
    
@router.get("/", response_model=List[DespesaOut])
def list_despesas(db: Session = Depends(get_db), 
                  clains: dict = Depends(get_current_clains),
                  despesaDeHoje: bool = Query(False, description="Filtrar despesas do dia atual")):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")
    user_id = int(user_id)

    try:
        dto = _service.get_all(db, user_id, despesaDeHoje)
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))
