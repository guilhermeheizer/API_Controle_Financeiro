SELECT id, "Descricao"
	FROM public."TipoCategoria";

INSERT INTO public."TipoCategoria"(
	id, "Descricao")
	VALUES (0, 'Saída');

INSERT INTO public."TipoCategoria"(
	id, "Descricao")
	VALUES (?, ?);

DELETE FROM public."TipoCategoria"
	WHERE 1=1

UPDATE public."TipoCategoria"
	SET id=?, "Descricao"=?
	WHERE <condition>;

select *
From public."Categoria";

select *
From public."Despesa";

UPDATE "Categoria" 
	SET "IdTipoCategoria"=(IdTipoCategoria), 
	"Descricao"=(Descricao) 
	WHERE "Categoria".id = 7
	
	\n[parameters: {'IdTipoCategoria': 2, 'Descricao': 'Vendas da padaria', 'Categoria_id': 7
	