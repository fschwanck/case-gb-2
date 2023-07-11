CREATE OR REPLACE PROCEDURE refined.tabela_3()
BEGIN
CREATE OR REPLACE TABLE `fschwanck-case-gb-2`.`refined`.`tabela_3` as
SELECT 
  MARCA,
  format_date('%Y', DATA_VENDA) AS ANO,
  format_date('%m', DATA_VENDA) AS MES,
  SUM(QTD_VENDA) AS QTD_VENDA
FROM `fschwanck-case-gb-2`.`raw`.`tabela_base`
GROUP BY MARCA, ANO, MES;
END

