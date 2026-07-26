-- SELECT 1 JOINS selectividad alta sin agregacion
-- Beneficia OLTP

-- Ver los datos de una cancion especifica junto al nombre del artista y su pais de origen
SELECT c.titulo, c.duracion, a.nombre, a.pais_origen
FROM Canciones c
JOIN Artistas a ON c.id_artista = a.id_artista
WHERE c.id_cancion = 1000;

