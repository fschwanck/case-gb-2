
CREATE TABLE IF NOT EXISTS `fschwanck-case-gb-2`.`refined`.`tabela_2`(
    MARCA STRING,
    LINHA STRING,
    QTD_VENDA INTEGER

);
TRUNCATE TABLE `fschwanck-case-gb-2`.`refined`.`tabela_2`;
INSERT `fschwanck-case-gb-2`.`refined`.`tabela_2` (MARCA, LINHA, QTD_VENDA)
SELECT 
  MARCA,
  LINHA,
  SUM(QTD_VENDA) AS QTD_VENDA
FROM `fschwanck-case-gb-2`.`raw`.`tabela_base`
GROUP BY MARCA, LINHA
