El presente proyecto está basado en el stack ELT. 
Primero conecta bases de datos sql y noSql con elasticsearch mediante logstash, para luego generar visualizaciones con Kibana. 

Instalación Herramientas:
1. Instalar las herramientas del stack: Elasticsearch, Logstash, Kibana. Su instalación es similar, descargamos los archivos desde los sitios oficiales y los colocamos en la raíz de nuestro sistema operativo (C:\)
2. Para verificar su funcionamiento, ingresamos a cmd y luego accedemos a la carpeta de cada uno de los servicios. Ejemplo:
Para ver funcionamiento de elasticsearch: 
cd elasticsearch
elasticsearch
NOTA: Es importante tener instaladas y configuradas las variables de entorno de java, aquí un video para conseguir eso: 
https://www.youtube.com/watch?v=8oFZ06yGsnM

Pasos:
Guardando en MongoDB
1. Una vez instalado el stack ELK, procederemos a realizar una mineria de datos de Twitter con Python, dentro del repositorio se encuentra un archivo llamado "cosecha.py", el cual contiene el script correspondiente.
2. Instalamos la librería necesaria con el comando pip install pymongo
3. Editamos las siguientes lineas a conveniencia, en este caso enviamos los datos relacionados a quejas y las coordenadas para la geolocalización de nuestro país
twitterStream.filter(track=["ecuador","ineficiencia", "ineptos","renunciaromo","yunda","corrupcion", "correa", "glass", "paronacional"])
twitterStream.filter(locations=[0.22985,-78.5249481,2.1961601,-79.8862076])
4. Ejecutamos
NOTA: Es importante modificar la cadena de conexión de atlas, por la del usuario de atlas que desee recolectar los tweets.

Guardando en CouchDB
1. Utilizamos el mismo script de Python, pero con la sintaxis de CouchDB para la conexión e inserción de datos. 
2. Instalamos la libreria necesaria con el comando pip install couchdb
3. Ejecutamos

Guardando en MySql 
1. Instalar XAMPP (https://www.apachefriends.org/es/index.html), correr el servidor de Mysql y de Apache.
2. Creamos una base de datos con el número de columnas correspondiente al número de columnas del dataset. El mismo debe ser de tipo .CSV
3. Ingresamos a importar, importamos el archivo y luego  seleccionamos CSV loading data, marcamos la casilla para que la importación se realice pese a algún error en el insert. 

Enviando BDs de Mysql a SQL 
1. Instalar SSMA (https://docs.microsoft.com/en-us/sql/ssma/sql-server-migration-assistant?view=sql-server-ver15)
2. Dentro del mismo selecionamos la opción de conectar con Mysql, seleccionamos la base de datos, las credenciales y ejecutamos la importación. 

Envando datos a Elasticsearch
Sql a Elasticsearch
1. Dentro de carpeta config del directorio de logstash, copiamos el archivo sql.conf
2. Instalamos el conector necesario: jdbc (https://docs.microsoft.com/en-us/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server?view=sql-server-ver15)
3. Corremos el comando logstash - f sql.conf

Couch a Elasticsearch
1. Dentro de carpeta config del directorio de logstash, copiamos el archivo couch.conf
2. Corremos el comando logstash - f couch.conf

Visualizaciones
1. Iniciamos el servicio de Kibana, ingresamos a localhost:5601 
2. Damos clic en el icono de rueda, allí creamos los índices de las bases de datos que están albergadas en elasticsearch
3. Nos dirigimos al apartado de visualizaciones, creamos una nueva visualización en y-axis lo podemos dejar por defecto, agregamos un x-axis, seleccionamos agregation, seleccionamos terms, seleccionamos el campo que queremos graficar. 
4. Damos clic en el botón azul con simbolo de play para ver la gráfica. 

Generar reporte HTML con Skeddler
1. Descargamos e instalamos Skeddler de igual forma que las herramientas del stack elk
2. Ingresamos a la carpeta de Skeddler
3. Corremos el comando service skeddler service.bat start 

Información extra.
Se pueden encontrar varios datasets de temas de interés en kaggle: https://www.kaggle.com/
Para la generación de tweets, es importante solicitar nuestra propia key para poder consumir el api. 







