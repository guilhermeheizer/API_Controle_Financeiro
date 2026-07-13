from pydantic import BaseModel, ConfigDict, PositiveInt, field_validator, model_validator, condecimal
from typing import Optional
from decimal import Decimal
from datetime import datetime
from pydantic_core import PydanticCustomError


class TransacaoCreate(BaseModel):
    IdCategoria: Optional[PositiveInt] | None= None
    IdDespesa: Optional[PositiveInt] | None = None
    Descricao: str
    Valor: condecimal(max_digits=12, decimal_places=2, ge=Decimal("0"))

    @field_validator("Descricao")
    @classmethod
    def _descricao(cls, v: str) -> str:
        if not v.strip():
            raise PydanticCustomError("Descrição obrigatória", "A descrição é obrigatória.")
        if len(v) > 150:
            raise PydanticCustomError("Máximo de caracteres", "A descrição deve ter no máximo 150 caracteres.")
        return v

    @field_validator("Valor")
    @classmethod
    def _valor(cls, v: Decimal) -> Decimal:
        if v < Decimal("0"):
            raise PydanticCustomError("Valor inválido", "O valor não pode ser negativo.")
        return v
    
    @model_validator(mode="after")
    def _xor_categoria_despesa(self) -> "TransacaoCreate":
        if(self.IdCategoria is None) == (self.IdDespesa is None):
            raise PydanticCustomError("Categoria ou Despesa obrigatória", "A transação deve estar associada a uma categoria ou a uma despesa, mas não ambas.")
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