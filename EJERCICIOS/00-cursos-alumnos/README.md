# Enunciado del Universo del Problema
Imagina una academia de formación que ofrece una variedad de cursos especializados. Cada curso tiene un número máximo de plazas disponibles. Los alumnos interesados deben inscribirse en los cursos deseados, y el sistema debe gestionar las inscripciones, asegurando que no se exceda el límite de plazas por curso. Además, la academia quiere mantener un registro de los alumnos, sus datos personales y los cursos en los que están inscritos.

## Modelo Entidad-Relación (MER)

### Entidades

#### Alumno:
    ID_Alumno (Clave Primaria)
    Nombre
    Apellidos
    DNI
    Email
    Telefono
#### Curso:
    ID_Curso (Clave Primaria)
    Nombre_Curso
    Descripcion
    Fecha_Inicio
    Fecha_Fin
    Max_Plazas
#### Matricula:
    ID_Matricula (Clave Primaria)
    ID_Alumno (Clave Foránea, referencia a Alumno)
    ID_Curso (Clave Foránea, referencia a Curso)
    Fecha_Matricula

### Relaciones
Un Alumno puede tener múltiples Matrículas (relación uno a muchos).
Un Curso puede tener múltiples Matrículas (relación uno a muchos).
La tabla Matricula, sirve para resolver la relación de muchos a muchos entre Alumno y Curso.

### Diagrama MER (descripción textual)
Alumno (1) --- (*) Matricula
Curso (1) --- (*) Matricula

## Instalación

lanzar lso scripts de incializacion  en este orden
1 - cursos_schem.sql
2 - cursos_data.sql 

## Procedimientos almacenados

en matricular.sql , esta el codigo que nos permite hacer una matriculación de un alaumno en un curso.

### Explicación del Procedimiento
#### 1 - Verificación de Existencia:
Se verifica si el alumno y el curso existen en sus respectivas tablas.
#### 2 -Verificación de Plazas:
Se cuenta el número de matrículas existentes para el curso y se compara con el máximo de plazas permitidas.
#### 3 -Verificación de Matrícula Duplicada:
Se verifica si el alumno ya se encuentra matriculado en el curso.
#### 4 - Realización de la Matrícula:
Se inserta un nuevo registro en la tabla Matricula, registrando la matrícula del alumno en el curso.
Se registra la fecha de la matricula.


Para lanzar el procedimiento hay que ejecutar

```sql 
SET @mensaje = '';
CALL MatricularAlumno(1, 3, @mensaje);
SELECT @mensaje;
```





