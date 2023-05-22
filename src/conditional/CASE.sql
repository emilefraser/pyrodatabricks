-- Databricks notebook source
SELECT * FROM silver_olist.cliente

-- COMMAND ----------

-- CASE WHEN, ELSE

SELECT *,
       CASE 
         WHEN descUF = 'SP' THEN 'paulista' 
         WHEN descUF = 'RJ' THEN 'fluminense' 
         WHEN descUF = 'PR' THEN 'paranaense'
         ELSE 'outros'
       END AS descNacionalidade 
FROM silver_olist.cliente

-- leia-se: caso na coluna descUF a sigla for 'SP', 'RJ' ou 'PR', crie uma nova coluna com nome descNacionalidade e atribuia o valor de 'paulista', 'fluminense' e 'paranaense', respecitivamente, do contrario atribuia 'outros'

-- COMMAND ----------

-- LIKE

SELECT *,
       CASE 
         WHEN descUF = 'SP' THEN 'paulista' 
         WHEN descUF = 'RJ' THEN 'fluminense' 
         WHEN descUF = 'PR' THEN 'paranaense'
         ELSE 'outros'
       END AS descNacionalidade,
       
-- leia-se: caso na coluna descUF a sigla for 'SP', 'RJ' ou 'PR', crie uma nova coluna com nome descNacionalidade e atribuia o valor de 'paulista', 'fluminense' e 'paranaense', respecitivamente, do contrario atribuia 'outros'
       
       CASE
         WHEN descCidade LIKE '%sao%' THEN 'Tem SÃO no nome' 
         ELSE 'Não tem SÃO no nome'
       END AS TemSao,
       
 -- leia-se: caso na coluna descCidade tenha no valor em alguma posição a string 'sao' crie uma coluna com nome TemSao e atribuia o valor de 'Tem SÃO no nome' se houver 'sao', e 'Não tem SÃO no nome' caso não haja 'sao'
       
       CASE 
         WHEN descUF in ('SP', 'RJ', 'MG', 'ES') THEN 'Sudeste' 
       END AS descRegiao 
       
-- leia-se: caso na coluna descUF tenha os valores 'SP', 'RJ', 'MG', 'ES' crie uma coluna com nome descRegiao e atribua o valor 'Sudeste'
       
FROM silver_olist.cliente


