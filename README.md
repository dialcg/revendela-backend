# Revendela

Revendela es una aplicacion web para la venta de tickets (entradas) para eventos de musica electronica

## Requisitos

- Python 3.10
- Django 5.0 
- Docker
- Docker Compose

## Instalación

1. Clona el repositorio:

     ```
     git clone git@github.com:JDGARCIA05/revendela-backend.git
     cd revendela
     ```

2. Instala los requerimientos del proyecto

      Dentro del gestor de entorno virtual que has creado, realiza la instalacion de los requerimientos necesarios para correr correctamente el proyecto:

      ```
      pip install -r requirements.txt -r requirements-dev.txt
      ```

3. Configura las variables de entorno

      Crea un archivo .env en la raiz del proyecto junto a settings.py
      constantes esperadas:

      ```
      DB_NAME
      DB_USER
      DB_PASSWORD
      ```

4. Corre el servidor con Docker

      Luego de haber instalado los requerimientos del proyecto procedemos a correr el proyecto con Docker:

      ```
      docker-compose up --build
      ```

5. Corre el servidor con Gunicorn

      Si prefieres usar Gunicorn para correr el servidor, puedes hacerlo con el siguiente comando:

      ```
      gunicorn revendela.wsgi:application --bind 0.0.0.0:8000
      ```

## Autenticación con Token

### Obtención de un Token de Acceso

Para autenticarte en la API, primero debes obtener un token de acceso utilizando tu nombre de usuario y contraseña. Puedes hacer una solicitud `POST` a la API de autenticación usando Postman:

1. Abre Postman y crea una nueva solicitud `POST`.
2. En la URL, ingresa `http://127.0.0.1:8000/authy/api/token/`.
3. En la pestaña `Headers`, agrega un nuevo encabezado con la clave `Content-Type` y el valor `application/json`.
4. En la pestaña `Body`, selecciona `raw` y `JSON`, luego ingresa el siguiente JSON:

     ```json
     {
          "username": "tu_usuario",
          "password": "tu_contraseña"
     }
     ```

5. Haz clic en `Send` para enviar la solicitud.

#### Respuesta esperada:

```json
{
     "access": "<access_token>",
     "refresh": "<refresh_token>"
}
```

### Renovar el Token de Acceso

El token de acceso tiene una duración limitada. Para renovarlo sin necesidad de volver a ingresar credenciales, usa el token de actualización en Postman:

1. Abre Postman y crea una nueva solicitud `POST`.
2. En la URL, ingresa `http://127.0.0.1:8000/authy/api/token/refresh/`.
3. En la pestaña `Headers`, agrega un nuevo encabezado con la clave `Content-Type` y el valor `application/json`.
4. En la pestaña `Body`, selecciona `raw` y `JSON`, luego ingresa el siguiente JSON:

     ```json
     {
          "refresh": "<refresh_token>"
     }
     ```

5. Haz clic en `Send` para enviar la solicitud.

#### Respuesta esperada:

```json
{
     "access": "<nuevo_access_token>"
}
```

## Troubleshooting

Si experimentas problemas durante la instalación o ejecución del proyecto, verifica:

- Que tienes las versiones correctas de Python y Django instaladas.
- Que el archivo `.env` contiene la configuración correcta.
- Que los contenedores Docker están corriendo sin errores (`docker ps` para verificar).
- Que los permisos de tu base de datos están correctamente configurados.

