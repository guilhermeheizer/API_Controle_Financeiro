from pydantic import BaseModel, ConfigDict, PositiveInt, StringConstraints, field_validator, model_validator, condecimal
from typing import Optional
from typing_extensions import Annotated
from  pydantic.types import StringConstraints
from decimal import Decimal
from datetime import datetime


class TransacaoCreate(BaseModel):
    IdCategoria: Optional[PositiveInt] | None= None
    IdDespesa: Optional[PositiveInt] | None = None
    Descricao: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]
    Valor: condecimal(max_digits=12, decimal_places=2, ge=Decimal("0"))

    @field_validator("Descricao")
    @classmethod
    def _descricao(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("A descrição é obrigatória.")
        return v

    @field_validator("Valor")
    @classmethod
    def _valor(cls, v: Decimal) -> Decimal:
        if v < Decimal("0"):
            raise ValueError("O valor não pode ser negativo.")
        return v
    
    @model_validator(mode="after")
    def _xor_categoria_despesa(self) -> "TransacaoCreate":
        if(self.IdCategoria is None) == (self.IdDespesa is None):
            raise ValueError("A transação deve estar associada a uma categoria ou a uma despesa, mas não ambas.")
        return self
    
class TransacaoUpdate(TransacaoCreate):
    id: PositiveInt

class TransacaoOut(BaseModel):
    id: int
    IdCategoria: int | None = None
    IdDespesa: int | None = None
    Descricao: str
    Valor: Decimal
    Data: datetime  
    CategoriaDescricao: str | None = None
    DespesaDescricao: str | None = None

    model_config = ConfigDict(from_attributes=True)