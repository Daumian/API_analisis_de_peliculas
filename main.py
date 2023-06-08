from fastapi import FastAPI
import pandas as pd


# import pickle

app = FastAPI()

# http://127.0.0.1:8000 

# Importamos dataset
df = pd.read_csv(r'df_final.csv')
Df = pd.read_csv(r'Df_recomendacion.csv')
df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d', errors='coerce')

with open('similarity_matrix.pickle', 'rb') as f:
    cosine_sim = pickle.load(f)

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
   return {f'el mes de {mes} se extrenaron {num_peliculas} peliculas'} 

def peliculas_dia(dia:int):
   dia_numerico = dia

   #Prevencion de errores
   if dia_numerico is None:
      return "error: Dato erroneo, por favor envia un dato en formato numero, desde el 1 al 31" 

   peliculas_en_este_dia = movies_df[movies_df['release_date'].dt.day == dia_numerico]
   num_peliculas = len(peliculas_en_este_dia)
   #return
   return {f'el dia {dia} del mes, se extrenaron {num_peliculas} peliculas'} 

def pelicula_datos(titulo:str):
    coincidencias = movies_df[movies_df['title'].str.contains(titulo, case=False)]
    resultados = coincidencias[['title', 'release_year', 'vote_average']].values.tolist()
    resultados_formateados = '\n'.join([f"Título: {r[0]} | Fecha de lanzamiento: {r[1]} | Calificación: {r[2]}" for r in resultados])
    return resultados_formateados


def votos_titulo(titulo:str):
    coincidencias = movies_df[(movies_df['title'].str.contains(titulo, case=False)) & (movies_df['vote_count'] > 2000)]
    resultados = coincidencias[['title', 'vote_average', 'vote_count']].values.tolist()
    resultados_formateados = '\n'.join([f"Título: {r[0]} | Puntuacion: {r[1]} | Cantidad de votos: {r[2]}" for r in resultados])
    return resultados_formateados


def obtener_informacion_actor(actor_nombre):
    coincidencias = credits_df[credits_df['cast'].str.contains(actor_nombre, case=False)]
    ids_peliculas = coincidencias['id'].tolist()
    peliculas_participadas = movies_df[movies_df['id'].isin(ids_peliculas)]
    num_peliculas = len(peliculas_participadas)
    suma_recaudacion = peliculas_participadas['return_of_invertion'].sum()
    return actor_nombre, num_peliculas, suma_recaudacion


def get_director(director_nombre):

    coincidencias = credits_df[credits_df['crew'].str.contains(director_nombre, case=False)]   
    ids_peliculas = coincidencias['id'].tolist()
    peliculas_dirigidas = movies_df[movies_df['id'].isin(ids_peliculas)]
    datos_mostrar = peliculas_dirigidas[['title', 'release_year','revenue','budget','return_of_invertion']].values.tolist()
    resultados_sumados = '\n'.join([f"Título: {r[0]} | Lanzamiento: {r[1]} | Recaudacion: {r[2]} | Presupuesto: {r[3]} |Return of Invertion: {r[4]} | " for r in datos_mostrar])
    
    suma_recaudacion = peliculas_dirigidas['return_of_invertion'].sum()
    Titulo = f'{director_nombre} ha recaudado un total de {suma_recaudacion} dirigiendo :'
    final_director = Titulo + "\n" + resultados_sumados

    return final_director



def actor_participo_en(actor_nombre):
    coincidencias = credits_df[credits_df['cast'].str.contains(actor_nombre, case=False)]
    ids_peliculas = coincidencias['id'].tolist()
    peliculas_participadas = movies_df[movies_df['id'].isin(ids_peliculas)]
    titulos_peliculas = peliculas_participadas['title'].tolist()
    return titulos_peliculas



#1   
#recibe un mes en formato texto, ej:"febrero"
#retorna la cantidad de peliculas filmadas ese mes
@app.get('/cantidad_filmaciones_mes/{mes}')
async def cantidad_filmaciones_mes(mes: str):
   can_peliculas_mes=peliculas_mes(mes)
   return can_peliculas_mes

#2   
#recibe un mes en formato texto, ej:"febrero"
#retorna la cantidad de peliculas filmadas ese mes
@app.get('/cantidad_filmaciones_dia/{dia}')
async def cantidad_filmaciones_dia(dia: int):
   can_peliculas_dia=peliculas_dia(int(dia))
   return can_peliculas_dia


#3
#recibe titulo
#devuelve datos de esa pelicula                 
@app.get('/score_titulo/{titulo}')
async def score_titulo(titulo: int):
    texto_buscado = titulo  
    resultados = pelicula_datos(str(texto_buscado))
    respuesta_datos = resultados
    return respuesta_datos


#4
#recibe un titulo
#devuelve su puntuacion, pero solo si hay mas de 2000 votos
@app.get('/votos_titulo/{titulo}')
async def votos_titulo(titulo: str):
    texto_buscado = titulo  
    resultados = pelicula_datos(str(texto_buscado))
    respuesta_datos = resultados
    return respuesta_datos

#5
#recibe un nombre de actor
#devuelve en cuantas peliculas salio y cuanto recaudo
@app.get('/get_actor/{actor}')
async def get_actor(actor: str):
    actor_buscado = "Liam N"
    resultado = obtener_informacion_actor(actor_buscado)
    nombre_actor, num_peliculas, recaucacion = resultado
    respuesta_actor = "{nombre_actor} participó en {num_peliculas} películas y recaudó un total de {recaucacion}."
    return respuesta_actor



#6
#recibe un director
#devuelve cuanto recaudo
#y todas sus peliculas
@app.get('/get_director/{director}')
async def get_director(director: str):
    director_buscado = director
    resultados = get_director(director_buscado)
    return resultados

#7
#recibe un actor
#devuelve las peliculas en las que actuo
@app.get('/search_actor/{actor}')
async def search_actor(actor: str):
    director_buscado = actor
    resultados = get_director(director_buscado)
    return resultados



# # ML. MODELO DE RECOMENDACIÓN
# @app.get('/recomendacion/{titulo}')
# def recomendacion(titulo:str):
#     # Buscar la fila correspondiente al título de la película
#     idx = Df.index[Df["title"].str.lower() == titulo.lower()].tolist()
#     if len(idx) == 0:
#         return "Película no encontrada"
#     else:
#         idx = idx[0]
    
#     # Calcular la similitud de la película con todas las demás películas
#     sim_scores = list(enumerate(cosine_sim[idx]))
    
#     # Ordenar las películas según su similitud y seleccionar las 5 más similares
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    
#     # Obtener los índices de las películas recomendadas
#     movie_indices = [i[0] for i in sim_scores]
    
#     # Devolver los títulos de las películas recomendadas
#     return list(Df["title"].iloc[movie_indices])
   