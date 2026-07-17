CREATE TABLE IF NOT EXISTS Usuarios (id_usuario SERIAL PRIMARY KEY, 
                        nombre varchar(50) NOT NULL, 
                        email varchar(50) NOT NULL, 
                        pais varchar(100) NOT NULL, 
                        fecha_registro TIMESTAMP NOT NULL, 
                        plan varchar(30) NOT NULL CHECK (plan IN ('free', 'premium', 'familiar'))
);

CREATE TABLE IF NOT EXISTS Artistas (id_artista SERIAL PRIMARY KEY,
                        nombre varchar(50) NOT NULL,
                        pais_origen varchar(100) NOT NULL,
                        genero_principal varchar(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS Generos (id_genero SERIAL PRIMARY KEY,
                        nombre varchar(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS Canciones (id_cancion SERIAL PRIMARY KEY,
                        duracion INT NOT NULL CHECK (duracion > 0),
                        titulo varchar(50) NOT NULL,
                        id_artista INT NOT NULL REFERENCES Artistas(id_artista),
                        id_genero INT  NOT NULL REFERENCES Generos(id_genero)
);

CREATE TABLE IF NOT EXISTS Reproducciones (id_reproduccion SERIAL PRIMARY KEY,
                            id_usuario INT NOT NULL REFERENCES Usuarios(id_usuario),
                            id_cancion INT NOT NULL REFERENCES Canciones(id_cancion),
                            tmsp TIMESTAMP NOT NULL,
                            dispositivo varchar(50) NOT NULL CHECK (dispositivo IN ('movil', 'web', 'smarttv')),
                            tiempo INT NOT NULL CHECK (tiempo > 0)
);