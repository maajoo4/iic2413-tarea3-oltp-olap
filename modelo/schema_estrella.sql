CREATE TABLE Dimen_usuario (id_usuario SERIAL PRIMARY KEY,
                            nombre varchar(50) NOT NULL, 
                            email varchar(50) NOT NULL, 
                            pais varchar(50) NOT NULL, 
                            fecha_registro TIMESTAMP NOT NULL, 
                            plan varchar(30) NOT NULL
);

CREATE TABLE Dimen_artista (id_artista SERIAL PRIMARY KEY,
                            nombre varchar(50) NOT NULL,
                            pais_origen varchar(30) NOT NULL,
                            genero_principal varchar(40) NOT NULL
                        
);

CREATE TABLE Dimen_cancion (id_cancion SERIAL PRIMARY KEY,
                            titulo varchar(50) NOT NULL,
                            duracion INT NOT NULL,
                            genero varchar(30) NOT NULL
);

CREATE TABLE Reproducciones (id_reproduccion SERIAL NOT NULL PRIMARY KEY,
                                id_usuario INT NOT NULL REFERENCES Dimen_usuario(id_usuario),
                                id_cancion INT NOT NULL REFERENCES Dimen_cancion(id_cancion),
                                id_artista INT NOT NULL REFERENCES Dimen_artista(id_artista),
                                tmsp TIMESTAMP NOT NULL,
                                dispositivo varchar(50) NOT NULL,
                                tiempo INT NOT NULL
);