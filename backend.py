import requests
import base64

info_pelicula = list[dict]

TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"


def consultar_peliculas(url_base:str,headers:str)->info_pelicula:

    try:

        info_peliculas = requests.get(url_base + "/movies", headers = headers)

    except:

        print("Error en la conexión")

    return info_peliculas


def consultar_sinopsis(url_base:str,movie_id:str,headers:str)->dict:

    try:

        sinopsis_peliculas = requests.get(url_base + "/movies"+ movie_id, headers = headers)

    except:

        print("Error en la conexión")

    return sinopsis_peliculas
    

def consultar_posters(url_base:str,id:str,headers:str)->bytes:

    try:

        poster_request = requests.get(url_base + "/posters" + id, headers = headers) #consulto
        
        poster_b64 = (poster_request.json()["poster_image"].split(",")[1])# extraigo el b64

        poster_utf_8= poster_b64.encode("utf-8") # lo paso a binario

        poster_bytes = base64.b64decode(poster_utf_8) # lo paso a bytes

    except:

        print("Error en la conexión")

    return poster_bytes


def descargar_poster(poster_bytes):
    

    with open ("Payaso.png","wb") as f:
        f.write(poster_bytes)


def consultar_snacks(url_base:str,headers:str)->dict:

    try:

        sinopsis_peliculas = requests.get(url_base + "/snacks", headers = headers)

    except:

        print("Error en la conexión")

    return sinopsis_peliculas
    

def consultar_proyecciones(url_base:str,movie_id:str,headers:str)->list:

    try:

        sinopsis_peliculas = requests.get(url_base + movie_id + "/cinemas", headers = headers)

    except:

        print("Error en la conexión")

    return sinopsis_peliculas
    

def consultar_info_cines(url_base:str,movie_id:str,headers:str)->info_cines:

    try:

        sinopsis_peliculas = requests.get(url_base + movie_id + "/cinemas", headers = headers)

    except:

        print("Error en la conexión")

    return sinopsis_peliculas
    

def main():

    headers={"Authorization" : TOKEN}

    url_base ="http://vps-3701198-x.dattaweb.com:4000"

    info_peliculas= consultar_peliculas(url_base,headers)

    print(info_peliculas.json())

    poster_bytes = consultar_posters(url_base,"/12",headers=headers)

    descargar_poster(poster_bytes)

main()
