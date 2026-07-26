SELECT c.id_cancion, c.titulo, c.duracion, g.nombre AS genero, c.id_artista
FROM canciones c
JOIN generos g ON c.id_genero = g.id_genero;