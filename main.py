from fastapi import FastAPI
import pandas as pd
import numpy as np

#Cargamos el dataframe
df = pd.read_csv(r"C:\Users\Alfonso\Desktop\PI01\dataset_final.csv", dtype={"columna35": str, "columna40": str}, low_memory=False)
df['title'].fillna('', inplace=True)
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
from sklearn.metrics.pairwise import cosine_similarity

# Paso 1: Calcular la matriz TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['title'])

# Paso 2: Calcular la matriz de similitud del coseno
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Ejemplo de uso de la matriz de similitud
input_movie_index = df.index[df['title'] == 'Toy Story']
movie_scores = similarity_matrix[input_movie_index]
similar_movie_indices = movie_scores.argsort()[0][::-1]
similar_movie_indices = similar_movie_indices[1:6]  # Excluye la misma película
recommended_movies = df.iloc[similar_movie_indices]['title'].tolist()
print(recommended_movies)

import nltk
nltk.download('punkt')
nltk.download('stopwords')

def recomendacion(titulo):
    # Encuentra el índice de la película en el DataFrame
    input_movie_index = df.index[df['title'] == titulo].item()

    # Calcula la similitud entre la película de entrada y todas las demás películas
    movie_scores = similarity_matrix[input_movie_index]

    # Ordena las películas según su similitud y selecciona las 5 películas con mayor puntuación
    similar_movie_indices = np.argsort(movie_scores)[::-1][:5]

    # Obtiene los títulos de las películas recomendadas
    recommended_movies = df.iloc[similar_movie_indices]['title'].tolist()

    # Devuelve la lista de películas recomendadas
    return recommended_movies