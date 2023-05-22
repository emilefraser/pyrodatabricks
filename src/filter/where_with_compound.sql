SELECT
  *
FROM
  silver_olist.pedido
WHERE
  descSituacao IN ('shipped', 'canceled') -- o IN pode ser usado no lugar do OR
  AND year(dtPedido) = '2018