CREATE OR REPLACE PROCEDURE refined.tabela_7()
BEGIN
CREATE OR REPLACE TABLE refined.tabela_7 AS 
WITH table_regex AS(
SELECT
 *,
 REGEXP_CONTAINS(description,r'\bBoticário|Boticario\b') as filter1,
 REGEXP_CONTAINS(name,r'\bBoticário|Boticario\b') as filter2,
FROM `refined.tabela_6`
)
SELECT * except(filter1, filter2) from table_regex
WHERE table_regex.filter1 = true or table_regex.filter2 = true;
END
