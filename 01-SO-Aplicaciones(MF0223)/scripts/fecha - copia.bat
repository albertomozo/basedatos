
@echo off

:: Obtener fecha y hora del sistema
set fecha=%DATE%
set hora=%TIME%

:: Reemplazar caracteres no válidos en los nombres de archivo
echo fecha :  %fecha%
echo hora : %hora%
set fecha=%fecha:/=-%
set hora=%hora::=-%
set hora=%hora: =0%

:: Crear el archivo con la fecha y hora en el nombre
set nombre_archivo=%fecha%_%hora%.txt
echo Este es un archivo generado el %fecha% a las %hora% > "%nombre_archivo%"

:: Mostrar mensaje de confirmación
echo Archivo generado con el nombre: %nombre_archivo%
pause

