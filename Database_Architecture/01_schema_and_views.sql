-- ==========================================
-- PROYECTO: OSM Analytics - Modelo Relacional
-- ==========================================

-- 1. CREACIÓN DE DIMENSIONES (Catálogos)
CREATE TABLE Equipos (
    id_equipo SERIAL PRIMARY KEY,
    nombre_equipo VARCHAR(100) NOT NULL,
    presupuesto NUMERIC(15,2)
);

CREATE TABLE Jugadores (
    id_jugador SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    valoracion INT CHECK (valoracion BETWEEN 1 AND 100),
    id_equipo INT,
    FOREIGN KEY (id_equipo) REFERENCES Equipos(id_equipo)
);

-- 2. CREACIÓN DE TABLA DE HECHOS (Fact Table con Multi-FK)
CREATE TABLE Partidos (
    id_partido SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    id_equipo_local INT,
    id_equipo_visitante INT,
    goles_local INT,
    goles_visitante INT,
    FOREIGN KEY (id_equipo_local) REFERENCES Equipos(id_equipo),
    FOREIGN KEY (id_equipo_visitante) REFERENCES Equipos(id_equipo)
);

-- 3. VISTA ANALÍTICA: Historial y Cálculo de Puntos (Multi-JOIN y CASE WHEN)
CREATE OR REPLACE VIEW vista_historial_partidos AS
SELECT 
    p.fecha,
    el.nombre_equipo AS equipo_local,
    p.goles_local,
    p.goles_visitante,
    ev.nombre_equipo AS equipo_visitante,
    CASE WHEN p.goles_local > p.goles_visitante THEN 3 WHEN p.goles_local = p.goles_visitante THEN 1 ELSE 0 END AS puntos_local,
    CASE WHEN p.goles_visitante > p.goles_local THEN 3 WHEN p.goles_visitante = p.goles_local THEN 1 ELSE 0 END AS puntos_visitante
FROM Partidos p
JOIN Equipos el ON p.id_equipo_local = el.id_equipo
JOIN Equipos ev ON p.id_equipo_visitante = ev.id_equipo;

-- 4. VISTA DE NEGOCIO: Tabla de Posiciones (CTE, UNION ALL y Window Functions)
CREATE OR REPLACE VIEW tabla_posiciones AS
WITH TodosLosPuntos AS (
    SELECT equipo_local AS club, puntos_local AS puntos FROM vista_historial_partidos
    UNION ALL
    SELECT equipo_visitante, puntos_visitante FROM vista_historial_partidos
)
SELECT 
    club,
    SUM(puntos) AS puntos_totales,
    RANK() OVER (ORDER BY SUM(puntos) DESC) AS posicion_liga
FROM TodosLosPuntos
GROUP BY club;