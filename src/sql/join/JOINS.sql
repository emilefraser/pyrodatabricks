-- Databricks notebook source
-- DBTITLE 1,LEFT JOIN: 
-- Tabela esquerda (left) como referência:

SELECT T1.idCliente,
        T2.descUF
        
FROM silver_olist.pedido AS T1 

LEFT JOIN silver_olist.cliente AS T2
ON T1.idCliente = T2.idCliente

-- COMMAND ----------

-- DBTITLE 1,RIGHT JOIN:
-- Tabela a direita (rigt) como referência:

SELECT T1.idPedido,
        T2.descUF
        
FROM silver_olist.pedido AS T1 

RIGHT JOIN silver_olist.cliente AS T2
ON T1.idCliente = T2.idCliente

-- COMMAND ----------

-- Não há tabela de referência, trás as correspondências:

SELECT T1.idPedido,
        T2.descUF
        
FROM silver_olist.pedido AS T1 

INNER JOIN silver_olist.cliente AS T2
ON T1.idCliente = T2.idCliente
