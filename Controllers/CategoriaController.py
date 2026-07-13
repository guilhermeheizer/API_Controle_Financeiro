from fastapi import APIRouter, Depends, HTTPException, status, responses, Query
from DTOs.CategoriaDTO import CategoriaOut, CategoriaCreate, CategoriaUpdate
from Services.CategoriaService import CategoriaService  
from Repositories.CategoriaRepository import CategoriaRepository
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from Utilities.dependecies import get_current_clains
from typing import Optional

router = APIRouter(prefix="/categoria", tags=["Categoria"])

_service = CategoriaService(CategoriaRepository())

@router.post("/", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
def create_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")

    try:
        user_id = int(user_id)
        dto = _service.create(db, categoria, user_id)
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))

@router.put("/", response_model=CategoriaOut)
def update_categoria(categoria: CategoriaUpdate, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")

    user_id = int(user_id)
    usuario_has_categoria = _service.usuario_has_categoria(db, categoria.id, user_id)
    if not usuario_has_categoria:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não tem permissão para atualizar esta categoria.")

    try:
        dto = _service.update(db, categoria)
        if not dto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria com id {categoria.id} não encontrada.")
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(id: int, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")

    user_id = int(user_id)
    usuario_has_categoria = _service.usuario_has_categoria(db, id, user_id)
    if not usuario_has_categoria:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não tem permissão para excluir esta categoria.")

    try:
        ok = _service.delete(db, id)
        if not ok:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria com id {id} não encontrada.")
        return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))

@router.get("/{id}", response_model=CategoriaOut)
def get_categoria(id: int, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")

    user_id = int(user_id)
    usuario_has_categoria = _service.usuario_has_categoria(db, id, user_id)
    if not usuario_has_categoria:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não tem permissão para visualizar esta categoria.")

    try:
        return _service.get(db, id)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))


@router.get("/", response_model=List[CategoriaOut])
def list_categorias(db: Session = Depends(get_db), clains: dict = Depends(get_current_clains), idTipoCategoria: Optional[int] = Query(None)):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")
    user_id = int(user_id)

    try:
        dto = _service.get_all(db, user_id, idTipoCategoria)
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))
