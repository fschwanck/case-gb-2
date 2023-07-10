CREATE OR REPLACE PROCEDURE refined.tabela_4()
BEGIN
CREATE TABLE IF NOT EXISTS `fschwanck-case-gb-2`.`refined`.`tabela_4`(
    LINHA STRING,
    ANO STRING,
    MES STRING,
    QTD_VENDA INTEGER

);
TRUNCATE TABLE `fschwanck-case-gb-2`.`refined`.`tabela_4`;
INSERT `fschwanck-case-gb-2`.`refined`.`tabela_4` (LINHA, ANO, MES, QTD_VENDA)
SELECT 
  LINHA,
  format_date('%Y', DATA_VENDA) AS ANO,
  format_date('%m', DATA_VENDA) AS MES,
  SUM(QTD_VENDA) AS QTD_VENDA
FROM `fschwanck-case-gb-2`.`raw`.`tabela_base`
GROUP BY LINHA, ANO, MES;
END
