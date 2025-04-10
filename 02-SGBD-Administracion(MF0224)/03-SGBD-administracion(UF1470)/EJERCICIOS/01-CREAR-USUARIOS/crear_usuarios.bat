@echo off
setlocal

:: Parámetros de entrada
set "DB_NAME=%1"
set "DB_USER=%2"
set "DB_PASS=%3"
set "DB_ROOT_USER=%4"
set "DB_ROOT_PASS=%5"

:: Validación de parámetros
if "%~5"=="" (
    echo Uso: %~nx0 DB_NAME DB_USER DB_PASS DB_ROOT_USER DB_ROOT_PASS
    exit /b 1
)

:: Ejecutar los comandos de MySQL
echo Creando base de datos y usuario...

mysql -u %DB_ROOT_USER% -p%DB_ROOT_PASS% -e ^
"CREATE DATABASE IF NOT EXISTS `%DB_NAME%`; ^
CREATE USER IF NOT EXISTS '%DB_USER%'@'%%' IDENTIFIED BY '%DB_PASS%'; ^
GRANT ALL PRIVILEGES ON `%DB_NAME%`.* TO '%DB_USER%'@'%%'; ^
FLUSH PRIVILEGES;"

:: Comprobar el resultado
if errorlevel 1 (
    echo Error al crear la base de datos o el usuario.
    exit /b 2
) else (
    echo Base de datos y usuario creados correctamente.
)

endlocal
pause

