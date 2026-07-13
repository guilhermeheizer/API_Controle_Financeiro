SELECT id, "Descricao"
	FROM public."TipoCategoria";

INSERT INTO public."TipoCategoria"(
	id, "Descricao")
	VALUES (0, 'Saída');

INSERT INTO public."TipoCategoria"(
	id, "Descricao")
	VALUES (?, ?);

DELETE FROM public."Categoria"
	WHERE 1=1

UPDATE public."TipoCategoria"
	SET id=?, "Descricao"=?
	WHERE <condition>;

select *
From public."Categoria";

select *
From public."Usuario";

select * --sum("Valor")
From public."Despesa"
where "Excluido" = False;

select * --sum("Valor")
From public."Transacao"
where "Excluido" = False;

-- Grafico
-- get_quantidade_entradas:
SELECT COUNT(*)
FROM "Transacao" t
JOIN "Categoria" c ON c.id = t."IdCategoria"
WHERE c."IdTipoCategoria" = 1
  AND t."Excluido" = false
  AND EXTRACT(YEAR FROM t."Data") = 2026;

-- get_quantidade_saidas
SELECT 
    COUNT(t.id) AS total
FROM 
    "Transacao" t
JOIN 
    "Categoria" c ON c.id = t."IdCategoria"
WHERE 
    t."Excluido" = FALSE
    AND (
        c."IdTipoCategoria" = 2
        OR t."IdDespesa" IS NOT NULL
    )
    AND EXTRACT(YEAR FROM t."Data") = 2026;

-- get_despesa_mensal
SELECT 
    COALESCE(SUM(d."Valor"), 0) AS total
FROM 
    "Despesa" d
WHERE 
    d."Excluido" = FALSE;

-- get_entradas_saidas_por_mes
SELECT
    EXTRACT(MONTH FROM t."Data") AS mes_num,
    SUM(
        CASE 
            WHEN c.id = 1 THEN t."Valor"
            ELSE 0
        END
    ) AS entradas,
    SUM(
        CASE 
            WHEN (c.id = 2 OR t."IdDespesa" IS NOT NULL) THEN t."Valor"
            ELSE 0
        END
    ) AS saídas
FROM
    "Transacao" t
LEFT JOIN
    "Categoria" c ON t."IdCategoria" = c.id
WHERE
    t."Excluido" = FALSE
    AND EXTRACT(YEAR FROM t."Data") = 2026
GROUP BY
    mes_num
ORDER BY
    mes_num;

-- get_gastos_por_mes
SELECT
    EXTRACT(MONTH FROM t."Data") AS mes_num,
    SUM(t."Valor") AS valor
FROM
    "Transacao" t
LEFT JOIN
    "Categoria" c ON t."IdCategoria" = c.id
WHERE
    t."Excluido" = FALSE
    AND EXTRACT(YEAR FROM t."Data") = 2026
    AND (
        c."IdTipoCategoria" = 2
        OR t."IdDespesa" IS NOT NULL
    )
GROUP BY
    mes_num
ORDER BY
    mes_num;

-- get_gastos_por_categoria
SELECT
    COALESCE(ct."Descricao", cd."Descricao") AS categoria,
    SUM(t."Valor") AS valor
FROM
    "Transacao" t
LEFT JOIN
    "Categoria" ct ON t."IdCategoria" = ct.id
LEFT JOIN
    "Despesa" d ON t."IdDespesa" = d.id
LEFT JOIN
    "Categoria" cd ON d."IdCategoria" = cd.id
WHERE
    t."Excluido" = FALSE
    AND (
        ct."IdTipoCategoria" = 2
        OR t."IdDespesa" IS NOT NULL
    )
    AND EXTRACT(YEAR FROM t."Data") = 2026
GROUP BY
    COALESCE(ct."Descricao", cd."Descricao")
ORDER BY
    SUM(t."Valor") DESC;
