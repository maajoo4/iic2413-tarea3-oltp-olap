SELECT 
    a.pais_origen,
    COUNT(r.id_reproduccion) AS cantidad_reproducciones,
    SUM(r.tiempo) AS tiempo_total,
    AVG(c.duracion) AS duracion_promedio
FROM fact_reproducciones r
JOIN dim_cancion c 
    ON r.id_cancion = c.id_cancion
JOIN dim_artista a 
    ON r.id_artista = a.id_artista
GROUP BY a.pais_origen
ORDER BY tiempo_total DESC;