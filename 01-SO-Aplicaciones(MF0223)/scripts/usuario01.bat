
@echo off
:: Verificar si se pasaron suficientes parámetros
if "%~1"=="" (
    
	:: Solicitar el nombre de la carpeta
	set /p nombre=Introduce el nombre de la carpeta principal:
) else (
	set nombre=%1
	echo nombre %nombre%
)

echo nombre %nombre%
:: Crear la carpeta principal

echo IFCT0310 %IFCT0310%
mkdir "%nombre%"

:: Crear subcarpetas y archivos en ellas
mkdir "%nombre%\Subcarpeta1"
mkdir "%nombre%\Subcarpeta2"
echo Este es un archivo en Subcarpeta1 > "%nombre%\Subcarpeta1\archivo1.txt"
echo Este es un archivo en Subcarpeta2 > "%nombre%\Subcarpeta2\archivo2.txt"

:: copia del fichero dir
copy "..\dir.txt" "%nombre%\copiadir.txt"

:: Confirmar la creación
echo Carpeta principal y subcarpetas creadas con exito.
pause
