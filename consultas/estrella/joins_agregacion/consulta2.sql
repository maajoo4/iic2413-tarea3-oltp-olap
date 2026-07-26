SELECT 
    u.pais,
    COUNT(DISTINCT u.id_usuario) AS cantidad_usuarios,
    COUNT(r.id_reproduccion) AS cantidad_reproducciones,
    SUM(r.tiempo) AS tiempo_total,
    AVG(r.tiempo) AS promedio_tiempo
FROM fact_reproducciones r
JOIN dim_usuario u 
    ON r.id_usuario = u.id_usuario
JOIN dim_cancion c 
    ON r.id_cancion = c.id_cancion
JOIN dim_artista a 
    ON r.id_artista = a.id_artista
WHERE u.plan = 'free'
GROUP BY u.pais
ORDER BY tiempo_total DESC;