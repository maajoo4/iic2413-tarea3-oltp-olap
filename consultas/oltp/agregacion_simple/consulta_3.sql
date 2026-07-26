-- SELECT 1 JOIN baja selectividad con agregacion 
-- Beneficia OLAP

SELECT 
    u.plan,
    COUNT(r.id_reproduccion) AS cantidad_reproducciones,
    AVG(r.tiempo) AS tiempo_promedio
FROM Reproducciones r
JOIN Usuarios u ON r.id_usuario = u.id_usuario
GROUP BY u.plan
ORDER BY cantidad_reproducciones DESC;

-- Como son las reproducciones segun plan 