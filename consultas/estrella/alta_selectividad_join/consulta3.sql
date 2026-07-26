SELECT c.titulo, c.duracion
FROM dim_artista a
JOIN dim_cancion c ON a.id_artista = c.id_artista
WHERE a.id_artista = 50;