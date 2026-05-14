from pydantic import BaseModel, ConfigDict, PositiveInt, field_validator, conint
from typing_extensions import Annotated
from  pydantic.types import StringConstraints, condecimal
from decimal import Decimal


class DespesaCreate(BaseModel):
    IdCategoria: PositiveInt
    Descricao: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]
    DiaCobranca: conint(ge=1, le=31)
    Valor: condecimal(max_digits=12, decimal_places=2, ge=Decimal("0"))

    @field_validator("Descricao")
    @classmethod
    def _descricao(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("A descrição é obrigatória.")
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