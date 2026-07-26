-- SELECT 1 JOINS  SELECTIVIDAD BAJA CON AGREGACION
--  Reproduccion mas larga de cada cancion
-- Beneficia OLAP

SELECT 
    c.id_cancion,
    MAX(r.tiempo)
FROM Reproducciones r
JOIN Canciones c 
    ON r.id_cancion = c.id_cancion
GROUP BY c.id_cancion;