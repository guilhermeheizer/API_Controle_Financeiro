from fastapi import APIRouter, Depends, HTTPException, status, responses
from DTOs.UsuarioDTO import UsuarioLogin, UsuarioOut, UsuarioCreate, UsuarioUpdate, UsuarioUpdatePassword
from Services.UsuarioService import UsuarioServide  
from Repositories.UsuarioRepository import UsuarioRepository
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from Utilities.auth import create_access_token
from Utilities.dependecies import get_current_clains_optinal, get_current_clains
from pydantic import ValidationError


router = APIRouter(prefix="/usuario", tags=["Usuario"])
_service = UsuarioServide(UsuarioRepository()) # Instancia do serviço com a implementação do repositório para injetar UsuarioRepository no UsuarioService

@router.post("/register", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db), clains: dict | None= Depends(get_current_clains_optinal)):
    try:
        existe_usuario = _service.existe_usuario(db)
        if existe_usuario:
            if not clains or not clains.get("is_admin", False):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                    detail="Apenas administradores podem criar novos usuários.")
        
        existing_user = _service.repo.get_by_email(db, usuario.Email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Já existe um usuário com este email.")
        
        dto = _service.create(db, usuario)
        return dto
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))

@router.post("/login")
def login(body: UsuarioLogin, db: Session = Depends(get_db)):
    try:
        # print(f"Usuario e senha:{body.Email} / {body.Senha}")
        usuario = _service.repo.get_by_email(db, body.Email)
        if not usuario or usuario.Excluido:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos.")
        
        if not _service.verify_password(db, body):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos.")
        
        token_data = {"sub": usuario.Email, "id": usuario.Id, "is_admin": usuario.IsAdmin}
        access_token = create_access_token(data=token_data)

        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))
    
@router.get("/existe-usuario")
def existe_usuario(db: Session = Depends(get_db)):
    try:
        existe_usuario = _service.existe_usuario(db)
        return {"existeUsuario": existe_usuario}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))

@router.put("", response_model=UsuarioOut, status_code=status.HTTP_200_OK)
def atualizar_senha_usuario(body: UsuarioUpdatePassword, db: Session = Depends(get_db), clains: dict = Depends(get_current_clains)):
    try:
        user_id = clains.get("id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")
        
        usuarioUpdate = UsuarioUpdate(Id=user_id, Senha=body.Senha)

        dto = _service.update(db, usuarioUpdate)
        if not dto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario com id {user_id} não encontrado ou excluído.")
        
        return dto
    
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex))
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor: " + str(e))