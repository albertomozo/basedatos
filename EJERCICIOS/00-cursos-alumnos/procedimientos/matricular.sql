DELIMITER //

CREATE PROCEDURE MatricularAlumno(
    IN p_IDAlumno INT,
    IN p_IDCurso INT,
    OUT p_Mensaje VARCHAR(255)
)
BEGIN
    -- Declaración de variables
    DECLARE v_PlazasOcupadas INT;
    DECLARE v_MaxPlazas INT;

    -- Verificar si el alumno existe
    IF NOT EXISTS (SELECT 1 FROM Alumno WHERE ID_Alumno = p_IDAlumno) THEN
        SET p_Mensaje = 'El alumno no existe.';
    ELSEIF NOT EXISTS (SELECT 1 FROM Curso WHERE ID_Curso = p_IDCurso) THEN
        SET p_Mensaje = 'El curso no existe.';

    -- Verificar si hay plazas disponibles
    ELSE
        SELECT COUNT(*) INTO v_PlazasOcupadas FROM Matricula WHERE ID_Curso = p_IDCurso;
        SELECT Max_Plazas INTO v_MaxPlazas FROM Curso WHERE ID_Curso = p_IDCurso;

        IF v_PlazasOcupadas >= v_MaxPlazas THEN
            SET p_Mensaje = 'No hay plazas disponibles en el curso.';
        ELSEIF EXISTS (SELECT 1 FROM Matricula WHERE ID_Alumno = p_IDAlumno AND ID_Curso = p_IDCurso) THEN
            SET p_Mensaje = 'El alumno ya está matriculado en este curso.';
        ELSE
            -- Realizar la matrícula
            INSERT INTO Matricula (ID_Alumno, ID_Curso) VALUES (p_IDAlumno, p_IDCurso);
            SET p_Mensaje = 'Matrícula realizada con éxito.';
        END IF;
    END IF;
END //

DELIMITER ;