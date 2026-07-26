-- SELECT 2 o 3 JOINS  SELECTIVIDAD BAJA SIN JOINS CON AGREGACION 
-- Beneficia OLAP

SELECT 
    u.pais,
    COUNT(DISTINCT u.id_usuario) AS cantidad_usuarios,
    COUNT(r.id_reproduccion) AS cantidad_reproducciones,
    SUM(r.tiempo) AS tiempo_total,
    AVG(r.tiempo) AS promedio_tiempo
FROM Reproducciones r
JOIN Usuarios u ON r.id_usuario = u.id_usuario
JOIN Canciones c ON r.id_cancion = c.id_cancion
JOIN Artistas a ON c.id_artista = a.id_artista
WHERE u.plan = 'free'
GROUP BY u.pais
ORDER BY tiempo_total DESC;

-- Como se comportan los usuarios de plan free