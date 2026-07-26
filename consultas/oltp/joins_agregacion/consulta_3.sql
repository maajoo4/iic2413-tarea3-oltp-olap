-- SELECT 2 o 3 JOINS  SELECTIVIDAD BAJA SIN JOINS CON AGREGACION 
-- Como son las reproducciones segun el pais de origen del artista 
SELECT a.pais_origen,
    COUNT(r.id_reproduccion) AS cantidad_reproducciones,
    SUM(r.tiempo) AS tiempo_total,
    AVG(c.duracion) AS duracion_promedio
FROM Reproducciones r
JOIN Canciones c ON r.id_cancion = c.id_cancion
JOIN Artistas a ON c.id_artista = a.id_artista
GROUP BY a.pais_origen
ORDER BY tiempo_total DESC;