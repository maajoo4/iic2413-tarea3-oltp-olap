SELECT 
    c.id_cancion,
    MAX(r.tiempo)
FROM fact_reproducciones r
JOIN dim_cancion c 
    ON r.id_cancion = c.id_cancion
GROUP BY c.id_cancion;
