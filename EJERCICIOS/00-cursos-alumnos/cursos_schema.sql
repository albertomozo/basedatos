CREATE TABLE Alumno (
    ID_Alumno INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    Apellidos VARCHAR(255) NOT NULL,
    DNI VARCHAR(20) UNIQUE NOT NULL,
    Email VARCHAR(255) UNIQUE,
    Telefono VARCHAR(20)
);

CREATE TABLE Curso (
    ID_Curso INT PRIMARY KEY AUTO_INCREMENT,
    Nombre_Curso VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Fecha_Inicio DATE,
    Fecha_Fin DATE,
    Max_Plazas INT NOT NULL
);

CREATE TABLE Matricula (
    ID_Matricula INT PRIMARY KEY AUTO_INCREMENT,
    ID_Alumno INT,
    ID_Curso INT,
    Fecha_Matricula DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Alumno) REFERENCES Alumno(ID_Alumno),
    FOREIGN KEY (ID_Curso) REFERENCES Curso(ID_Curso)
);