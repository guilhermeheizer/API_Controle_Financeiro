from pydantic import BaseModel, ConfigDict, PositiveInt, field_validator
from typing import Optional
import re
from pydantic_core import PydanticCustomError


class UsuarioCreate(BaseModel):
    Nome: str
    Email: str
    Senha: str

    @field_validator("Nome")
    @classmethod
    def _nome(cls, v: str) -> str:
        if not v.strip():
            raise PydanticCustomError("Nome obrigatório.", "O nome é obrigatório.")
        if v is not None and len(v.strip()) < 6 or len(v.strip()) > 100:
            raise PydanticCustomError("Mínimo e máxmo de caracteres", "O nome deve ter pelo menos 6 caracteres e no máximo 100 caracteres.")
        return v
    
    @field_validator("Email")
    @classmethod
    def _email(cls, v: str):
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise PydanticCustomError("Email", "Email inválido.")
        return v
    
    @field_validator("Senha")
    @classmethod
    def _senha(cls, v: str):
        if v is None:
            raise PydanticCustomError("Senha obrigatória", "A senha é obrigatória.")
        if v is not None and len(v) < 6 or len(v) > 80:
            raise PydanticCustomError("Mínimo e máxmo de caracteres", "A senha deve ter pelo menos 6 caracteres e no máximo 80 caracteres.")
        return v

class UsuarioUpdate(BaseModel):
    Id: PositiveInt
    Nome: Optional[str] = None
    Email: Optional[str] = None
    Senha: Optional[str] = None

    @field_validator("Nome")
    @classmethod
    def _nome(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if v is not None and len(v) < 6 or len(v) > 100:
            raise PydanticCustomError("Mínimo e máxmo de caracteres", "O nome deve ter pelo menos 6 caracteres e no máximo 100 caracteres.")
        return v
    
    @field_validator("Email")
    @classmethod
    def _email(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if v is not None and not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise PydanticCustomError("Email", "Email inválido.")
        return v
    
    @field_validator("Senha")
    @classmethod
    def _senha(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if v is not None and len(v) < 6 or len(v) > 80:
            raise PydanticCustomError("Mínimo e máxmo de caracteres", "A senha deve ter pelo menos 6 caracteres e no máximo 80 caracteres.")
        return v

class UsuarioOut(BaseModel):
    Id: int
    Nome: str
    Email: str #EmailStr
    IsAdmin: bool

    model_config = ConfigDict(from_attributes=True)

class UsuarioLogin(BaseModel):
    Email: str
    Senha: str
    
    @field_validator("Email")
    @classmethod
    def _email(cls, v: str):
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise PydanticCustomError("Email", "Email inválido.")
        return v
    
    @field_validator("Senha")
    @classmethod
    def _senha(cls, v: str):
        if v is None or v == "":
            raise PydanticCustomError("Senha obrigatória", "A senha é obrigatória.")
        if v is not None and len(v) < 6 or len(v) > 80:
            raise PydanticCustomError("Mínimo e máxmo de caracteres", "A senha deve ter pelo menos 6 caracteres e no máximo 80 caracteres.")
        return v
    
class UsuarioToken(BaseModel):
    access_token: str
    token_type: str

class ExisteUsuario(BaseModel):
    existeUsuario: bool

class UsuarioUpdatePassword(BaseModel):
    Senha: str  
    
    @field_validator("Senha", mode="before")
    @classmethod
    def _senha(cls, v: str):
        if v is None or v == "":
            raise PydanticCustomError("Senha obrigatória", "A senha é obrigatória.")
        if v is not None and len(v) < 6 or len(v) > 80:
            raise PydanticCustomError("Mínimo e máxmo de caracteres", "A senha deve ter pelo menos 6 caracteres e no máximo 80 caracteres.")
        return v    