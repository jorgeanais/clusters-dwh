-- Base structure of the database used in the star cluster dashboard
-- Any change to the table structure must be reflected in the file
-- A new instance of the database should start excecuting this script

DROP SCHEMA IF EXISTS dash_cl CASCADE;
CREATE SCHEMA dash_cl;

CREATE TABLE dash_cl.cluster
(
    cluster     TEXT PRIMARY KEY
);

CREATE TABLE dash_cl.star
(
    star_id     INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    ra          DOUBLE PRECISION NOT NULL,
    dec         DOUBLE PRECISION NOT NULL,
    pmra        DOUBLE PRECISION,
    epmra       DOUBLE PRECISION,
    pmdec       DOUBLE PRECISION,
    epmdec      DOUBLE PRECISION,
    plx         DOUBLE PRECISION,
    eplx        DOUBLE PRECISION,
    mz          DOUBLE PRECISION,
    ez          DOUBLE PRECISION,
    my          DOUBLE PRECISION,
    ey          DOUBLE PRECISION,
    mj          DOUBLE PRECISION,
    ej          DOUBLE PRECISION,
    mh          DOUBLE PRECISION,
    eh          DOUBLE PRECISION,
    mk          DOUBLE PRECISION,
    ek          DOUBLE PRECISION,
    probability DOUBLE PRECISION,
    cluster  TEXT,
    FOREIGN KEY (cluster) REFERENCES dash_cl.cluster
);
