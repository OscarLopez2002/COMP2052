-- Primero eliminamos la base de datos si existe
DROP DATABASE IF EXISTS encuestas_votaciones;

-- Creamos la base de datos
CREATE DATABASE encuestas_votaciones CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usamos la base de datos recién creada
USE encuestas_votaciones;

-- Creamos la tabla role
CREATE TABLE role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL
);

-- Insertamos los roles iniciales
INSERT INTO role (name) VALUES ('Admin'), ('Moderador'), ('Votante');

-- Creamos la tabla user
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

-- Creamos la tabla encuesta
CREATE TABLE encuesta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_cierre DATETIME NULL,
    estado VARCHAR(20) DEFAULT 'activo',
    creador_id INT NOT NULL,
    FOREIGN KEY (creador_id) REFERENCES user(id)
);
-- INSERT INTO user (username, email, password_hash, role_id) VALUES 
-- ('admin', 'admin@example.com', 'hashed_password_placeholder', (SELECT id from role WHERE name = 'Admin'));

/*
-- Para un sistema de encuestas más completo, se podrían necesitar tablas como:

CREATE TABLE pregunta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    encuesta_id INT NOT NULL,
    texto_pregunta VARCHAR(255) NOT NULL,
    tipo_pregunta VARCHAR(50) NOT NULL, -- ej: 'opcion_multiple_unica_respuesta', 'opcion_multiple_varias_respuestas', 'abierta_corta', 'escala_likert'
    orden INT DEFAULT 0, -- Para ordenar preguntas dentro de una encuesta
    FOREIGN KEY (encuesta_id) REFERENCES encuesta(id) ON DELETE CASCADE
);

CREATE TABLE opcion_respuesta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregunta_id INT NOT NULL,
    texto_opcion VARCHAR(255) NOT NULL,
    orden INT DEFAULT 0, -- Para ordenar opciones dentro de una pregunta
    FOREIGN KEY (pregunta_id) REFERENCES pregunta(id) ON DELETE CASCADE
);

CREATE TABLE voto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pregunta_id INT NOT NULL, -- O directamente encuesta_id si el voto es por encuesta y no por pregunta
    opcion_id INT NOT NULL, -- El ID de la opcion_respuesta elegida
    fecha_voto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (pregunta_id) REFERENCES pregunta(id),
    FOREIGN KEY (opcion_id) REFERENCES opcion_respuesta(id),
    UNIQUE (user_id, pregunta_id) -- Un usuario solo puede votar una vez por pregunta
);
*/
