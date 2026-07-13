from pydantic import BaseModel, ConfigDict, PositiveInt, field_validator, conint
from  pydantic.types import condecimal
from decimal import Decimal
from pydantic_core import PydanticCustomError


class DespesaCreate(BaseModel):
    IdCategoria: PositiveInt
    Descricao: str
    DiaCobranca: conint(ge=1, le=31)
    Valor: condecimal(max_digits=12, decimal_places=2, ge=Decimal("0"))

    @field_validator("Descricao")
    @classmethod
    def _descricao(cls, v: str) -> str:
        if not v.strip():
            raise PydanticCustomError("Descrição obrigatória", "A descrição é obrigatória.")
        if len(v) > 150:
            raise PydanticCustomError("Máximo de caracteres", "A descrição deve ter no máximo 150 caracteres.")
        return v
    
class DespesaUpdate(DespesaCreate):
    id: PositiveInt

class DespesaOut(BaseModel):
    id: int
    IdCategoria: int
    Descricao: str
    DiaCobranca: int
    Valor: Decimal
    CategoriaDescricao: str | None = None

    model_config = ConfigDict(from_attributes=True)