import requests
import base64
import os
import qrcode
import time

from PIL import Image, ImageDraw,ImageFont

TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"
HEADERS={"Authorization" : TOKEN}
URL_BASE ="http://vps-3701198-x.dattaweb.com:4000"

PRECIO_ENTRADAS = 2000

VERSION_QR = 1
ERROR_CORRECCION = qrcode.constants.ERROR_CORRECT_L
TAMANIO_QR=15
BORDE_QR = 2
COLOR_FONDO_QR = "white"
COLOR_QR="black"

"""
#######################################################################################################################
                                        BATERíA DE FUNCIONES PARA CONSUMIR LA API
                            Están en el mismo orden que el archivo "API Reference(1).PDF"
#######################################################################################################################
"""
def gestion_error_conexion(request)->str:

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
                                     BATERíA DE FUNCIONES ESTRUCTURAS DE DATOS  
#######################################################################################################################
"""

def completar_peliculas_x_cine(url_base:str,headers:str):
    """
    PRE: 
    url_base: url base como se encuentra en archivo "Trabajo Práctico N°2 - Algoritmos I - Lanzillotta. (1).PDF",
    url_base ="http://vps-3701198-x.dattaweb.com:4000"
    headers: TOKEN formateado, headers={"Authorization" : TOKEN}
    POS:
    peliculas_x_cine_completa: estructura de datos inspirada en la definida por los docentes en archivo, "API Reference(1).PDF"
    [
        {
            "cinema_id":"1",
            "has_movies":[
                "1",
                "2",
                "3",
            
            ]
        }
        {
            "cinema_id":"2",
            "has_movies":[
                "1",
                "2",
                "3",
            
            ]
        }
        {
            "cinema_id":"3",
            "has_movies":[
                "1",
                "2",
                "3",
            
            ]
        }
    ]
    """

    info_cines= consultar_info_cines(url_base,headers)

    peliculas_x_cine=[]

    for cine in info_cines:

        peliculas_x_cine.append( consultar_peliculas_x_cine (url_base,"/"+cine["cinema_id"],headers)[0] ) 
    
    return peliculas_x_cine


def completar_info_cine(peliculas_x_cine:list[dict],url_base:str,headers:str)->list[dict]:
    """
    PRE:
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
    peliculas_x_cine: estructura de datos definida en la función completar_peliculas_x_cine"
    [
        {
            "cinema_id":"1",
            "has_movies":[
                "1",
                "2",
                "3",
            
            ]
        }
        {
            "cinema_id":"2",
            "has_movies":[
                "1",
                "2",
                "3",
            
            ]
        }
        {
            "cinema_id":"3",
            "has_movies":[
                "1",
                "2",
                "3",
            
            ]
        }
    ]
    POS:
    info_cines_completa: estructura de datos basada en la definida por los docentes en archivo, "API Reference(1).PDF"
    [
        {
            "cinema_id":"1",
            "location":"Caballito",
            "available_seats":32
            "1":32
            "2":32 ...
            "id_movie":available_seats
        },
        {
            "cinema_id":"2",
            "location":"Abasto",
            "available_seats":40
            "1":32
            "2":32 ...
            "id_movie":available_seats
        },
        {
            "cinema_id":"3",
            "location":"Puerto Madero",
            "available_seats":25
            "1":32
            "2":32 ...
            "id_movie":available_seats
        }
    ]
    """

    info_cine = consultar_info_cines(url_base,headers) #consulto API

    for cine in info_cine:

        for cine_peliculas_x_cine in peliculas_x_cine:
        
            if cine["cinema_id"]  == cine_peliculas_x_cine["cinema_id"]:

                for peliculas in cine_peliculas_x_cine["has_movies"]:

                    cine[peliculas] = cine["available_seats"]
    
    return info_cine


def crear_cines(url_base,headers):

    peliculas_x_cine = completar_peliculas_x_cine(url_base,headers)

    info_peliculas = completar_info_cine(peliculas_x_cine,url_base,headers)

    return info_peliculas


"""
#######################################################################################################################
                                        BATERíA DE FUNCIONES RESERVA 
#######################################################################################################################
"""

def buscar_pelicula(info_peliculas:list[dict],nombre_pelicula:str)->str:
    """
    PRE:
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
    nombre_pelicula: nombre película introducido por el cliente
    POS:
    movie_id: id de la película que introdujo el cliente
    """

    for pelicula in info_peliculas:

        if nombre_pelicula == pelicula["name"]:
            id_pelicula = pelicula["movie_id"]

    return id_pelicula


def buscar(info_peliculas:list[dict],nombre_pelicula:str)->str:
    """
    PRE:
    nombre_pelicula: nombre de la pelicula introducido por el cliente en el buscador
    POS: 
    movie_id: id de la pelicula, "0" pelicula no encontrada
    """

    try:

        return buscar_pelicula(info_peliculas,nombre_pelicula)
        
    except:

        return "0"
    

def revisar_disponibilidad_asientos(cantidad_entradas:int,asientos_disponibles:int)->bool:
    """
    PRE:
    cantidad_entradas: cantidad de entradas compradas
    asientos_disponibles: asientos disponibles, "available_seats"
    POS:
    True si hay asientos disponibles
    """

    if ( asientos_disponibles - cantidad_entradas ) > 0:
        return True
    else:
        return False


def reservar_pelicula(info_cines_completa:list[dict],cantidad_entradas:int,id_cine:str,id_movie:str)->None:
    """
    PRE:
    info_cines_completa: estructura de datos definida por los docentes en archivo, "API Reference(1).PDF"
    [
        {
            "cinema_id":"1",
            "location":"Caballito",
            "available_seats":32
            "1":32
            "2":32
        },
        ...
    ]
    cantidad_entradas: cantidad de entradas compradas
    id_cine: id del cine, cinema_id
    POS:
    Actualiza info_cines disminuyendo las entradas disponibles
    """

    for cine in info_cines_completa:

        if cine["cinema_id"] == id_cine:
            cine[id_movie] -= cantidad_entradas


"""
#######################################################################################################################
                                        BATERíA DE FUNCIONES COMPRA 
#######################################################################################################################
"""
def adicion_entradas(cantidad_entradas:int, precio_entradas:float)->float:
    """
    PRE:
    cantidad_entradas: cantidad de entradas compradas por el cliente
    PRECIO_ENTRADAS: precio de una entrada
    POS:
    Precio total por entradas
    """

    return cantidad_entradas * precio_entradas


def comprar_snak(snack_adquiridos:dict,snack_adquirido:str,cantidad:int)->dict:
    """
    PRE:
    snack_adquirido: nombre snack introducido por el usuario
    cantidad: cantidad de snack_adquirido
    POS:
    snacks_adquiridos: estructura de datos definida por los docentes en archivo, "API Reference(1).PDF"
    {
        "doritos": "2"
        "popcorn_xxl": "1"
        "Coca_xxl": "2"
    }
    """

    snack_adquiridos[snack_adquirido] = cantidad

    return snack_adquiridos

def adicion_snack(snacks_adquiridos:dict,snacks:dict)->float:
    """
    PRE:
    snacks_adquiridos: estructura de datos similar a la definida por los docentes en archivo, "API Reference(1).PDF"
    {
        "doritos": "2"
        "popcorn_xxl": "1"
    }
    snacks: estructura de datos definida por los docentes en archivo, "API Reference(1).PDF"
    {
        "doritos": "2250"
        "popcorn_xxl": "1000"
    }
    POS:
    adicion: suma del precio de todos los snacks
    """

    adicion = 0 
    
    for snack_adquirido in snacks_adquiridos.item():
        
        for snack in snacks.item():
            
            if snack_adquirido[0] == snack[0]:
                adicion += (snacks[1] * snack_adquirido[1]) 
    
    return adicion
    

def total_consumido(precio_snack:float,precio_entradas:float)->float:
    """
    PRE:
    precio_snack: suma precios de los snacks comprados por el cliente
    precio_entradas: suma precios de los entradas comprados por el cliente
    POS:
    precio total de la compra
    """

    return precio_entradas + precio_snack


"""
#######################################################################################################################
                                        BATERíA DE FUNCIONES QR 
#######################################################################################################################
"""
def generar_info_qr(nombre_pelicula:str,ubicacion_totem:str,cantidad_entradas:int)->str:
    """
    PRE:
    id_qr:
    nombre_pelicula: dato introducido por el cliente
    ubicacion_totem: depende de la ubicación del totem, tiene que coincidir con el dela primera 
    pantalla del programa
    cantidad_entradas: dato introducido por el cliente
    POS:
    info_qr: información a encriptar en el código qr
    info_qr = “ID_QR + pelicula + ubicación_totem + cantidad_entradas + timestamp_compra”
    """

    timestamp_compra = time.strftime("%d %B %Y %H:%M:%S",time.localtime()) #"%d %B %Y %H:%M:%S" -> formato fecha y hora

    return (" ").join[nombre_pelicula,ubicacion_totem,cantidad_entradas,timestamp_compra]


def crear_qr(info_qr:str)->None:
    """
    PRE:
    info_qr: información a encriptar en el código qr
    info_qr = “ID_QR + pelicula + ubicación_totem + cantidad_entradas + timestamp_compra”
    POS:
    Esta función crea una imagen en formato png
    """

    qr = qrcode.QRCode(version=VERSION_QR,error_correction=ERROR_CORRECCION,box_size=TAMANIO_QR,border=BORDE_QR)
    """
    El parámetro de versión es un número entero del 1 al 40 que controla el tamaño del Código QR (el más pequeño,
     versión 1, es una matriz de 21x21). Establezca en Ninguno y use el parámetro de ajuste al crear el código para determinar
     esto automáticamente.
    
     El parámetro error_correction controla la corrección de errores utilizada para el código QR. Los siguientes cuatro
     Las constantes están disponibles en el paquete qrcode:

         ERROR_CORRECT_L
         Se pueden corregir alrededor del 7% o menos de los errores.

         ERROR_CORRECT_M (predeterminado)
         Se pueden corregir alrededor del 15% o menos de los errores.

         ERROR_CORRECT_Q
         Se pueden corregir alrededor del 25% o menos de los errores.

         ERROR_CORRECT_H.
         Se pueden corregir alrededor del 30% o menos de los errores.

     El parámetro box_size controla cuántos píxeles tiene cada "cuadro" del código QR.

     El parámetro de borde controla cuántos cuadros de grosor debe tener el borde (el valor predeterminado es 4,
     que es el mínimo según las especificaciones).
    """

    qr.add_data(info_qr)

    img = qr.make_image(back_color=COLOR_FONDO_QR, fill_color=COLOR_QR)
    """
    fill_color y back_color pueden cambiar el fondo y el color de pintura del QR,
    cuando se utiliza la fábrica de imágenes predeterminada. Ambos parámetros aceptan tuplas de colores RGB.
    """

    qr.make(fit=True)
    """
    make(): este método con (fit = True) garantiza que se utilice toda la dimensión del código
    QR, aunque nuestros datos de entrada puedan caber en menos campos.
    """
    
    img.save("qrcode.png")


def main()->None:

    crear_cines(URL_BASE,HEADERS)

main()
