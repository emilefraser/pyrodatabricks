-- Databricks notebook source
-- DBTITLE 1,CTEs:
-- Exemplo 1: Lista de vendedores que estão no estado com mais clientes:

-- Passo 1: Descubra o estado com mais clientes:

-- SELECT descUF,
--        COUNT(DISTINCT idClienteUnico) AS QntdeClientes
-- FROM silver_olist.cliente
-- GROUP BY descUF
-- ORDER BY QntdeClientes DESC

-- Passo 2: Descubra a lista de vendedores:

-- SELECT idVendedor 
-- FROM silver_olist.vendedor
-- WHERE descUF = 'SP'

-- Passo 3: Faça a subquery com as devidas alterações:

SELECT idVendedor,
       descUF
FROM silver_olist.vendedor
WHERE descUF = (

 SELECT descUF
 FROM silver_olist.cliente

 GROUP BY descUF
 ORDER BY COUNT(DISTINCT idClienteUnico) DESC
 LIMIT 1
 
 )


-- COMMAND ----------

-- Exemplo 2: Lista de vendedores que estão nos 2 estados com mais clientes:

SELECT idVendedor,
        descUF
FROM silver_olist.vendedor
WHERE descUF IN ( -- IN: pois agora é uma lista de estados

 SELECT descUF
 FROM silver_olist.cliente

 GROUP BY descUF
 ORDER BY COUNT(DISTINCT idClienteUnico) DESC
 LIMIT 2
 
 )

-- COMMAND ----------

-- DBTITLE 1,Cláusula WITH:
-- Tabela temporária:

WITH tb_estados AS (

 SELECT descUF
 FROM silver_olist.cliente

 GROUP BY descUF
 ORDER BY COUNT(DISTINCT idClienteUnico) DESC
 LIMIT 2
 ),
 
tb_vendedores AS(
 
  SELECT idVendedor, descUF
  FROM silver_olist.vendedor
  WHERE descUF IN (SELECT descUF FROM tb_estados)
  )
  
SELECT * FROM tb_vendedores

-- COMMAND ----------

-- Nota média dos pedidos dos vendedores de cada estado:


WITH tb_pedido_nota AS (

  SELECT T1.idVendedor, T2.vlNota
  FROM silver_olist.item_pedido AS T1
  
  LEFT JOIN silver_olist.avaliacao_pedido AS T2
  ON T1.idPedido = T2.idPedido
),

tb_avg_vendedor AS (

  SELECT idVendedor,
         AVG(vlNota) as avgNotaVendedor
  FROM tb_pedido_nota
  GROUP BY idVendedor
),

tb_vendedor_estado AS (

  SELECT T1.*,
         T2.descUF
  FROM tb_avg_vendedor AS T1
  LEFT JOIN silver_olist.vendedor AS T2
  ON T1.idVendedor = T2.idVendedor

)

SELECT descUF,
       AVG(avgNotaVendedor) AS avgNotaEstado

FROM tb_vendedor_estado

GROUP BY descUF
ORDER BY avgNotaEstado DESC
