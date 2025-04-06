@echo off

echo "Eliminando unidades de red existentes..."
net use * /delete /y

echo "Conectando unidades de red..."



net use T: \\192.168.100.118\contabilidad /user:usuario_contabilidad contabilidad
if errorlevel 1 (
    echo "Error al conectar la unidad T: (conta)"
) else (
    echo "Unidad T: conectada correctamente."
)

net use M: \\alberto-virtualbox\marketing  /user:usuario_marketing marketing
if errorlevel 1 (
    echo "Error al conectar la unidad M:"
) else (
    echo "Unidad M: conectada correctamente."
)

net use L: \\192.168.100.118\compartida
if errorlevel 1 (
    echo "Error al conectar la unidad L:"
) else (
    echo "Unidad L: conectada correctamente."
)

net use P: \\192.168.100.118\privada
if errorlevel 1 (
    echo "Error al conectar la unidad P:"
) else (
    echo "Unidad P: conectada correctamente."
)

pause

