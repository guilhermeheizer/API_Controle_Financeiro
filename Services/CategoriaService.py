from Repositories.CategoriaRepository import CategoriaRepository
from sqlalchemy.orm import Session
from DTOs.CategoriaDTO import CategoriaCreate, CategoriaUpdate, CategoriaOut
from typing import Optional, List
from Entities.models import Categoria


class CategoriaService:
    def __init__(self, repo: CategoriaRepository):
        self.repo = repo

    def create(self, db: Session, categoriaCreate: CategoriaCreate, idUsuario: int) -> Optional[CategoriaOut]:
        entity = Categoria(**categoriaCreate.model_dump(), IdUsuario=idUsuario)
        # Ler categoria por descricao para evitar duplicidade
        categoria_existente = self.repo.get_by_descricao(db, categoriaCreate.IdTipoCategoria, categoriaCreate.Descricao)
        if categoria_existente:
            raise ValueError("Categoria com essa descrição já existe.")

        categoriaCriada = self.repo.create(db, entity)
        if not categoriaCriada:
            raise ValueError("Erro ao criar a categoria.")
        
        dto = CategoriaOut.model_validate(categoriaCriada)
        return dto.model_copy(update={
            "TipoCategoriaDescricao": categoriaCriada.TipoCategoria.Descricao if categoriaCriada.TipoCategoria else None
        })
    
    def update(self, db: Session, categoriaUpdate: CategoriaUpdate) -> Optional[CategoriaOut]:
        if getattr(categoriaUpdate, 'id', None) is None:
            raise ValueError("O atributo Id é obrigatório.")
        
        categoria = self.repo.get(db, categoriaUpdate.id)
        if not categoria:
            raise ValueError(f"Categoria com id {categoriaUpdate.id} não encontrada ou excluída.")
        
        # Ler categoria por descricao para evitar duplicidade
        quant = self.repo.get_by_descricao_contar(db, categoriaUpdate.IdTipoCategoria, categoriaUpdate.Descricao)
        if quant > 1:
            raise ValueError("Categoria com essa descrição já existe.")
            
        entity = Categoria(**categoriaUpdate.model_dump())
        categoriaAlterada = self.repo.update(db, entity)
        if not categoriaAlterada:
            raise ValueError(f"Categoria com id {categoriaUpdate.id} não encontrada.")
        
        dto = CategoriaOut.model_validate(categoriaAlterada)
        return dto.model_copy(update={
            "TipoCategoriaDescricao": categoriaAlterada.TipoCategoria.Descricao if categoriaAlterada.TipoCategoria else None
        })
    
    def delete(self, db: Session, id_: int) -> bool:
        categoria = self.repo.get(db, id_)
        if not categoria:
            raise ValueError(f"Categoria com id {id_} não encontrada ou excluída.")
        
        if categoria.Excluido:
            raise ValueError(f"Categoria com id {id_} já foi excluída.")
        
        return self.repo.delete(db, categoria)

    def get(self, db: Session, id_: int) -> Optional[CategoriaOut]:
        categoria = self.repo.get(db, id_)
        if not categoria:
            raise ValueError(f"Categoria com id {id_} não encontrada ou excluída.")
        
        dto = CategoriaOut.model_validate(categoria)
        return dto.model_copy(update={
            "TipoCategoriaDescricao": categoria.TipoCategoria.Descricao if categoria.TipoCategoria else None
        })
    
    def get_all(self, db: Session, idUsuario: int, idTipoCategoria: Optional[int]) -> List[CategoriaOut]:
        categorias = self.repo.get_all(db, idUsuario, idTipoCategoria)
        return [
            CategoriaOut(
                id=c.id,
                IdTipoCategoria=c.IdTipoCategoria,
                Descricao=c.Descricao,
                TipoCategoriaDescricao=c.TipoCategoria.Descricao,
            )
            for c in categorias
        ]
    
    def usuario_has_categoria(self, db: Session, id_: int, idUsuario: int) -> bool:
        return self.repo.usuario_has_categoria(db, id_, idUsuario)