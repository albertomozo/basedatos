CREATE TABLE Alumno (
    ID_Alumno INTEGER PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Apellidos TEXT NOT NULL,
    DNI TEXT UNIQUE NOT NULL,
    Email TEXT UNIQUE,
    Telefono TEXT
);

CREATE TABLE Curso (
    ID_Curso INTEGER PRIMARY KEY,
    Nombre_Curso TEXT NOT NULL,
    Descripcion TEXT,
    Fecha_Inicio DATE,
    Fecha_Fin DATE,
    Max_Plazas INTEGER NOT NULL
);

CREATE TABLE Matricula (
    ID_Matricula INTEGER PRIMARY KEY,
    ID_Alumno INTEGER,
    ID_Curso INTEGER,
    Fecha_Matricula DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Alumno) REFERENCES Alumno(ID_Alumno),
    FOREIGN KEY (ID_Curso) REFERENCES Curso(ID_Curso)
);