SELECT 
    u.plan,
    COUNT(r.id_reproduccion) AS cantidad_reproducciones,
    AVG(r.tiempo) AS tiempo_promedio
FROM fact_reproducciones r
JOIN dim_usuario u 
    ON r.id_usuario = u.id_usuario
GROUP BY u.plan
ORDER BY cantidad_reproducciones DESC;