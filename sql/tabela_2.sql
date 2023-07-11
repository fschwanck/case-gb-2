CREATE OR REPLACE PROCEDURE refined.tabela_2()
BEGIN
CREATE OR REPLACE TABLE `fschwanck-case-gb-2`.`refined`.`tabela_2` as
SELECT 
  MARCA,
  LINHA,
  SUM(QTD_VENDA) AS QTD_VENDA
FROM `fschwanck-case-gb-2`.`raw`.`tabela_base`
GROUP BY MARCA, LINHA;
END