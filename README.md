# Componente lógico de Microservicio Chats
Microservicio que hace parte de todo un sistema basado en microsevicios con la funcionalidad de chat dentro de la aplicación. Es el encargado de gestionar los mensajes de los usuarios haciendo uso de una cola de mensajeria (RabbitMQ), desplegado en contenedores Docker.

## Tecnologías

Las tecnologías usadas para la creación de este microservicio fueron:

- [Python] - Lenguaje de Porgramación base
- [Django] - Framework de Python para backend
- [MongoDB] - Base de datos.
- [Mongo Atlas] - Servicio de despliegue de bases de datos en la nube
- [RabbitMQ] - Cola de mensajeria que gestiona las peticiones al microservicio
