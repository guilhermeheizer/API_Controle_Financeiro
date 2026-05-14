from pydantic import BaseModel, ConfigDict, PositiveInt, field_validator
from typing_extensions import Annotated
from  pydantic.types import StringConstraints


class CategoriaCreate(BaseModel):
    IdTipoCategoria: PositiveInt
    Descricao: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]

    @field_validator("Descricao")
    @classmethod
    def _descricao(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("A descrição é obrigatória.")
        return v

class CategoriaUpdate(CategoriaCreate):
    id: PositiveInt

class CategoriaOut(BaseModel):
    id: int
    IdTipoCategoria: int
    Descricao: str
    TipoCategoriaDescricao: str | None = None

    model_config = ConfigDict(from_attributes=True)