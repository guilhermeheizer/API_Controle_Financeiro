from pydantic import BaseModel, ConfigDict


class TipoCategoriaDTO(BaseModel):
    id: int
    descricao: str

    model_config = ConfigDict(from_attributes=True)

class TipoCategoriaOut(BaseModel):
    id: int
    Descricao: str

    model_config = ConfigDict(from_attributes=True)    