from fastapi import APIRouter, Depends, HTTPException, status, Query
from DTOs.GraficoDTO import DataJson, Dashboard, GraficoGastosPorCategoria, GraficoGastosPorMes, GraficoQuantidadeDespesasPorCategoria, Graficos, GraficoEntradasESaidasPorMes
from Services.DespesaService import DespesaService
from Services.TransacaoService import TransacaoService
from Repositories.DespesaRepository import DespesaRepository
from Repositories.TransacaoRepository import TransacaoRepository
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from Utilities.dependecies import get_current_clains
from datetime import date

router = APIRouter(prefix="/grafico", tags=["Grafico"])

_serviceDespesa = DespesaService(DespesaRepository())
_serviceTransacao = TransacaoService(TransacaoRepository())

@router.get("/", response_model=DataJson, status_code=status.HTTP_200_OK)
def get_dados_grafico(db: Session = Depends(get_db), 
                      clains: dict = Depends(get_current_clains),
                      datainicio: date = Query(date(date.today().year, 1, 1), description="Data de início no formato YYYY-MM-DD"),
                      datafim: date = Query(date(date.today().year, 12, 31), description="Data de fim no formato YYYY-MM-DD")):
    user_id = clains.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário ausente no token")

    user_id = int(user_id)

    try:
        resumo = _serviceTransacao.get_resumo(db, datainicio, datafim, user_id)
        gastos_por_categoria = _serviceTransacao.get_gastos_por_categoria(db, datainicio, datafim, user_id)
        gastos_por_mes = _serviceTransacao.get_gastos_por_mes(db, datainicio, datafim, user_id)
        quantidade_despesas_mensais_por_categoria = _serviceDespesa.get_quantidade_despesas_por_categoria(db, user_id)
        entradas_e_saida_mes = _serviceTransacao.get_entradas_saida_por_mes(db, datainicio, datafim, user_id)

        dashboard = Dashboard(
            resumo = resumo,
            graficos = Graficos(
                entradas_e_saidas_por_mes=GraficoEntradasESaidasPorMes(
                    titulo="Entradas e Saídas por Mês",
                    dados=entradas_e_saida_mes
                ),
                gastos_por_categoria=GraficoGastosPorCategoria(
                    titulo="Gastos por Categoria",
                    dados=gastos_por_categoria
                ),
                gastos_por_mes=GraficoGastosPorMes(
                    titulo="Gastos por Mês",
                    dados=gastos_por_mes
                ),
                quantidade_despesas_mensais_por_categoria=GraficoQuantidadeDespesasPorCategoria(
                    titulo="Quantidade de Despesas Mensais por Categoria",
                    dados=quantidade_despesas_mensais_por_categoria
                ),
            )
        )
        return DataJson(dashboard=dashboard)
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor: " + str(e))