SELECT * FROM suppliedProducts WHERE suppliedProducts.Dodavatel LIKE '%wortman%';


SELECT * FROM suppliedProducts JOIN suppliersCountry ON suppliedProducts.Dodavatel = suppliersCountry.Dodavel WHERE suppliersCountry._CZ_ano_ne not LIKE '%ne%' AND Poznámka LIKE '%obleč%';
--SELECT "suma", SUM(Množství_celkem) FROM suppliedProducts JOIN suppliersCountry ON suppliedProducts.Dodavatel = suppliersCountry.Dodavel WHERE suppliersCountry._CZ_ano_ne not LIKE '%ne%' AND Poznámka LIKE '%obleč%';
--SELECT * FROM suppliedProducts JOIN suppliersCountry ON suppliedProducts.Dodavatel = suppliersCountry.Dodavel WHERE suppliersCountry._CZ_ano_ne not LIKE '%ne%' AND Poznámka = "Oblečení - pánské - Lerros";
--SELECT DISTINCT Poznámka FROM suppliedProducts;



--SELECT * FROM suppliedProducts ORDER BY "Dodavatel";
--SELECT * FROM suppliedProducts JOIN suppliersCountry ON suppliedProducts.Dodavatel = suppliersCountry.Dodavel WHERE suppliersCountry._CZ_ano_ne not LIKE '%ne%' AND Typ_zbozi LIKE '%kabel%';
SELECT * FROM suppliedProducts as sp JOIN suppliersCountry as sc ON sp.Dodavatel LIKE '%' || sc.Dodavel || '%' WHERE sc._CZ_ano_ne not LIKE '%ne%';
--SELECT * FROM suppliedProducts WHERE Dodavatel like '%assa%';

SELECT * FROM ekokom_res ORDER BY PuvodCZ, Typ_zbozi, Dodavatel;