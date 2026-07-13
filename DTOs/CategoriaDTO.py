from pydantic import BaseModel, ConfigDict, PositiveInt, field_validator
from pydantic_core import PydanticCustomError


class CategoriaCreate(BaseModel):
    IdTipoCategoria: PositiveInt
    Descricao: str

    @field_validator("Descricao")
    @classmethod
    def _descricao(cls, v: str) -> str:
        if not v.strip():
            raise PydanticCustomError("Descrição obrigatória", "A descrição é obrigatória.")
        if len(v) > 50:
            raise PydanticCustomError("Máximo de caracteres", "A descrição deve ter no máximo 50 caracteres.")
        return v

class CategoriaUpdate(CategoriaCreate):
    id: PositiveInt

class CategoriaOut(BaseModel):
    id: int
    IdTipoCategoria: int
    Descricao: str
    TipoCategoriaDescricao: str | None = None

    model_config = ConfigDict(from_attributes=True)