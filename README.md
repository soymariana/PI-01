# PI-01
**Primer proyecto individual de Henry**

**Herramientas utilizadas:**
Para efectos de esta práctica, se trabajó la ETL y el EDA sobre google colaboratory, además, para el archivo de la API main.py se trabajó en visual studio code.

**Ingeniería de datos:**
El primer paso realizado una vez descargados los datasets de movies.csv y credits.csv y cargados a google colab como df, fue realizar transformaciones en las columnas de ambos arvhivos, puesto a que en algunas columnas se encontraban datos anidados y era necesario acceder a ellos, de manera tal que se realizó una función para desanidar cada columna.
Una vez realizadas las transformaciones requeridas (por separado para cada archivo) se concatenaron ambos dataframes, dando como resultado df_unido, el cual fue exportado como csv para ser cargado en VS code.
Posteriormente, se procedió a crear la API en VS code, así que se cargó el csv y se procedió al desarrollo de la API creando las funciones solicitadas.
Una vez que fue creada la API, se subió el archivo main.py al repositorio (creado anteriormente), se realizó el registro en Render y se creó la web service.

**Análisis Exploratorio de datos:**
En el EDA se revisaron las variables involucradas, la estadística descriptiva básica de las variables numéricas, se realizaron gráficos univariables y de correlación, análisis de outliers, de las variables categóricas y una nube de palabras.

**Sistema de recomendación:**
Finalmente, se creó el sistema de recomendación sobre el archivo main.py, donde se realizó la matriz de correlaciones y la función recomendación que se añade a la API, recomendando 5 películas similares al título de la película de entrada.
