# README: Uso de la API de Airtable con Postman y generación de código en JavaScript y Python

Este documento explica cómo interactuar con la API de Airtable usando Postman para realizar pruebas y generar código en JavaScript y Python. Se enfoca en el uso local del código sin depender de servidores como Netlify.

---

## **Requisitos previos**

1. **Cuenta en Airtable**: Regístrate y accede a tu base en Airtable.
2. **Postman**: Descarga e instala la aplicación de escritorio de Postman.
3. **API Key o Token de Acceso Personal**: Obtén tu clave desde la sección de configuración de Airtable.

---

## **Configuración inicial**

### **1. Obtener el Token de Acceso Personal**

- Ve a la sección de "API Documentation" en Airtable.
- Genera un token personal desde la opción "Create Tokens".
- Copia este token para usarlo en las solicitudes.


### **2. Configurar Postman**

1. Abre Postman y crea una nueva colección para organizar tus solicitudes.
2. Configura una solicitud GET para obtener datos:
    - URL: `https://api.airtable.com/v0/YOUR_BASE_ID/TABLE_NAME`
    - Reemplaza `YOUR_BASE_ID` y `TABLE_NAME` con los valores correspondientes.
    - En la pestaña "Headers", añade:
        - **Key**: `Authorization`
        - **Value**: `Bearer YOUR_ACCESS_TOKEN`
3. Haz clic en "Send" para probar tu solicitud y ver la respuesta en formato JSON.

---

