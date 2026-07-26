-- SELECT 1 JOIN selectividad alta sin agregacion
-- Beneficia OLTP

-- Ver todos los datos de una reproduccion especifica junto al usuario su plan y pais

SELECT r.id_cancion, 
    r.tmsp, 
    r.dispositivo, 
    r.tiempo, 
    u.nombre AS nombre_usuario, 
    u.plan, 
    u.pais
FROM Reproducciones r 
JOIN Usuarios u ON r.id_usuario = u.id_usuario
WHERE r.id_reproduccion = 678;
