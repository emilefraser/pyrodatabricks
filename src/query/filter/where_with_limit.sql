-- Databricks notebook source
SELECT
  *
FROM
  silver_olist.pedido
WHERE
  descSituacao = 'shipped'
  AND YEAR(dtPedido) = '2018' 
LIMIT 100