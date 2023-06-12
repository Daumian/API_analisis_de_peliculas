from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np

app = FastAPI()
# http://127.0.0.1:8000 



# Importamos dataset
credits_df = pd.read_csv(r'dcredits_limpio.csv')
movies_df = pd.read_csv(r'dmovies_df_limpio.csv')

movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], format='%Y-%m-%d', errors='coerce')


#Consultas

def peliculas_mes(mes:str):
   meses = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
   mes_numerico = meses.get(mes.lower())

   #Prevencion de errores
   if mes_numerico is None:
      return "error: Dato erroneo, por favor envia un dato en formato texto, por ejemplo 'febrero'" 

   peliculas_en_este_mes = movies_df[movies_df['release_date'].dt.month == mes_numerico]
   num_peliculas = len(peliculas_en_este_mes)
   #return
   
   return {f'mes: {mes}, cantidad: {num_peliculas}'}  

def peliculas_dia(dia:int):
   dia_numerico = dia

   #Prevencion de errores
   if dia_numerico is None:
      return "error: Dato erroneo, por favor envia un dato en formato numero, desde el 1 al 31" 

   peliculas_en_este_dia = movies_df[movies_df['release_date'].dt.day == dia_numerico]
   num_peliculas = len(peliculas_en_este_dia)
   #return
   return {f'dia: {dia},cantidad: {num_peliculas}'}



def pelicula_datos(titulo:str):
    coincidencias = movies_df[movies_df['title'].str.contains(titulo, case=False)]
    resultados = coincidencias[['title', 'release_year', 'vote_average']].values.tolist()
    resultados_formateados = '|                                       |'.join([f"Título: {r[0]} | Fecha de lanzamiento: {r[1]} | Calificación: {r[2]}" for r in resultados])
    return resultados_formateados


def votos_titulo(titulo:str):
    coincidencias = movies_df[(movies_df['title'].str.contains(titulo, case=False)) & (movies_df['vote_count'] > 2000)]
    resultados = coincidencias[['title', 'vote_average', 'vote_count']].values.tolist()
    resultados_formateados = '|                                       |'.join([f"Título: {r[0]} | Puntuacion: {r[1]} | Cantidad de votos: {r[2]}" for r in resultados])
    return resultados_formateados


def obtener_informacion_actor(actor_nombre):
    coincidencias = credits_df[credits_df['cast'].str.contains(actor_nombre, case=False)]
    ids_peliculas = coincidencias['id'].tolist()
    peliculas_participadas = movies_df[movies_df['id'].isin(ids_peliculas)]
    num_peliculas = len(peliculas_participadas)
    suma_recaudacion = peliculas_participadas['return_of_invertion'].sum()
    return actor_nombre, num_peliculas, suma_recaudacion


def get_directore(director_nombre):
    coincidencias = credits_df[credits_df['crew'].str.contains(director_nombre, case=False)]   
    ids_peliculas = coincidencias['id'].tolist()
    peliculas_dirigidas = movies_df[movies_df['id'].isin(ids_peliculas)]
    datos_mostrar = peliculas_dirigidas[['title', 'release_year','revenue','budget','return_of_invertion']].values.tolist()
    resultados_sumados = '\n'.join([f"Título: {r[0]} | Lanzamiento: {r[1]} | Recaudacion: {r[2]} | Presupuesto: {r[3]} |Return of Invertion: {r[4]} | " for r in datos_mostrar])

    suma_recaudacion = peliculas_dirigidas['return_of_invertion'].sum()
    TituloD = f'{director_nombre} ha recaudado un total de {suma_recaudacion} dirigiendo:'
    final_director = TituloD + "\n" + resultados_sumados + "|                                       |"

    return final_director


def buscar_recomendacion(nombre):
    # Filtrar películas con los mismos géneros
    pelicula = movies_df[movies_df['title'].str.contains(nombre, case=False, na=False)].head(1)
    if len(pelicula) == 0:
        return "No se encontraron películas con ese título o texto relacionado."
    # Obtener los géneros de la película encontrada
    generos_pelicula = pelicula['genres'].iloc[0]
    # Filtrar películas con los mismos géneros
    peliculas_similares = movies_df[movies_df['genres'] == generos_pelicula]
    # Ordenar por la calificación promedio
    peliculas_similares = peliculas_similares.sort_values(by='vote_average', ascending=False)
    # Mostrar un máximo de 5 películas
    peliculas_similares = peliculas_similares.head(5)

    peliculas_similares = peliculas_similares[['title', 'genres']]
    peliculas_similares = peliculas_similares.reset_index(drop=True)
    
    resultado = f"Películas similares a '{nombre}':"
    for index, pelicula in peliculas_similares.iterrows():
        titulo = pelicula['title']
        generos = pelicula['genres']
        resultado += f"{titulo} |{generos} |                                       |"

    return resultado





def actor_participo_en(actor_nombre):
    coincidencias = credits_df[credits_df['cast'].str.contains(actor_nombre, case=False)]
    ids_peliculas = coincidencias['id'].tolist()
    peliculas_participadas = movies_df[movies_df['id'].isin(ids_peliculas)]
    titulos_peliculas = peliculas_participadas['title'].tolist()
    return titulos_peliculas



#1   
#Se ingresa el mes y la funcion retorna la cantidad de peliculas
#que se estrenaron ese mes historicamente
@app.get('/cantidad_filmaciones_mes/{mes}')
async def cantidad_filmaciones_mes(mes: str):
   can_peliculas_mes=peliculas_mes(mes)
   return can_peliculas_mes

#2   
#Se ingresa el dia y la funcion retorna 
#la cantidad de peliculas que se estrebaron ese dia historicamente
@app.get('/cantidad_filmaciones_dia/{dia}')
async def cantidad_filmaciones_dia(dia: int):
   can_peliculas_dia=peliculas_dia(int(dia))
   return can_peliculas_dia


#3
#Se ingresa el título de una filmación esperando 
#como respuesta el título, el año de estreno y el score                
@app.get('/score_titulo/{titulo}')
async def score_titulo(titulo: str):
    texto_buscado = titulo  
    resultados = pelicula_datos(texto_buscado)
    respuesta_datos = resultados
    return respuesta_datos


#4
#Se ingresa el título de una filmación esperando como respuesta el título, 
# a cantidad de votos y el valor promedio de las votaciones. 
#La misma variable deberá de contar con al menos 2000 valoraciones, 
#caso contrario, debemos contar con un mensaje avisando que no cumple 
#esta condición y que por ende, no se devuelve ningun valor.
@app.get('/votos_titulo/{titulo}')
async def votos_titulo(titulo: str):
    texto_buscado = titulo  
    resultados = pelicula_datos(str(texto_buscado))
    respuesta_datos = resultados
    return respuesta_datos

#5
#se ingresa el nombre de un actor que se encuentre dentro 
#de un dataset debiendo devolver el éxito del mismo medido 
#a través del retorno. 
#Además, la cantidad de películas que en las que ha participado y 
#el promedio de retorno
@app.get('/get_actor/{actor}')
async def get_actor(actor: str):
    actor_buscado = actor
    resultado = obtener_informacion_actor(actor_buscado)
    nombre_actor, num_peliculas, recaucacion = resultado
    respuesta_actor = f"{nombre_actor} participó en {num_peliculas} películas y recaudó un total de {recaucacion}."
    return respuesta_actor


#6
#Se ingresa el nombre de un director que se encuentre dentro de
#un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
#Además, deberá devolver el nombre de cada película con la 
#fecha de lanzamiento, retorno individual, costo y ganancia de la misma.
@app.get('/get_director/{director}')
async def get_director(director: str):
    resultados = get_directore(director)
    return resultados



#7 Recomendador de peliculas
#Se ingresa el titulo de una pelicula y devuelve las peliculas similares

@app.get('/recomendacion/{titulo}')
async def search_actor(titulo: str):
    resultados = buscar_recomendacion(titulo)
    return resultados


#8
#recibe un actor
#devuelve las peliculas en las que actuo
@app.get('/search_actor/{actor}')
async def search_actor(actor: str):
    director_buscado = actor
    resultados = get_director(director_buscado)
    return resultados

#9
#El home tiene informacion, para que te sepas orientar en la api
@app.get("/", response_class=HTMLResponse)
async def home():
   lineas = [
    "BIENVENIDO<br>"
    "estos son los path que existen:<br>",
    "Cantidad de peliculas estrenadas este mes (Enero,Frebrero...)",
    "@app.get('/cantidad_filmaciones_mes/{mes}')<br><br>",
    "Cantidad de peliculas extrenadas ese dia",
    "@app.get('/cantidad_filmaciones_dia/{dia}')<br><br>",
    "Año de estreno y escore de una pelicula",
    "@app.get('/score_titulo/{titulo}')<br><br>",
    "Votos y score de una pelicula",
    "@app.get('/votos_titulo/{titulo}')<br><br>",
    "Recaudacion de un actor y peliculas",
    "@app.get('/get_actor/{actor}')<br><br>",
    "peliculas de un director",
    "@app.get('/get_director/{director}')",
    "peliculas de un actor",
    "@app.get('/search_actor/{actor}')"
   ]
   return "<br>".join(lineas) 
