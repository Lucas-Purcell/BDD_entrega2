# BDD_entrega2
Para poder ejecutar los cargadores desde la terminal, se debe ingresar a ```entrega2/Scripts/``` y ejecutar el comando ```python3 main.py```. Este script se encargará de ejecutar todos los otros scripts en el orden correcto para que no exstan errores de dependencias de unas tablas con otras. Luego de poblar todas las tablas, man.py escrbirá en el archivo ```error.txt``` todos los errores que se atraparon durante la ejecución, con la excepción de los errores al insertar en la base de datos como UniqueViolation y ForeignKeyViolation. Estos debido a que es esperable que estos errores ocurran muy seguido y son propios de filas con información repetida o de filas con información sobre entidades que se decidieron filtrar y eliminar.

Se asumió que el formato de los csv que se quieran cargar a la bases de datos siempre tendrán los mismos nombres de archivo que los que fueron entregados para la tarea en giithub, estaas son:
calificacion.csv
cldeldes.csv 
clientes.csv
comuna2.csv 
pedidos2.csv 
platos.csv
restaurantes2.csv 
suscripciones.csv

Además se asume que el orden de las columnas es el mismo que el de estos rchivos orignales, el nombre de las columnas puede variar sin causar problemas a los scripts.

En resumen se asumió que estos archivos serán consistentes con los entregados para la entrega2.

Además de las instrucciones sobre las restricciones de integridad de los datos, se asumieron las siguientes restricciones de integridad:
- El nombre de un usuario debe ser alfanumérico.



También se modificaron las siguientes restricciones con respecto a las instrucciones porque se consideró que eran necesarias para permitir un correcto funcionamiento de los scripts:
- El número de telefono puede tener el formato +56 XXX XXX XXX, donde 56 es el código de país y XXX XXX XXX es el número de teléfono, o bien se acepta que sea +562 XXX XXX XXX, donde 562 es el código de país para telefonos fijos. Esto se hizo para permitir que los números de teléfono de los clientes puedan ser insertados en la base de datos.


Los siguientes casos son tratados por los mismos scripts:
- Si un nombre de Plato es muy largo, se modificará la restricción de longitud de caracteres para que se pueda insertar en la base de datos.
- Si el nombre de una calle es muy largo, se modificará la restricción de longitud de caracteres para que se pueda insertar en la base de datos.

