import os
import cv2
import time
import random
import qrcode
import base64
import tkinter
import requests
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw,ImageFont

TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"
HEADERS:dict = {"Authorization" : TOKEN}
URL_BASE:str = "http://vps-3701198-x.dattaweb.com:4000"
PRECIO_ENTRADAS = 4000


def es_par(numero:int) -> int:
    auxiliar:int = 0
    if numero % 2 != 0:
        auxiliar = 1
    return auxiliar

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
    return sinopsis_peliculas.json()

def cargar_imagenes_poster(url_base:str, headers:dict, id_poster:str):
    poster_request = requests.get(url_base + "/posters/" + id_poster, headers = headers).json()
    poster_b64 = poster_request["poster_image"].split(",")[1]
    decoded = base64.decodebytes(poster_b64.encode("utf-8"))
    if not os.path.exists('poster_peliculas'):
        os.makedirs('poster_peliculas')
    with open(f'poster_peliculas/poster{id_poster}.png', 'wb') as f:
        f.write(decoded)


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

    peliculas_x_cine = requests.get(url_base + "/cinemas/" + cinema_id + "/movies", headers = headers)

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


def completar_info_cine(url_base:str,headers:str)->list[dict]:
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
            "peliculas":{
                "1": {info_pelicula}
                "2":{info_pelicula} ...
            }
        },
        {
            "cinema_id":"2",
            "location":"Abasto",
            "peliculas":{
                "1": {info_pelicula}
                "2":{info_pelicula} ...
            }
        },
        {
            "cinema_id":"3",
            "location":"Puerto Madero",
            "peliculas":{
                "1": {info_pelicula}
                "2":{info_pelicula} ...
            }
        }
    ]
    """
    peliculas_x_cine = completar_peliculas_x_cine(url_base,headers)
    info_cine = consultar_info_cines(url_base,headers) #consulto API
    for cine in info_cine:
        for cine_peliculas_x_cine in peliculas_x_cine:
            if cine["cinema_id"]  == cine_peliculas_x_cine["cinema_id"]:
                peliculas_cine_obtenido = {}
                for peliculas in cine_peliculas_x_cine["has_movies"]:
                    info_pelicula = consultar_sinopsis(url_base,"/" + peliculas ,headers)
                    info_pelicula.pop("id")
                    info_pelicula.pop("poster_id")
                    info_pelicula["available_seats"]= cine["available_seats"]
                    peliculas_cine_obtenido[peliculas] = info_pelicula
                cine.pop("available_seats")
                cine["peliculas"] = peliculas_cine_obtenido
    return info_cine


"""
#######################################################################################################################
                                        BATERíA DE FUNCIONES RESERVA 
#######################################################################################################################
"""


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

def generar_codigo_qr(string_generador:str) -> None:
    imagen = qrcode.make(string_generador)
    imagen.save("qrcode.png")

def generar_pdf_código_e_id_qr(id_codigo_qr:str):
    nombre_pdf:str = "completar"
    imagen:Image = Image.open('qrcode.png').convert('RGB')
    draw = ImageDraw.Draw(imagen)
    texto:str = f"ID codigoQR: {id_codigo_qr}"
    posiciones:tuple[int] = (150, 10)#coordenadas x,y
    color:tuple[int] = (0, 0, 0)#color negro
    tipo_letra:ImageFont = ImageFont.truetype('arial.ttf', 16)
    draw.text(posiciones, texto, fill=color, font=tipo_letra)
    os.remove("qrcode.png")
    if not os.path.exists("archivos_pdf"):
        os.makedirs("archivos_pdf")
    imagen.save(os.path.join("archivos_pdf", f"{nombre_pdf}.pdf"))


"""
#######################################################################################################################
                                                    FRONTEND
#######################################################################################################################
"""

def Encabezado(location: str, pantalla: tkinter) -> None:
    tkinter.Label(pantalla,
                text = f"CINEMA {location}",
                font = "Mincho 20",
                bg = 'gold3',
                fg = "#242424"
                ).grid(row=0, column=0, columnspan=2, pady=10)

def Snack(pantalla_reserva):
    #Esta es la informacion que debera recibir de la API
    #--------------------------------------------------- 
    snacks = {"doritos": "2500.00", "popcorn_xxl": "4300.00"}
    #--------------------------------------------------- 
    tkinter.Label(pantalla_reserva,
                text = "ESTOS SON LOS SNACKS DISPONIBLES:",
                font = "Rockwell 12"
                ).place(x = 20, y = 340, height = 17)
    i = 0
    for n in snacks:
        tkinter.Label(pantalla_reserva,
                    text = f"{n} : {snacks[n]}",
                    font = "Rockwell 11"
                    ).place(x = 70, y = 370 + i*20, height = 15)
        i += 1
    tkinter.Label(pantalla_reserva,
                text = "INGRESE EL SNACK:",
                font = "Rockwell 12"
                ).place(x = 20, y = 540, height = 17)
    pantalla_reserva.ingresar_cant_entradas = tkinter.Entry(pantalla_reserva
                                                ).place(x = 330, y = 540, width= 230)
    tkinter.Label(pantalla_reserva,
                text = "INGRESE LA CANTIDAD:",
                font = "Rockwell 12"
                ).place(x = 20, y = 580, height = 17)
    pantalla_reserva.ingresar_cant_entradas = tkinter.Entry(pantalla_reserva
                                                ).place(x = 330, y = 580, width= 230)

    pantalla_reserva.boton_comprar = tkinter.Button(pantalla_reserva,
                                                    text = "COMPRAR",
                                                    font = "Rockwell 20",
                                                    bg = 'gold3'
                                                    ).place(x = 210, y = 620)


def Pantalla_Reserva(dato_cine, id_pelicula) -> None:
    pantalla_reserva = tkinter.Toplevel()
    pantalla_reserva.geometry("576x720")
    pantalla_reserva.resizable(0, True)
    pantalla_reserva.focus()
    pantalla_reserva.grab_set()
    pantalla_reserva.title(f"CINEMA{dato_cine['location']} - Pantalla Reserva")
    Encabezado(dato_cine['location'], pantalla_reserva)
    
    tkinter.Label(pantalla_reserva,
                text = "INGRESE LA CANTIDAD DE ENTRADAS:",
                font = "Rockwell 12"
                ).place(x = 20, y = 130, height = 17)
    ingresar_cant_entradas = tkinter.Entry(pantalla_reserva).place(x = 330, y = 130, width= 230)
    boton_comprar = tkinter.Button(pantalla_reserva,
                                                    text = "COMPRAR",
                                                    font = "Rockwell 20",
                                                    bg = 'gold3'
                                                    ).place(x = 210, y = 170)
    
    bton_agregar_snacks= tkinter.Button(pantalla_reserva,
                                                text = "AÑADIR SNACK",
                                                font = "Rockwell 20",
                                                bg = 'gold3',
                                                command=lambda:Snack(pantalla_reserva)
                                                ).place(x = 170, y = 250)


def Pantalla_Secundaria(dato_cine:dict, id_pelicula:str) -> None:
    datos_pelicula:dict = dato_cine["peliculas"][id_pelicula]
    name:str = datos_pelicula["name"]
    synopsis:str = datos_pelicula["synopsis"]
    gender:str = datos_pelicula["gender"]
    duration:str = datos_pelicula["duration"]
    actors:str = datos_pelicula["actors"]
    directors:str = datos_pelicula["directors"]
    rating:str = datos_pelicula["rating"]

    pantalla_secundaria:tkinter.Toplevel = tkinter.Toplevel()
    pantalla_secundaria.geometry("700x720")
    pantalla_secundaria.resizable(0, True)
    pantalla_secundaria.focus()
    pantalla_secundaria.grab_set()
    
    pantalla_secundaria.title(f"CINEMA{dato_cine['location']} - Pantalla Pelicula")
    Encabezado(dato_cine['location'], pantalla_secundaria)
    
    tkinter.Label(pantalla_secundaria,
                text = name,
                font = "Rockwell 15"
                ).place(x = 20, y = 130, height = 17)
    tkinter.Label(pantalla_secundaria,
                text = f"Duración: {duration}",
                font = "Rockwell 12",
                ).place(x = 40, y = 160, height = 15)
    tkinter.Label(pantalla_secundaria,
                text = f"Actores: {directors}",
                font = "Rockwell 12"
                ).place(x = 40, y = 190, height = 17)
    tkinter.Label(pantalla_secundaria,
                text = f"Directores: {actors}",
                font = "Rockwell 12"
                ).place(x = 40, y = 220, height = 17)
    tkinter.Label(pantalla_secundaria,
                text = f"Género: {gender}",
                font = "Rockwell 12"
                ).place(x = 40, y = 250, height = 15)
    tkinter.Label(pantalla_secundaria,
                text = f"Clasificación: {rating}",
                font = "Rockwell 12",
                fg = 'deeppink4'
                ).place(x = 360, y = 250, height = 15)
    
    tkinter.Label(pantalla_secundaria,
                text = "SINOPSIS",
                font = "Rockwell 15"
                ).place(x = 20, y = 310, height = 17)
    letra: int = 0
    for n in range(7):
        tkinter.Label(pantalla_secundaria,
                    text = synopsis[letra*n :65 + letra*n],
                    font = "Rockwell 11"
                    ).place(x = 40, y = 340 + n*20, height = 15)
        letra = 65
    
    boton_volver = tkinter.Button(pantalla_secundaria,
                            text = "Volver a pantalla principal",
                            font = "Rockwell 9",
                            command = pantalla_secundaria.destroy
                            ).place(x = 420, y = 105)
    
    boton_reservar = tkinter.Button(pantalla_secundaria,
                            text = "Reservar",
                            font = "Rockwell 20",
                            bg = 'gold3',
                            command = lambda:Pantalla_Reserva(dato_cine, id_pelicula)
                            ).place(x = 410, y = 600)

def nombres_peliculas_x_cine(id_peliculas:list[str]) -> list[str]:
    peliculas_cine_consultado:list[str] = []
    peliculas_totales:list[dict] = consultar_peliculas(URL_BASE, HEADERS)
    for id_pelicula in id_peliculas:
        peliculas_cine_consultado.append(peliculas_totales[int(id_pelicula) - 1]["name"])
    return peliculas_cine_consultado

def validar_ingreso(botones:list[tkinter.Button], poster_ref:list, id_posters_cine:list[str], pelicula_ingresada:str) -> None:
    peliculas_cine:list[str] = nombres_peliculas_x_cine(id_posters_cine)
    if pelicula_ingresada.upper() in peliculas_cine:
        posicion_pelicula_elegida = peliculas_cine.index(pelicula_ingresada.upper())
        id_primer_pelicula:str = id_posters_cine[0]
        id_pelicula_elegida:str = id_posters_cine[posicion_pelicula_elegida]
        imagen_primer_pelicula:ImageTk.PhotoImage = ImageTk.PhotoImage(file=f"poster_peliculas/poster{id_primer_pelicula}.png")
        imagen_pelicula_elegida:ImageTk.PhotoImage = ImageTk.PhotoImage(file=f"poster_peliculas/poster{id_pelicula_elegida}.png")
        id_posters_cine[0] = id_pelicula_elegida
        id_posters_cine[posicion_pelicula_elegida]:str = id_primer_pelicula
        poster_ref[0] = imagen_pelicula_elegida
        poster_ref[posicion_pelicula_elegida] = imagen_primer_pelicula
        botones[0].config(image=imagen_pelicula_elegida)
        botones[posicion_pelicula_elegida].config(image=imagen_primer_pelicula)
    else:
        messagebox.showwarning("validar peliculas ingresada", f"Ingrese películas validas: {peliculas_cine}")

def limitar_barra_desplazamiento(canvas:tkinter.Canvas) -> None:
        canvas.configure(scrollregion=canvas.bbox('all'))

def crear_boton_buscar_pelicula(nuevo_comando) -> None:
    boton_busqueda:tkinter.Button = tkinter.Button(text="Buscar", command=nuevo_comando)
    boton_busqueda.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

def crear_cuadro_buscar_pelicula() -> tkinter.Entry:
    cuadro_entrada:tkinter.Entry = tkinter.Entry()
    cuadro_entrada.insert(0, "Ingrese película...")
    cuadro_entrada.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    return cuadro_entrada

def crear_canvas():
    cuadro_de_lienzo:tkinter.Canvas = tkinter.Canvas(bg="black", width=435, height=600)
    cuadro_de_lienzo.configure(highlightbackground='black')
    cuadro_de_lienzo.grid(row=1, column=0, columnspan=2, pady=5)
    return cuadro_de_lienzo

def crear_barra_desplazamiento(canvas:tkinter.Canvas) -> None:
    scrollbar:ttk.Scrollbar = ttk.Scrollbar(orient="vertical", command=canvas.yview)
    style:ttk.Style = ttk.Style()
    style.theme_use('default')
    style.configure("TScrollbar", background="black")
    style.map("TScrollbar", background=[("active", "black")])
    scrollbar.grid(row=1, column=2, sticky=tkinter.N+tkinter.S, pady=5)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda event: limitar_barra_desplazamiento(canvas))

def crear_botones_posters(dato_cine:dict, id_posters:list, botones:list, posters_ref:list, canvas:tkinter.Canvas) -> None:
    for i in range(len(id_posters)):
        poster:ImageTk.PhotoImage = ImageTk.PhotoImage(file=f"poster_peliculas/poster{id_posters[i]}.png")
        posters_ref.append(poster)
        row:int = i // 2
        col:int = es_par(i)
        nuevo_comando = lambda i=i: Pantalla_Secundaria(dato_cine, id_posters[i])
        boton_poster:tkinter.Button = tkinter.Button(canvas, image=posters_ref[i], command=nuevo_comando)
        canvas.create_window((col * 215 + 10, row * 302), window=boton_poster, anchor='nw')
        botones.append(boton_poster)

def caracterizar_pantalla_principal(pantalla_principal:tkinter.Tk, dato_cine:dict) -> None:
    pantalla_principal.geometry("460x740")
    pantalla_principal.resizable(0, True)
    pantalla_principal.config(bg="black")
    pantalla_principal.title(f"CINEMA{dato_cine['location']} - Pantalla Principal")
    Encabezado(dato_cine['location'], pantalla_principal)

def Pantalla_Principal(dato_cine:dict, id_posters_cine:list[str]) -> None:
    pantalla_principal:tkinter.Tk = tkinter.Tk()
    caracterizar_pantalla_principal(pantalla_principal, dato_cine)
    posters_ref:list[ImageTk.PhotoImage] = []
    botones:list[tkinter.Button] = []
    cuadro_de_lienzo:tkinter.Canvas = crear_canvas()
    crear_barra_desplazamiento(cuadro_de_lienzo)
    pelicula_buscada:tkinter.Entry = crear_cuadro_buscar_pelicula()
    comando_boton_buscar = lambda: validar_ingreso(botones, posters_ref, id_posters_cine, pelicula_buscada.get())
    crear_boton_buscar_pelicula(comando_boton_buscar)
    crear_botones_posters(dato_cine, id_posters_cine, botones, posters_ref, cuadro_de_lienzo)
    pantalla_principal.mainloop()

def calcular_id_sede_cine(datos_cines:dict) -> str:
    id_cine:int = random.randint(1, len(datos_cines))
    return id_cine

def cargar_posters_cine(id_posters_cine:list[str])-> None:
    for id_pelicula in id_posters_cine:
        cargar_imagenes_poster(URL_BASE, HEADERS, id_pelicula)

def main()->None:
    datos_cines:list[dict] = completar_info_cine(URL_BASE, HEADERS)
    id_cine:int = calcular_id_sede_cine(datos_cines)
    dato_cine:dict = datos_cines[id_cine - 1]
    id_posters_cine:list[str] = list((dato_cine["peliculas"]).keys())
    cargar_posters_cine(id_posters_cine)
    Pantalla_Principal(dato_cine, id_posters_cine)
main()