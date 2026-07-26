-- SELECT 1 JOINS  SELECTIVIDAD BAJA CON AGREGACION
--  Cuales artistas tienen canciones con mayor duracion promedio 
-- Beneficia OLAP
SELECT 
    a.nombre,
    a.pais_origen,
    AVG(c.duracion) AS duracion_promedio
FROM Canciones c
JOIN Artistas a ON c.id_artista = a.id_artista
GROUP BY a.id_artista, a.nombre, a.pais_origen
ORDER BY duracion_promedio DESC;