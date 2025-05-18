USE encuestas_votaciones;

-- Agregar las columnas faltantes a la tabla encuesta
ALTER TABLE encuesta ADD COLUMN fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE encuesta ADD COLUMN fecha_cierre DATETIME NULL;
ALTER TABLE encuesta ADD COLUMN estado VARCHAR(20) DEFAULT 'activo';
