-- Databricks notebook source
-- DBTITLE 1,COUNT:
-- COUNT

SELECT COUNT(*) AS NumeroLinhasNaoNulas -- linhas não nulas
FROM silver_olist.cliente 

-- conta quantas linhas não nulas existes na tabela 'cliente'

-- COMMAND ----------

SELECT 
  COUNT(*) AS NumeroLinhasNaoNulas, -- linhas não nulas
  COUNT(idCliente) AS NumeroCLientesNaoNulos
FROM silver_olist.cliente 

-- conta quantas linhas existes na tabela 'cliente'

-- COMMAND ----------

-- COUNT DISTICT

SELECT 
  COUNT(*) AS NumeroLinhasNaoNulas, -- linhas não nulas
  COUNT(idCliente) AS NumeroCLientesNaoNulos, -- clientes não nulos
  COUNT(DISTINCT idCliente) AS NumeroClientesNaoNulos -- clientes distintos
FROM silver_olist.cliente 

-- COMMAND ----------

SELECT 
  COUNT(*) AS NumeroLinhasNaoNulas, -- linhas não nulas
  COUNT(idCliente) AS NumeroCLientesNaoNulos, -- clientes não nulos
  COUNT(DISTINCT idCliente) AS NumeroClientesDistintos,  -- compras distintas
  COUNT(DISTINCT idClienteUnico) AS NumeroClienteUnicoDistinto -- clientes distindos
FROM silver_olist.cliente 

-- COMMAND ----------

-- DBTITLE 1,WHERE:
SELECT COUNT(*) AS qtdLinhas,
       COUNT(distinct idClienteUnico) AS qtdClientes
FROM silver_olist.cliente
WHERE descCidade IN ('curitiba','presidente prudente')

-- COMMAND ----------

SELECT * FROM silver_olist.item_pedido

-- COMMAND ----------

-- DBTITLE 1,AVG (Média):
-- AVG (Média)

SELECT 
      AVG(vlPreco) AS PrecoMedioDosProdutos, -- média de preço dos produtos
      AVG(vlFrete) AS PrecoMedioDosFretes -- média dos fretes
FROM silver_olist.item_pedido

-- COMMAND ----------

-- DBTITLE 1,MAX (Valor máximo):
-- MAX (Máximo)

SELECT 
      MAX(vlPreco) AS PrecoMaisCaro, -- maior valor de preço dos produtos
      MAX(vlFrete) AS FreteMaisCaro -- maior valor de frete
FROM silver_olist.item_pedido

-- COMMAND ----------

-- DBTITLE 1,MIN (Valor mínimo):
-- MIN (Mínimo)

SELECT 
      MIN(vlPreco) AS PrecoMaisBaixo, -- maior valor de preço dos produtos
      MIN(vlFrete) AS FreteMaisBaixo -- maior valor de frete
FROM silver_olist.item_pedido

-- COMMAND ----------

-- DBTITLE 1,PERCENTIL (Mediana):
-- percentile 0,5 (mediana)

SELECT 
      ROUND(PERCENTILE(vlPreco, 0.5),2) AS PrecoMediana, -- mediana (valor central) dos preços arrendodado em 2 casas decimais
      ROUND(PERCENTILE(vlFrete, 0.5),2) AS FreteMediana -- mediana (valor central) dos fretes arrendodado em 2 casas decimais
FROM silver_olist.item_pedido
