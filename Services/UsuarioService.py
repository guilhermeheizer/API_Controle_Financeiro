from Repositories.UsuarioRepository import UsuarioRepository
from sqlalchemy.orm import Session
from DTOs.UsuarioDTO import UsuarioCreate, UsuarioUpdate, UsuarioOut, UsuarioLogin
from typing import Optional, List
from Entities.models import Usuario
from Utilities.auth import hash_password, verify_password


class UsuarioServide:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def create(self, db: Session, usuarioCreate: UsuarioCreate) -> Optional[UsuarioOut]:
        hashed_password = hash_password(usuarioCreate.Senha)
        primeiro_usuario = not self.repo.existe_usuario(db)
        entity = Usuario(
            Nome=usuarioCreate.Nome,
            Email=usuarioCreate.Email.lower(),
            PasswordHash=hashed_password,
            IsAdmin=primeiro_usuario
        )
        usuarioCriado = self.repo.create(db, entity)
        if not usuarioCriado:
            raise ValueError("Erro ao criar o usuario.")
        
        dto = UsuarioOut.model_validate(usuarioCriado)
        return dto
    
    def update(self, db: Session, usuarioUpdate: UsuarioUpdate) -> Optional[UsuarioOut]:
        usuarioSelecionado = self.repo.get(db, usuarioUpdate.Id)
        if not usuarioSelecionado:
            raise ValueError(f"Usuario com id {usuarioUpdate.Id} não encontrada ou excluída.")
        
        if usuarioSelecionado.Excluido:
            raise ValueError(f"Usuario com id {usuarioUpdate.Id} já foi excluída.")
        
        if usuarioUpdate.Nome is not None:
            usuarioSelecionado.Nome = usuarioUpdate.Nome

        if usuarioUpdate.Email is not None:
            usuarioSelecionado.Email = usuarioUpdate.Email.lower()

        if usuarioUpdate.Senha is not None:
            hashed_password = hash_password(usuarioUpdate.Senha)
            usuarioSelecionado.PasswordHash = hashed_password

        UsuarioUpdated = self.repo.update(db, usuarioSelecionado)
        if not UsuarioUpdated:
            raise ValueError("Erro ao atualizar o usuario.")
        dto = UsuarioOut.model_validate(UsuarioUpdated)

        return dto

    def delete(self, db: Session, id_: int) -> bool:
        usuario = self.repo.get(db, id_)
        if not usuario:
            raise ValueError(f"Usuario com id {id_} não encontrado ou excluído.")
        
        if usuario.Excluido:
            raise ValueError(f"Usuario com id {id_} já foi excluído.")
        
        usuario.Excluido = True
        db.commit()

        return True

    def get(self, db: Session, id_: int) -> Optional[UsuarioOut]:
        usuario = self.repo.get(db, id_)
        if not usuario:
            raise ValueError(f"Usuario com id {id_} não encontrado ou excluído.")
        
        dto = UsuarioOut.model_validate(usuario)

        return dto
    
    def get_all(self, db: Session) -> List[UsuarioOut]:
        usuarios = self.repo.get_all(db)
        return [
            UsuarioOut.model_validate(usuario) for usuario in usuarios
        ]
    
    def get_by_email(self, db: Session, email: str) -> Optional[UsuarioOut]:
        usuario = self.repo.get_by_email(db, email)
        if not usuario:
            raise ValueError(f"Usuario com email {email} não encontrado ou excluído.")
        
        dto = UsuarioOut.model_validate(usuario)

        return dto
    
    def verify_password(self, db: Session, usuarioLogin: UsuarioLogin) -> bool:
        usuario = self.repo.get_by_email(db, usuarioLogin.Email)
        if not usuario:
            raise ValueError(f"Usuario com email {usuarioLogin.Email} não encontrado ou excluído.")
        
        return verify_password(usuarioLogin.Senha, usuario.PasswordHash)
    
    def existe_usuario(self, db: Session) -> bool:
        return self.repo.existe_usuario(db)