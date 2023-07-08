from fastapi import FastAPI
import pandas as pd

#Cargamos el dataframe
df = pd.read_csv(r"C:\Users\Alfonso\Desktop\PI01\datasets_unidos_ETL.csv", dtype={"columna35": str, "columna40": str}, low_memory=False)

app = FastAPI()

@app.get("/")
def read_root():
    return {"API": "Endpoints disponibles: peliculas_idioma, peliculas_duracion, franquicia, peliculas_pais, productoras_exitosas, get_director"}

@app.get("/peliculas_idioma")
def peliculas_idioma(Idioma: str):
    count = df[df['original_language'] == Idioma].shape[0]
    return f"{count} películas fueron estrenadas en {Idioma}"

@app.get("/peliculas_duracion")
def peliculas_duracion(Pelicula: str):
    pelicula_data = df[df['title'] == Pelicula].iloc[0]
    duracion = pelicula_data['runtime']
    año = pelicula_data['release_year']
    return f"Duración: {duracion} minutos. Año: {año}"

@app.get("/franquicia/{Franquicia}")
def franquicia(Franquicia: str):
    peliculas_franquicia = df[df["name_belongs_to_collection"] == Franquicia]
    cantidad_peliculas = len(peliculas_franquicia)
    ganancia_total = peliculas_franquicia["revenue"].sum() / 1000000.0
    ganancia_promedio = peliculas_franquicia["revenue"].mean() / 1000000.0
    return f"La franquicia {Franquicia} posee {cantidad_peliculas} películas, una ganancia total de {ganancia_total} millones de dólares y una ganancia promedio de {ganancia_promedio} millones de dólares."

@app.get("/peliculas_pais")
def peliculas_pais(Pais: str):
    count = df[df['name_production_countries'] == Pais].shape[0]
    return f"Se produjeron {count} películas en el país {Pais}"

@app.get("/productoras_exitosas")
def productoras_exitosas(Productora: str):
    productora_data = df[df['name_production_companies'] == Productora]
    peliculas_count = productora_data.shape[0]
    revenue_total = productora_data['revenue'].sum()
    return f"La productora {Productora} ha tenido un revenue de {revenue_total} en {peliculas_count} películas"

@app.get("/get_director")
def get_director(nombre_director: str):
    directores = df.loc[df['job_crew'] == 'Director', 'name_crew']
    
    if nombre_director not in directores.values:
        return {"error": "El director no se encuentra en la lista"}
    
    director_data = df[df['name_crew'] == nombre_director]
    
    peliculas = []
    for _, row in director_data.iterrows():
        pelicula_info = {
            "title": row['title'],
            "release_date": row['release_date'],
            "return": row['return'],
            "budget": row['budget'],
            "revenue": row['revenue']
        }
        peliculas.append(pelicula_info)
    
    return peliculas

#RECOMENDACION

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def recomendacion(titulo: str):
    #Obtener el índice de la película de entrada
    index = df[df['title'] == titulo].index[0]

    #Crear una instancia de TfidfVectorizer y ajustarla a los títulos de las películas
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['title'])

    #Calcular la similitud del coseno entre las películas
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    #Obtener los puntajes de similitud de la película de entrada con todas las demás películas
    scores = list(enumerate(cosine_sim[index]))

    #Ordenar los índices de las películas según los puntajes de similitud en orden descendente
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    #Nombres de las 5 películas más similares
    top_scores = sorted_scores[1:6]
    recommended_movies = [df['title'][i[0]] for i in top_scores]

    return recommended_movies