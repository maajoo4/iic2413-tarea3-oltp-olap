SELECT r.id_reproduccion, r.id_usuario, r.id_cancion, c.id_artista, r.tmsp, r.dispositivo, r.tiempo
FROM Reproducciones r
JOIN Canciones c ON r.id_cancion = c.id_cancion;