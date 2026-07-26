-- SELECT 1 o 2 JOINS baja selectividad con agregacion 
-- Beneficia OLAP

-- Datos de reproduccion segun genero considerando reproducciones tiempo total y duracion promedio de canciones
SELECT 
    g.nombre AS genero,
    COUNT(r.id_reproduccion) AS cantidad_reproducciones,
    COUNT(DISTINCT r.id_usuario) AS usuarios_activos,
    SUM(r.tiempo) AS tiempo_total,
    AVG(c.duracion) AS duracion_promedio
FROM Reproducciones r
JOIN Canciones c ON r.id_cancion = c.id_cancion
JOIN Generos g ON c.id_genero = g.id_genero
JOIN Usuarios u ON r.id_usuario = u.id_usuario
GROUP BY g.nombre
ORDER BY tiempo_total DESC;