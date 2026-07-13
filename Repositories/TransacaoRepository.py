from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, func, or_, extract, case
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import Optional, List
from Entities.models import Transacao, Categoria, Despesa
from datetime import date, datetime, time


nomes_meses = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }

class TransacaoRepository:

    def create(self, db: Session, transacao: Transacao) -> Transacao:
        try:
            db.add(transacao)
            db.commit()
            db.refresh(transacao)
            return transacao
        except IntegrityError:
            db.rollback()
            raise ValueError("Erro ao criar transação.")
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError("Erro ao salvar transação." + str(e))

    def update(self, db: Session, transacao: Transacao) -> Optional[Transacao]:
        try:
            merged = db.merge(transacao)
            db.commit()
            db.refresh(merged)
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError("Erro ao atualizar transação." + str(e))
        return merged
    
    def delete(self, db: Session, id_: int) -> bool:
        try:
            transacao = db.get(Transacao, id_)
            if transacao is None:
                return False
            
            if not transacao.Excluido:
                transacao.Excluido = True
                db.merge(transacao)
                db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError("Erro ao excluir transação." + str(e))

    def get(self, db: Session, id_: int) -> Optional[Transacao]:
        try:
            stmt = select(Transacao).where(Transacao.id == id_, Transacao.Excluido.is_(False))
            return db.scalars(stmt).first()
        except SQLAlchemyError as e:
            raise ValueError("Erro ao buscar transação." + str(e))

    def get_all(self, db: Session, user_id: int) -> List[Transacao]:
        try:
            stmt = select(Transacao).where(Transacao.Excluido.is_(False), Transacao.IdUsuario == user_id).order_by(Transacao.Descricao)
        except SQLAlchemyError as e:
            raise ValueError("Erro ao listar transações." + str(e))
        return list(db.scalars(stmt))
    
    def get_quantidade_entradas(self, db: Session, datainicio: date, datafim: date, user_id: int) -> int:
        try:
            dataInicio_dt = datetime.combine(datainicio, time.min)
            dataFim_dt = datetime.combine(datafim, time.max)
            return(
                db.query(func.count(Transacao.id))
                .join(Categoria, Transacao.IdCategoria == Categoria.id)
                .filter(
                    Categoria.IdTipoCategoria == 1,
                    Transacao.Excluido.is_(False),
                    Transacao.Data.between(dataInicio_dt, dataFim_dt),
                    Transacao.IdUsuario == user_id
                )
                .scalar() or 0
            )
        except SQLAlchemyError as e:
            raise ValueError("Erro ao contar entradas: " + str(e))

    def get_quantidade_saidas(self, db: Session, datainicio: date, datafim: date, user_id: int) -> int:
        try:
            dataInicio_dt = datetime.combine(datainicio, time.min)
            dataFim_dt = datetime.combine(datafim, time.max)
            return (
                db.query(func.count(Transacao.id))
                .outerjoin(Categoria, Transacao.IdCategoria == Categoria.id)
                .filter(
                    Transacao.Excluido.is_(False),
                    Transacao.Data.between(dataInicio_dt, dataFim_dt),
                    or_(
                        Categoria.IdTipoCategoria == 2,
                        Transacao.IdDespesa.isnot(None)
                    ),
                    Transacao.IdUsuario == user_id
                )
                .scalar() or 0
            )
        except SQLAlchemyError as e:
            raise ValueError("Erro ao contar saídas: " + str(e))

    def get_quantidade_despesas(self, db: Session, datainicio: date, datafim: date,) -> int:
        try:
            dataInicio_dt = datetime.combine(datainicio, time.min)
            dataFim_dt = datetime.combine(datafim, time.max)
            return (
                db.query(func.count(Transacao.id))
                .join(Categoria, Transacao.IdCategoria == Categoria.id)
                .filter(
                    Transacao.Excluido == False,
                    or_(
                        Categoria.IdTipoCategoria == 2,
                        Categoria.id.isnot (None)
                    ),
                    Transacao.Data.between(dataInicio_dt, dataFim_dt)
                )
                .scalar() or 0
            )
        except SQLAlchemyError as e:
            raise ValueError("Erro ao contar despesas: " + str(e))

    def get_despesa_mensal(self, db: Session, user_id: int) -> float:
        try:
            return(
                db.query(func.coalesce(func.sum(Despesa.Valor), 0))
                .filter(
                    Despesa.Excluido == False,
                    Despesa.IdUsuario == user_id
                    )
                .scalar()
            )

        except SQLAlchemyError as e:
            raise ValueError("Erro ao calcular despesa mensal: " + str(e))

    def get_entradas_saidas_por_mes(self, db: Session, datainicio: date, datafim: date, user_id: int):
        dataInicio_dt = datetime.combine(datainicio, time.min)
        dataFim_dt = datetime.combine(datafim, time.max)
        try:
            query = (
                db.query(
                    extract('month', Transacao.Data).label('mes_num'),
                    func.sum(
                        case(
                            (Categoria.IdTipoCategoria == 1, Transacao.Valor),
                            else_=0
                        )
                    ).label('entradas'),
                    func.sum(
                        case(
                            (
                            or_ (
                                Categoria.IdTipoCategoria == 2,
                                Transacao.IdDespesa.isnot(None)
                            ),
                            Transacao.Valor
                            ),
                            else_=0
                        )
                    ).label('saidas')
                    ).outerjoin(Categoria, Transacao.IdCategoria == Categoria.id)
                    .filter(Transacao.Excluido == False,
                            Transacao.Data.between(dataInicio_dt, dataFim_dt),
                            Transacao.IdUsuario == user_id)
                    .group_by('mes_num')
                    .order_by('mes_num')
            )

            resultados = query.all()

            lista = [
                {
                    "mes": nomes_meses.get(int(r.mes_num), str(r.mes_num)),
                    "entrada": float(r.entradas or 0.0),
                    "saida": float(r.saidas or 0.0)
                }
                for r in resultados
            ]

            return lista
        except SQLAlchemyError as e:
            raise ValueError("Erro ao calcular entradas e saídas por mês: " + str(e))

    def get_gastos_por_mes(self, db: Session, datainicio: date, datafim: date, user_id: int):
        dataInicio_dt = datetime.combine(datainicio, time.min)
        dataFim_dt = datetime.combine(datafim, time.max)
        try:
            query = (
                db.query(
                    extract('month', Transacao.Data).label('mes_num'),
                    func.sum(Transacao.Valor).label('valor')
                )
                .outerjoin(Categoria, Transacao.IdCategoria == Categoria.id)
                .filter(
                    Transacao.Excluido == False,
                    Transacao.Data.between(dataInicio_dt, dataFim_dt),
                    ((Categoria.IdTipoCategoria == 2) | (Transacao.IdDespesa.isnot(None))),
                    Transacao.IdUsuario == user_id
                )
                .group_by('mes_num')
                .order_by('mes_num')
            )

            resultados = query.all()

            gastosPorMes = [
                {
                    "mes": nomes_meses.get(int(r.mes_num), str(r.mes_num)),
                    "valor": float(r.valor or 0.0)
                }
                for r in resultados
            ]

            return gastosPorMes
        except SQLAlchemyError as e:
            raise ValueError("Erro ao calcular gastos por mês: " + str(e))
    
    def get_gastos_por_categoria(self, db: Session, datainicio: date, datafim: date, user_id: int):
        try:
            dataInicio_dt = datetime.combine(datainicio, time.min)
            dataFim_dt = datetime.combine(datafim, time.max)
            CategoriaTransacao = aliased(Categoria)
            CategoriaDespesa = aliased(Categoria)

            query = (
                db.query(
                    func.coalesce(CategoriaTransacao.Descricao, CategoriaDespesa.Descricao).label('categoria'),
                    func.sum(Transacao.Valor).label('valor')
                )
                .outerjoin(CategoriaTransacao, Transacao.IdCategoria == CategoriaTransacao.id)
                .outerjoin(Despesa, Transacao.IdDespesa == Despesa.id)
                .outerjoin(CategoriaDespesa, Despesa.IdCategoria == CategoriaDespesa.id)
                .filter(
                    Transacao.Excluido == False,
                    or_(
                        CategoriaTransacao.IdTipoCategoria == 2,
                        Transacao.IdDespesa.isnot(None)
                    ),
                    Transacao.Data.between(dataInicio_dt, dataFim_dt),
                    Transacao.IdUsuario == user_id
                )
                .group_by(func.coalesce(CategoriaTransacao.Descricao, CategoriaDespesa.Descricao))
                .order_by(func.sum(Transacao.Valor).desc())
            )

            resultados = query.all()

            return [
                {
                    "categoria": r.categoria,
                    "valor": float(r.valor or 0.0)
                }
                for r in resultados
            ]
        except SQLAlchemyError as e:
            raise ValueError("Erro ao calcular gastos por categoria: " + str(e))
        
    def usuario_has_transacao(self, db: Session, id_: int, idUsuario: int) -> bool:
        try:
            stmt = select(Transacao).where(Transacao.id == id_, Transacao.IdUsuario == idUsuario, Transacao.Excluido.is_(False))
            return db.scalars(stmt).first() is not None
        except SQLAlchemyError as e:
            raise RuntimeError("get: Erro ao buscar a transaco: " + str(e)) 