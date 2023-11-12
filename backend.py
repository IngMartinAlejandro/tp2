import requests
import base64
import os



TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

"""
#######################################################################################################################
                                        BATERíA DE FUNCIONES PARA CONSUMIR LA API
                            Están en el mismo orden que el archivo "API Reference(1).PDF"
#######################################################################################################################
"""
def gestion_error_conexion(request):

    if not request.ok: 

        print("Error en la conexión",request.status_code)

        return "Error" + str(request.status_code)


def consultar_peliculas(url_base:str,headers:dict)->list[dict]:
    """
    PRE: 
    url_base: url base como se encuentra en archivo "Trabajo Práctico N°2 - Algoritmos I - Lanzillotta. (1).PDF",
    url_base ="http://vps-3701198-x.dattaweb.com:4000"
    headers: TOKEN formateado, headers={"Authorization" : TOKEN}
    POS: 
    info_peliculas: estructura de datos definida por los docentes en archivo, "API Reference(1).PDF"
    [
        {
            "movie_id": "1",
            "name": "BOOGYMAN TU MIEDO ES REAL",
            "poster_id": "1"
    
    },
        {
            "movie_id": "2",
            "name": "COCO",
            "poster_id": "2"
    
    }
    ]
    """

    info_peliculas = requests.get(url_base + "/movies", headers = headers)

    gestion_error_conexion(info_peliculas)

    return info_peliculas.json()


def consultar_sinopsis(url_base:str,movie_id:str,headers:dict)->dict:
    """
    PRE: 
    url_base: url base como se encuentra en archivo "Trabajo Práctico N°2 - Algoritmos I - Lanzillotta. (1).PDF",
    url_base ="http://vps-3701198-x.dattaweb.com:4000"
    movie_id: definido por los docentes en "API Reference(1).PDF", en 1- Obtener información principal de todas las películas  
    movie_id = "/12"
    headers: TOKEN formateado, headers={"Authorization" : TOKEN}
    POS: 
    info_sinopsis: estructura de datos definida por los docentes en archivo, "API Reference(1).PDF"
    {
        'id': '12', 
        'poster_id': '12', 
        'release_date': '', 
        'name': 'LA MONJA 2', 
        'synopsis': '1956 - Francia. Un sacerdote es asesinado. Un mal se está extendiendo. La secuela del gran éxito mundial sigue a 
    la Hermana Irene cuando, una vez más, se encuentra cara a cara con Valak, la monja demonio . ', 
        'gender': 'Terror', 
        'duration': '109min', 
        'actors': 'Anna Popplewell, Bonnie Aarons, Taissa Farmiga', 
        'directors': 'Michael Chaves', 
        'rating': '+13'
    }
    """

    sinopsis_peliculas = requests.get(url_base + "/movies" + movie_id, headers = headers)

    gestion_error_conexion(sinopsis_peliculas)

    return sinopsis_peliculas.json()
    

def consultar_posters(url_base:str,poster_id:str,headers:str)->bytes:
    """
    PRE: 
    url_base: url base como se encuentra en archivo "Trabajo Práctico N°2 - Algoritmos I - Lanzillotta. (1).PDF",
    url_base ="http://vps-3701198-x.dattaweb.com:4000"
    movie_id: definido por los docentes en "API Reference(1).PDF", en 3- Obtener el poster de una película por ID  
    poster_id = "/12"
    headers: TOKEN formateado, headers={"Authorization" : TOKEN}
    POS: 
    poster_bytes: bytes de la imagen del poster en archivo.png
    """ 

    poster_request = requests.get(url_base + "/posters" + poster_id, headers = headers) #consulto
        
    poster_b64 = (poster_request.json()["poster_image"].split(",")[1])# extraigo el b64

    poster_utf_8= poster_b64.encode("utf-8") # lo paso a binario

    poster_bytes = base64.b64decode(poster_utf_8) # lo paso a bytes

    gestion_error_conexion(poster_request)

    return poster_bytes


def consultar_snacks(url_base:str,headers:str)->dict:
    """
    PRE: 
    url_base: url base como se encuentra en archivo "Trabajo Práctico N°2 - Algoritmos I - Lanzillotta. (1).PDF",
    url_base ="http://vps-3701198-x.dattaweb.com:4000"
    headers: TOKEN formateado, headers={"Authorization" : TOKEN}
    POS: 
    snacks: estructura de datos definida por los docentes en archivo, "API Reference(1).PDF"
    {
        "doritos": "2500.00"
        "popcorn_xxl": "4300.00"
    }
    """ 

    snacks = requests.get(url_base + "/snacks", headers = headers)

    gestion_error_conexion(snacks)

    return snacks.json()
    

def consultar_proyecciones(url_base:str,movie_id:str,headers:dict)->list:
    """
    PRE: 
    url_base: url base como se encuentra en archivo "Trabajo Práctico N°2 - Algoritmos I - Lanzillotta. (1).PDF",
    url_base ="http://vps-3701198-x.dattaweb.com:4000"
    movie_id: definido por los docentes en "API Reference(1).PDF", en 5- Obtener información de dónde se proyecta cada película   
    movie_id = "/12"
    headers: TOKEN formateado, headers={"Authorization" : TOKEN}
    POS: 
    proyecciones: estructura de datos definida por los docentes en archivo, "API Reference(1).PDF"
    [
        "1",
        "2",
        "3",
    ]
    """ 

    proyecciones = requests.get(url_base + "/movies" + movie_id + "/cinemas", headers = headers)

    gestion_error_conexion(proyecciones)

    return proyecciones.json()

    
def consultar_info_cines(url_base:str,headers:dict)->list[dict]:
    """
    PRE: 
    url_base: url base como se encuentra en archivo "Trabajo Práctico N°2 - Algoritmos I - Lanzillotta. (1).PDF",
    url_base ="http://vps-3701198-x.dattaweb.com:4000"
    headers: TOKEN formateado, headers={"Authorization" : TOKEN}
    POS: 
    info_cines: estructura de datos definida por los docentes en archivo, "API Reference(1).PDF"
    [
        {
            "cinema_id":"1",
            "location":"Caballito",
            "available_seats":32
        },
        {
            "cinema_id":"2",
            "location":"Abasto",
            "available_seats":40
        },
        {
            "cinema_id":"3",
            "location":"Puerto Madero",
            "available_seats":25
        }
    ]
    """ 

    info_cines = requests.get(url_base + "/cinemas", headers = headers)

    gestion_error_conexion(info_cines)

    return info_cines.json()
    

def consultar_peliculas_x_cine(url_base:str,cinema_id:str,headers:dict)->list[dict]:
    """
    PRE: 
    url_base: url base como se encuentra en archivo "Trabajo Práctico N°2 - Algoritmos I - Lanzillotta. (1).PDF",
    url_base ="http://vps-3701198-x.dattaweb.com:4000"
    cinema_id: definido por los docentes en "API Reference(1).PDF", en 7- Obtener películas proyectadas en un determinado cine   
    cinema_id = "/1"
    headers: TOKEN formateado, headers={"Authorization" : TOKEN}
    POS: 
    peliculas_x_cine: estructura de datos definida por los docentes en archivo, "API Reference(1).PDF"
    [
        {
            "cinema_id":"1",
            "has_movies":[
                "1",
                "2",
                "3",
            
            ]
        }
    ]
    """ 

    peliculas_x_cine = requests.get(url_base + "/cinemas" + cinema_id + "/movies", headers = headers)

    gestion_error_conexion(peliculas_x_cine)

    return peliculas_x_cine.json()


"""
#######################################################################################################################
                                        BATERíA DE FUNCIONES 
#######################################################################################################################
"""

def descargar_poster(poster_bytes:bytes)->None:
    """
    PRE:
    poster_bytes: bytes de la imagen del poster en archivo.png
    POS:
    Esta función escribe los bytes de la imagen en un archivo.png
    """
    
    if not os.path.exists("imagenes"):
        os.mkdir("imagenes")
    
    with open ("imagenes/poster.png","wb") as f:
        f.write(poster_bytes)


def main()->None:

    headers={"Authorization" : TOKEN}

    url_base ="http://vps-3701198-x.dattaweb.com:4000"


main()
