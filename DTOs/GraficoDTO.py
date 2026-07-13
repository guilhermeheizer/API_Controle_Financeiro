from pydantic import BaseModel, Field
from typing import List


class GastoCategoria(BaseModel):
    categoria: str
    valor: float

class GastoMes(BaseModel):
    mes: str
    valor: float

class QuantidadeDespesaCategoria(BaseModel):
    categoria: str
    quantidade: int

class EntradasSaidaMes(BaseModel):
    mes: str
    entrada: float
    saida: float

class GraficoGastosPorCategoria(BaseModel):
    titulo: str
    dados: List[GastoCategoria] = Field(default_factory=list)

class GraficoGastosPorMes(BaseModel):
    titulo: str
    dados: List[GastoMes] = Field(default_factory=list)

class GraficoQuantidadeDespesasPorCategoria(BaseModel):
    titulo: str
    dados: List[QuantidadeDespesaCategoria] = Field(default_factory=list)

class GraficoEntradasESaidasPorMes(BaseModel):
    titulo: str
    dados: List[EntradasSaidaMes] = Field(default_factory=list)

class Graficos(BaseModel):
    entradas_e_saidas_por_mes: GraficoEntradasESaidasPorMes
    gastos_por_categoria: GraficoGastosPorCategoria
    gastos_por_mes: GraficoGastosPorMes
    quantidade_despesas_mensais_por_categoria: GraficoQuantidadeDespesasPorCategoria

class Resumo(BaseModel):
    quantidade_entradas: int
    quantidade_saidas: int
    despesa_mensal: float

class Dashboard(BaseModel):
    graficos: Graficos
    resumo: Resumo

class DataJson(BaseModel):
    dashboard: Dashboard