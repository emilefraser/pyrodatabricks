-- Databricks notebook source
SELECT * from silver_olist.pedido
-- selecionando todas as colunas (*) da tabela silver_olist.pedido

-- COMMAND ----------

SELECT idPedido, descSituacao FROM silver_olist.pedido
-- selecionando as colunas idPedido e descSituacao da tabela silver_olist.pedido

-- COMMAND ----------

SELECT idPedido, descSituacao FROM silver_olist.pedido LIMIT 5
-- selecionando as 5 primeiras linhas da filtragem das colunas idPedido e descSituacao da tabela silver_olist.pedido

-- COMMAND ----------

SELECT *,
datediff(dtEstimativaEntrega, dtEntregue) AS qtdDiasPromessaEntrega
FROM silver_olist.pedido
LIMIT 5
-- selecionando as 5 primeiras linhas da tabela silver_olist.pedido e criando a coluna qtdDiasPromessaEntrega

-- COMMAND ----------


