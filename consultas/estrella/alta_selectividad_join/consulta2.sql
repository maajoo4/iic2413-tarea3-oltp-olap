SELECT f.id_cancion,
    f.tmsp,
    f.dispositivo,
    f.tiempo,
    u.nombre AS nombre_usuario,
    u.plan,
    u.pais
FROM fact_reproducciones f
JOIN dim_usuario u ON f.id_usuario = u.id_usuario
WHERE f.id_reproduccion = 678;