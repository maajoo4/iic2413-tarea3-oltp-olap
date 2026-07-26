SELECT 
    c.genero AS genero,
    COUNT(r.id_reproduccion) AS cantidad_reproducciones,
    COUNT(DISTINCT r.id_usuario) AS usuarios_activos,
    SUM(r.tiempo) AS tiempo_total,
    AVG(c.duracion) AS duracion_promedio
FROM fact_reproducciones r
JOIN dim_cancion c 
    ON r.id_cancion = c.id_cancion
JOIN dim_usuario u 
    ON r.id_usuario = u.id_usuario
GROUP BY c.genero
ORDER BY tiempo_total DESC;