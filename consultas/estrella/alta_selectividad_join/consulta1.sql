SELECT c.titulo, c.duracion, a.nombre, a.pais_origen
FROM dim_cancion c
JOIN dim_artista a ON c.id_artista = a.id_artista
WHERE c.id_cancion = 1300;