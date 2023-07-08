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
    director_data = df[(df['job_crew'] == "Director") & (df['name_crew'] == nombre_director)]
    peliculas = []
    for _, row in director_data.iterrows():
        pelicula_info = {
            "title": row['title'],
            "release_date": row['release_date'],
            "return": str(row['return']),
            "budget": str(row['budget']),
            "revenue": str(row['revenue'])
        }
        peliculas.append(pelicula_info)
    return peliculas