SELECT 
    a.nombre,
    a.pais_origen,
    AVG(c.duracion) AS duracion_promedio
FROM dim_cancion c
JOIN dim_artista a 
    ON c.id_artista = a.id_artista
GROUP BY a.id_artista, a.nombre, a.pais_origen
ORDER BY duracion_promedio DESC;
