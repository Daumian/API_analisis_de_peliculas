# Proyecto Henry Peliculas

## Enlaces utiles:
### api  [Render Api](https://api-henry-s9k1.onrender.com)
### eda y etl [deepnote EDA](https://deepnote.com/workspace/daumian-ruiz-ceed-0677a995-df7e-45a8-9540-809a03138f79/project/ETL-Dataframes-00606b1a-4413-426c-8abb-9db2b6644c1b/notebook/57b76f0137b14d4f8755c59acc95dc0d)


## Resumen:
A partir de una base de datos en bruto,que contiene información sobre peliculas, (Titulo, Actores, Generos, Presupuesto, Recaudación, Idioma y Director), tras limpiarla, normalizarla y prepararla, se genero una API donde se pudiera consultar información sobre los distintos datos, plataformas, actores, promedios, etc. Incluso se genero un sistema que te recomienda peliculas en base a tus gustos.

# Procesos del proyecto
## EDA y ETL
### Este proceso se fue limpiando la base de datos, puedes consultarlo en el siguiente [enlace](https://deepnote.com/workspace/daumian-ruiz-ceed-0677a995-df7e-45a8-9540-809a03138f79/project/HenryLabs-sup-11-00606b1a-4413-426c-8abb-9db2b6644c1b/notebook/EDA%20y%20ETL%20movies_csv-57b76f0137b14d4f8755c59acc95dc0d)
 
esta en deepnote para que puedas facilmente ejecutarlo y analizarlo.
se realizaron las siguientes acciones:

1. Algunos campos, como belongs_to_collection, production_companies y otros (ver diccionario de datos), estaban anidados. han sido desanidados para poder y unirlos al dataset nuevamente hacer alguna de las consultas de la API. O bien, buscar la 
2. Los valores nulos de los campos revenue, budget fueron rellenados con el número 0.
3. Los valores nulos del campo release date fueron eliminados.
4. las fechas se pusieron en formato AAAA-mm-dd. Además, y se creo la columna release_year donde se extrajo el año de la fecha de estreno.
5. Se creó la columna con el retorno de inversión, llamada return, con los campos revenue y budget, dividiendo estas dos últimas revenue / budget. Cuando no había datos disponibles para calcularlo, se tomó el valor 
6. Se eliminaron las columnas que no serán utilizadas: video, imdb_id, adult, original_title, poster_path y homepage.


## API

Se disponibilizaron los datos de la empresa mediante el framework FastAPI. Las consultas propuestas son las siguientes:

6 funciones con un decorador (@app.get('/')).

## /cantidad_filmaciones_mes/{Mes} 
Se ingresa un mes en idioma Español. Debe haber devuelto la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.
Ejemplo de retorno: X cantidad de películas fueron estrenadas en el mes de X

## /cantidad_filmaciones_dia/{Dia}
Se ingresa un día en idioma Español. Debe haber devuelto la cantidad de películas que fueron estrenadas en el día consultado en la totalidad del dataset.
Ejemplo de retorno: X cantidad de películas fueron estrenadas en los días X

## /score_titulo/{titulo_de_la_filmación} 
Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
Ejemplo de retorno: La película X fue estrenada en el año X con un score/popularidad de X

## /votos_titulo/{titulo_de_la_filmación} 
Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. La misma variable deberá haber contado con al menos 2000 valoraciones, en caso contrario, debemos haber contado con un mensaje avisando que no cumple esta condición y que por ende, no se devolvió ningún valor.
Ejemplo de retorno: La película X fue estrenada en el año X. La misma cuenta con un total de X valoraciones, con un promedio de X

## /get_actor/{nombre_actor}
Se ingresa el nombre de un actor que se encuentre dentro de un dataset, debiendo haber devuelto el éxito del mismo medido a través del retorno. Además, la cantidad de películas en las que ha participado y el promedio de retorno. La definición no debió haber considerado directores.
Ejemplo de retorno: El actor X ha participado en X cantidad de filmaciones. El mismo ha conseguido un retorno de X con un promedio de X por filmación

## /get_director/{nombre_director} 
Se ingresa el nombre de un director que se encuentre dentro de un dataset, debiendo haber devuelto el éxito del mismo medido a través del retorno. Además, debió haber devuelto el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.

## /recomendacion/{Titulo}
A partir de un titulo se entrega 5 peliculas similares a esta, ordenadas a partir de su puntuación

