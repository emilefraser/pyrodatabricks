-- Databricks notebook source
-- DBTITLE 1,HAVING:
SELECT descUF,
       COUNT(idVendedor) AS qntVendedorUF
FROM silver_olist.vendedor
GROUP BY descUF
HAVING qntVendedorUF >= 100 -- filtro após a agregação 
ORDER BY qntVendedorUF DESC

-- COMMAND ----------

-- Utilizando WHERE antes da agregação (filtrando em COLUNA já existente)

SELECT descUF,
       COUNT(idVendedor) AS qntVendedorUF
FROM silver_olist.vendedor
WHERE descUF IN ('SP', 'RJ', 'MG', 'ES')
GROUP BY descUF
HAVING qntVendedorUF >= 100
ORDER BY qntVendedorUF DESC
