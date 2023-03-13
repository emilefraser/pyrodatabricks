SELECT
  *,
  vlPreco + vlFrete AS vlTotal,
  vlFrete / (vlPreco + vlFrete) AS pctFrete,
  CASE
    WHEN vlFrete / (vlPreco + vlFrete) <= 0.10 THEN '< 10%'
    WHEN vlFrete / (vlPreco + vlFrete) <= 0.25 THEN '10% a 25%'
    WHEN vlFrete / (vlPreco + vlFrete) <= 0.50 THEN '25% a 50%'
    ELSE '+50%'
  END AS faixaFrete
  FROM
  silver_olist.item_pedido
