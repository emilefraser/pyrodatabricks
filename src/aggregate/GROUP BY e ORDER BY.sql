-- Databricks notebook source
-- DBTITLE 1,GROUP BY:
-- GROUP BY:

SELECT
    descUF, 
    count(*)
FROM silver_olist.cliente
GROUP BY descUF 

-- leia-se: agrupe as linhas pela informações da coluna descUF (estados) e conte o total

-- COMMAND ----------

SELECT
    descUF, 
    count(DISTINCT idClienteUnico)
FROM silver_olist.cliente
GROUP BY descUF 

-- leia-se: agrupe as linhas pela informações da coluna descUF (estados) e conte o total de clientes unicos por estado

-- COMMAND ----------

-- DBTITLE 1,ORDER BY
-- ORDER BY

SELECT
    descUF, 
    count(DISTINCT idClienteUnico) AS qtdClientes
FROM silver_olist.cliente
GROUP BY descUF 
ORDER BY descUF

-- leia-se: agrupe as linhas pela informações da coluna descUF (estados) e conte o total de clientes unicos por estado em order alfabética

-- COMMAND ----------

-- Primeira forma:

SELECT
    descUF, 
    count(DISTINCT idClienteUnico) AS qtdClientes
FROM silver_olist.cliente
GROUP BY descUF 
ORDER BY 2

-- COMMAND ----------

-- Segunda forma:

SELECT
    descUF, 
    count(DISTINCT idClienteUnico) AS qtdClientes
FROM silver_olist.cliente
GROUP BY descUF 
ORDER BY qtdClientes

-- COMMAND ----------

-- Terceira forma:

SELECT
    descUF, 
    count(DISTINCT idClienteUnico) AS qtdClientes
FROM silver_olist.cliente
GROUP BY descUF 
ORDER BY count(DISTINCT idClienteUnico)

-- COMMAND ----------

-- Ordenando de forma descrescente:

SELECT
    descUF, 
    count(DISTINCT idClienteUnico) AS qtdClientes
FROM silver_olist.cliente
GROUP BY descUF 
ORDER BY qtdClientes DESC

-- COMMAND ----------

-- Vendo apenas o estado com mais clientes

SELECT
    descUF, 
    count(DISTINCT idClienteUnico) AS qtdClientes
FROM silver_olist.cliente
GROUP BY descUF 
ORDER BY qtdClientes DESC
LIMIT 1
