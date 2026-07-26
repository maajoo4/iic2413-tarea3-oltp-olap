-- SELECT 1 JOINS selectividad alta sin agregacion
-- Beneficia OLTP

-- Todas las canciones de un artista especifico 

SELECT c.titulo, c.duracion
FROM Artistas a
JOIN Canciones c ON a.id_artista = c.id_artista
WHERE a.id_artista = 50;