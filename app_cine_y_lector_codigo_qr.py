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
import functools

TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"
HEADERS:dict = {"Authorization" : TOKEN}
URL_BASE:str = "http://vps-3701198-x.dattaweb.com:4000"
PRECIO_ENTRADAS = 4000
TAMANIO_PANTALLA = '650x730'

FONDO_COLOR = 'Gray25'
LETRA_COLOR = 'Light gray'
MARCO_COLOR = 'gold3'
ENCABEZADO_COLOR = 'deeppink4'

TITULO_FONT = 'Rockwell 16'
BOTON_FONT = 'Rockwell 14'
TEXTO_FONT = 'Rockwell 11'
LIST_FONT = 'Rockwell 10'
TITULO_BOTON_FONT = "Rockwell 9"

def es_par(numero:int) -> int:
    auxiliar:int = 0
    if numero % 2 != 0:
        auxiliar = 1
    return auxiliar

def intercambiar_posiciones(lista, posición1, posicion2) -> None:
    aux = lista[posición1]
    lista[posición1] = lista[posicion2]
    lista[posicion2] = aux

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


def consultar_peliculas(url_base:str,headers:dict)->list:
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
    """
    PRE:Url_base, headers, id_poster tienen que estar definidos.
    POST:Guarda las imagenes de las peliculas consultadas a la api, en una carpeta llamada posters, los
        nombres quedarán respecto de su id y en formato png(ejm: "poster_1.png").
    """
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

def consultar_info_cines(url_base:str,headers:dict)->list:
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
    

def consultar_peliculas_x_cine(url_base:str,cinema_id:str,headers:dict)->list:
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

def incializar_snack_adquiridos(snacks:dict)->dict:

    snack_adquiridos={}

    for snack in snacks.items():
        snack_adquiridos[snack[0]] = 0

    return  snack_adquiridos

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

    snack_adquiridos[snack_adquirido] += cantidad
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
    for snack_adquirido in snacks_adquiridos.items():
        for snack in snacks.items():
            if snack_adquirido[0] == snack[0]:
                adicion += (float(snack[1]) * snack_adquirido[1]) 
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
def generar_info_qr(nombre_pelicula:str, cantidad_entradas:int, total_consumido:int)->str:
    """
    PRE:
    id_qr:
    nombre_pelicula: dato introducido por el cliente
    ubicacion_totem: depende de la ubicación del totem, tiene que coincidir con el dela primera 
    pantalla del programa
    cantidad_entradas: dato introducido por el cliente
    POS:
    info_qr: información a encriptar en el código qr
    info_qr = "timestamp_compra + nombre_pelicula + str(cantidad_entradas) + total_consumido"
    """
    timestamp_compra = time.strftime("%d %B %Y %H:%M:%S",time.localtime()) #"%d %B %Y %H:%M:%S" -> formato fecha y hora
    return ("+").join([timestamp_compra, nombre_pelicula, str(cantidad_entradas), str(total_consumido)])

def generar_codigo_qr(string_generador:str) -> None:
    """
    PRE:String_generador tiene que estar definido.
    POST:Crea una imagen de código QR, respecto del string_generador recibido.
    """
    imagen:qrcode.make = qrcode.make(string_generador)
    imagen.save("qrcode.png")

def generar_pdf_código_e_id_qr(id_codigo_qr:str):
    """
    PRE:Id_codigo_qr tiene que estar definido.
    POST:Modifica la imagen del codigo qr de nombre "qrcode.png" agregandole el id_codigo_qr recibido,
        para luego guadar dicha imagen en un pdf en la carpeta archivos_pdf, además de que elimina la
        imagen del qr modificado, ya que esta no se usará. 
    """
    nombre_pdf:str = f"{id_codigo_qr}"#información que se calculará respecto del id_codigo_qr y lo recibido de la app cine.
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


def finalizar_operacion(pantalla_principal, nombre_pelicula,cantidad_entradas, total_consumido):
    string_generador = generar_info_qr(nombre_pelicula,cantidad_entradas, total_consumido)
    id_codigo_qr = calcular_id_codigo_QR(string_generador)
    string_generador = f"{id_codigo_qr}+{string_generador}"
    generar_codigo_qr(string_generador)
    generar_pdf_código_e_id_qr(id_codigo_qr)
    pantalla_principal.destroy()
    crear_archivo_strings_generadores(string_generador)
    messagebox.showinfo("Ventana de información", "Se generará un archivo pdf con los datos de la compra.")


"""
#######################################################################################################################
                                                    FRONTEND
#######################################################################################################################
"""

def Encabezado(location: str, pantalla: tkinter) -> None:
    """
    PRE:Location y pantalla tienen que estar definidas.
    POST:Crea y configura una etiqueta en la parte superior de la pantalla
        de tal forma que será usado como encabezado.
    """
    tkinter.Label(pantalla,
                text = f"CINEMA {location}",
                font = "Mincho 20",
                bg = 'gold3',
                fg = "#242424"
                ).grid(row=0, column=0, columnspan=2, pady=10)

def Boton_regreso(pantalla:tkinter, fila:int = None, columna:int = None) -> None:
    """
    PRE:Pantalla, fila y columna tienen que estar definidos
    POST:Crea un botón y configura un botón que se elimina la panatalla en la que se
        encuentre ubicado, al hacerlo click.
    """
    boton_regreso = tkinter.Button(pantalla, text = "Volver", font = BOTON_FONT,
                                    bg = MARCO_COLOR, command = pantalla.destroy)
    boton_regreso.grid(row = fila, column = columna)

"""
#######################################################################################################################
                                                    PANTALLA CHECKOUT
#######################################################################################################################
"""

def Configuracion(pantalla: tkinter) -> None:
    pantalla.geometry(TAMANIO_PANTALLA)
    pantalla.configure(bg = FONDO_COLOR)
    pantalla.resizable(0, True)
    pantalla.focus()
    pantalla.grab_set()


def Checkout(pantalla_principal, cant_tickets,location,list_snack,snacks,nombre_pelicula) -> None:
    
    pantalla_checkout = tkinter.Toplevel()
    Configuracion(pantalla_checkout)
    
    Encabezado(location, pantalla_checkout)    
    pantalla_checkout.title(f"CINEMA{location} - Pantalla Checkout")

    subtotal_entradas=adicion_entradas(cant_tickets,PRECIO_ENTRADAS)

    subtotal_snack= adicion_snack(list_snack,snacks)

    precio_total=total_consumido(subtotal_snack,subtotal_entradas)
    
    label_listado_titulo = tkinter.Label(pantalla_checkout, text = "SE COMPRO:", font = TITULO_FONT, bg = FONDO_COLOR,
                                    fg = LETRA_COLOR)
    label_listado_titulo.grid(row = 2, column = 0, ipady = 20, columnspan = 2, sticky = "w")

    label_listado_1 = tkinter.Label(pantalla_checkout, text = f"Tickets: {cant_tickets}".upper(), font = LIST_FONT,
                    bg = FONDO_COLOR, fg = LETRA_COLOR)
    label_listado_1.grid(row = (3), column = 0, sticky = "e")

    i = 0
    for n in list_snack:
        label_listado_2 = tkinter.Label(pantalla_checkout, text = f"{n}: {list_snack[n]}".upper(), font = LIST_FONT,
                    bg = FONDO_COLOR, fg = LETRA_COLOR)
        label_listado_2.grid(row = (4 + i), column = 0, sticky = "e")
        i += 1
    
    
    label_precio = tkinter.Label(pantalla_checkout, text = "PRECIO TOTAL:", font = TITULO_FONT, bg = FONDO_COLOR,
                                    fg = LETRA_COLOR)
    label_precio.grid(row = 15, column = 0, ipady = 20, columnspan = 2, sticky = "w")

    label_precio_total = tkinter.Label(pantalla_checkout, text = f"{precio_total}$", font = TITULO_FONT, bg = FONDO_COLOR,
                                    fg = LETRA_COLOR)
    label_precio_total.grid(row = 15, column = 1,)

    decoracion =  tkinter.Frame(pantalla_checkout, width = 576, height = 5, bg = FONDO_COLOR)
    decoracion.grid(column = 0, row = 20, ipady = 20, columnspan = 2)
    
    Boton_regreso(pantalla_checkout, 21, 0)
    pagar = lambda: finalizar_operacion(pantalla_principal,nombre_pelicula,cant_tickets,precio_total)
    
    boton_comprar_entradas = tkinter.Button(pantalla_checkout, text = "Pagar", font = BOTON_FONT,
                                    bg = MARCO_COLOR,command=pagar)
    boton_comprar_entradas.grid(row = 21, column = 1)

"""
#######################################################################################################################
                                                PANTALLA RESERVA
#######################################################################################################################
"""

def actualizar_cantidad_snack(pantalla_reserva,snacks_adquiridos):
    i = 0
    for n in snacks_adquiridos:
        label_listado = tkinter.Label(pantalla_reserva, text = f"{n} ({snacks_adquiridos[n]})".upper(), font = LIST_FONT,
                    bg = FONDO_COLOR, fg = LETRA_COLOR)
        label_listado.grid(row = (7 + i), column = 0)
        i += 1

def Snack(pantalla_reserva,snacks,snacks_adquiridos) -> None:
    label_listado_titulo = tkinter.Label(pantalla_reserva, text = "LOS SNACKS DISPONIBLES SON:", font = TITULO_FONT, bg = FONDO_COLOR,
                                    fg = LETRA_COLOR)
    label_listado_titulo.grid(row = 6, column = 0, ipady = 20, columnspan = 2, sticky = "w")
    
    actualizar_cantidad_snack(pantalla_reserva,snacks_adquiridos)

    i = 0
    for n in snacks:
        label_listado = tkinter.Label(pantalla_reserva, text = f"{snacks[n]}".upper(), font = LIST_FONT,
                    bg = FONDO_COLOR, fg = LETRA_COLOR)
        label_listado.grid(row = (7 + i), column = 1)
        i += 1

    i = 0
    for n in snacks_adquiridos:
        compra = functools.partial (comprar_snak,snacks_adquiridos,n,1)# functools partial permite crear la funcion en el momento lambda lo crea a mediad que se necesita
        
        boton_entradas = tkinter.Button(pantalla_reserva, font = 'Rockwell 11', bg = FONDO_COLOR,
                                    fg = LETRA_COLOR, text = "+1", command=compra)
        boton_entradas.grid(row = (7 + i), column = 2, sticky="e")
        i += 1
    
    decoracion =  tkinter.Frame(pantalla_reserva, width = 576, height = 5, bg = FONDO_COLOR)
    decoracion.grid(column = 0, row = 18, ipady = 20, columnspan = 2)

    actualizar =lambda : actualizar_cantidad_snack(pantalla_reserva,snacks_adquiridos)
    
    boton_comprar_snack = tkinter.Button(pantalla_reserva, text = "Añadir al Carrito", font = BOTON_FONT,
                                    bg = MARCO_COLOR,command = actualizar)
    boton_comprar_snack.grid(row = 19, column = 1)

def reservar_entradas(cant_entradas,entradas_disponibles,id_pelicula,dato_cine):
    
    if revisar_disponibilidad_asientos(cant_entradas,entradas_disponibles):

        dato_cine["peliculas"][id_pelicula]["available_seats"] -= cant_entradas


def actualizar_cant_entradas(pantalla_reserva,cant_entradas):

    cant_entradas[0] += 1

    label_entradas = tkinter.Label(pantalla_reserva, text = f"Entradas ({PRECIO_ENTRADAS}): {cant_entradas}", font = LIST_FONT,
                                    bg = FONDO_COLOR, fg = LETRA_COLOR)
    label_entradas.grid(row = 3, column = 0, sticky = "e")


def Pantalla_Reserva(pantalla_principal, dato_cine, id_pelicula) -> None:
    location = dato_cine["location"]
    cant_entradas = [0]
    entradas_disponibles = dato_cine["peliculas"][id_pelicula]["available_seats"]
    nombre_pelicula = dato_cine["peliculas"][id_pelicula]["name"]
    
    pantalla_reserva = tkinter.Toplevel()
    Configuracion(pantalla_reserva)
    
    Encabezado(location, pantalla_reserva)    
    pantalla_reserva.title(f"CINEMA{location} - Pantalla Reserva")
    
    label_entradas = tkinter.Label(pantalla_reserva, text = f"LAS ENTRADAS DISPONIBLES SON ({entradas_disponibles}):", font = TITULO_FONT,
                                    bg = FONDO_COLOR, fg = LETRA_COLOR)
    label_entradas.grid(row = 2, column = 0, ipady = 20, columnspan = 2, sticky = "w")
    
    label_entradas = tkinter.Label(pantalla_reserva, text = f"Entradas ({PRECIO_ENTRADAS}): {cant_entradas}", font = LIST_FONT,
                                    bg = FONDO_COLOR, fg = LETRA_COLOR)
    label_entradas.grid(row = 3, column = 0, sticky = "e")

    actualizar= lambda : actualizar_cant_entradas(pantalla_reserva ,cant_entradas)
    
    boton_entradas = tkinter.Button(pantalla_reserva, font = 'Rockwell 11', bg = FONDO_COLOR,
                                    fg = LETRA_COLOR, text = "+1", command = actualizar)
    boton_entradas.grid(row = 3, column = 1)
    
    decoracion =  tkinter.Frame(pantalla_reserva, width = 576, height = 5, bg = FONDO_COLOR)
    decoracion.grid(column = 0, row = 4, ipady = 20, columnspan = 2)
    
    
    #Esta es la informacion recibida por la API
    #---------------------------------------------------    
    snacks = consultar_snacks(URL_BASE,HEADERS)
    snacks_adquiridos = incializar_snack_adquiridos(snacks)
    #---------------------------------------------------

    comando_snack = lambda: Snack(pantalla_reserva,snacks,snacks_adquiridos)

    boton_snack = tkinter.Button(pantalla_reserva, text = "Añadir Snacks", font = BOTON_FONT,
                                    bg = MARCO_COLOR, command = comando_snack)
    boton_snack.grid(row = 6, column = 0)
    
    decoracion =  tkinter.Frame(pantalla_reserva, width = 576, height = 5, bg = FONDO_COLOR)
    decoracion.grid(column = 0, row = 20, ipady = 20, columnspan = 2)
    
    Boton_regreso(pantalla_reserva, 21, 0)

    checkout = lambda: Checkout(pantalla_principal,cant_entradas[0],location,snacks_adquiridos,snacks,nombre_pelicula)
    
    boton_comprar_entradas = tkinter.Button(pantalla_reserva, text = "Finalizar Compra", font = BOTON_FONT,
                                    bg = MARCO_COLOR, command = checkout)
    boton_comprar_entradas.grid(row = 21, column = 1)

"""
#######################################################################################################################
                                        FUNCIONES DE LA PANTALLA SECUNDARIA
#######################################################################################################################
"""

def configurar_pantalla_secundaria(pantalla:tkinter.Toplevel, datos_cine:dict) -> None:
    """
    PRE:Pantalla y datos_cine tienen que estar definidos.
    POST:Configura las características básicas(tamaño, color, etc) de la pantalla secundaria.
    """
    pantalla.geometry("500x790")
    pantalla.config(bg="#242424")
    pantalla.resizable(0, True)
    pantalla.grab_set()
    pantalla.title(f"CINEMA{datos_cine['location']} - Pantalla Pelicula")

def boton_reservar(pantalla:tkinter.Toplevel, comando):
    """
    PRE:Pantalla y comando tienen que estar definidos.
    POST:Crea y configura un botón para poder reservar la película elegida previamene, llevandote
        a la pantalla de reserva.
    """
    tkinter.Button(pantalla,
                            text = "Reservar",
                            font = "Rockwell 14",
                            bg = 'gold3',
                            command = comando
                            ).grid(row= 4, column=1)

def crear_descripcion_sinopsis(datos_pelicula:dict) ->str:
    """
    PRE:Datos pelicula tiene que estar definido.
    POST:Crea y devuelve una cadena con información(duración, actores, género, etc) de la pelicula.
    """
    descripcion:str = f"""
    Duración: {datos_pelicula["duration"]}
    Directores: {datos_pelicula["directors"]}
    Actores: {datos_pelicula["actors"]}
    Género: {datos_pelicula["gender"]}"""
    return descripcion

def agregar_sinopsis_completa_al_frame(frame:tkinter.Frame, datos_pelicula:dict) -> None:
    """
    PRE:Frame y datos_pelicula tienen que estar definidos.
    POST:Agrega información de la pélicula(nombre, actores, sinopsis, etc) al cuadro frame.
    """
    descripcion = crear_descripcion_sinopsis(datos_pelicula)
    nombre = tkinter.Label(frame, text=datos_pelicula["name"], font="Rockwell 15", bg="#C5C5ED", wraplength=350)
    nombre.grid(row=0, column=0, sticky="w")
    descripcion = tkinter.Label(frame, text=descripcion, font="Rockwell 12", bg="#C5C5ED", justify="left", wraplength=350)
    descripcion.grid(row=1, column=0, sticky="w")
    clasificacion = tkinter.Label(frame,text=f"Clasificación: {datos_pelicula['rating']}", font="Rockwell 12", bg="#C5C5ED", fg='deeppink4')
    clasificacion.grid(row=2, column=0, sticky="e")
    subtitulo_sinopsis = tkinter.Label(frame, text="SINOPSIS", font="Rockwell 15", bg="#C5C5ED",)
    subtitulo_sinopsis.grid(row=3, column=0, sticky="w")
    sinopsis = tkinter.Label(frame, text=datos_pelicula["synopsis"], font="Rockwell 12", bg="#C5C5ED", justify="left", wraplength=350)
    sinopsis.grid(row=4, column=0, sticky="w", padx=10)

def Pantalla_Secundaria(pantalla_principal, dato_cine:dict, id_pelicula:str) -> None:
    """
    PRE:Dato_cine e id_pelicula tienen que estar definidos.
    POST:Crea una pantalla con información de la película(nombre, actores, sinopsis, etc) y
        dos botones(uno para regresar y otro para reservar entradas de la película).
    """
    datos_pelicula:dict = dato_cine["peliculas"][id_pelicula]
    pantalla_secundaria:tkinter.Toplevel = tkinter.Toplevel()
    configurar_pantalla_secundaria(pantalla_secundaria, dato_cine)
    Encabezado(dato_cine['location'], pantalla_secundaria)
    sala= tkinter.Label(pantalla_secundaria, text=f"SALA {id_pelicula}", font="Rockwell 15", bg="#C5C5ED", wraplength=350)
    sala.grid(row=1, column=0, padx=10, sticky="w")
    Boton_regreso(pantalla_secundaria, 2, 1)
    frame = tkinter.Frame(pantalla_secundaria, bg="#C5C5ED")
    agregar_sinopsis_completa_al_frame(frame, datos_pelicula)
    frame.grid(row=3, column=0, padx=10)
    comando = lambda:Pantalla_Reserva(pantalla_principal, dato_cine, id_pelicula)
    boton_reservar(pantalla_secundaria, comando)

"""
#######################################################################################################################
                                        FUNCIONES DE LA PANTALLA PRINCIPAL
#######################################################################################################################
"""

def completar_info_cine(url_base:str,headers:str)->list:
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

def nombres_peliculas_x_cine(id_peliculas:list) -> list:
    """
    PRE:Id_peliculas y la función consultar_pelicula tiene que estar definidas y/o creadas .
    POST:Devuelve una lista con los nombres de todas las peliculas del cine en que se encuntra.
    """
    peliculas_cine_consultado:list[str] = []
    peliculas_totales:list[dict] = consultar_peliculas(URL_BASE, HEADERS)
    for id_pelicula in id_peliculas:
        peliculas_cine_consultado.append(peliculas_totales[int(id_pelicula) - 1]["name"])
    return peliculas_cine_consultado

def validar_ingreso(botones:list, poster_ref:list, id_posters_cine:list, pelicula_ingresada:str) -> None:
    """
    PRE:Botones, poster_ref, id_posters_cine, pelicula_ingresada tienen que estar definidos.
    POST:Devuelve un mensaje de alerta con los nombres de las películas validas si pelicula ingresada es incorrecta,
        pero si la pelicula ingresada es correcta, intercambia la lista id_posters y botones de la película en la primera 
        posición(respecto de todos los botones) con la película ingresada, de tal forma que la película que ingresó
        se vea al princípio de la ventana.
    """
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
    """
    PRE:Canvas tiene que estar definido.
    POST:Limita el rango del scrollbar, de tal forma que se mantenga dentro de los parametros
        del cuadro de canvas.
    """
    canvas.configure(scrollregion=canvas.bbox('all'))

def crear_boton_buscar_pelicula(comando) -> None:
    """
    PRE:Comando tiene que estar definido.
    POST:Crea un botón que enviará el nombre de la película que ingresó el usario, para luego ser buscado.
    """
    boton_busqueda:tkinter.Button = tkinter.Button(text="Buscar", command=comando)
    boton_busqueda.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

def crear_cuadro_buscar_pelicula() -> tkinter.Entry:
    """
    PRE:-
    POST:Crea un cuadro de entrada para el cual el usuario podrá ingresar la película que desea buscar.
    """
    cuadro_entrada:tkinter.Entry = tkinter.Entry()
    cuadro_entrada.insert(0, "Ingrese película...")
    cuadro_entrada.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    return cuadro_entrada

def crear_canvas() -> None:
    """
    PRE:-
    POST:Crea y configura las características básicas del cuadro de canvas.
    """
    cuadro_de_lienzo:tkinter.Canvas = tkinter.Canvas(bg="black", width=435, height=600)
    cuadro_de_lienzo.configure(highlightbackground='black')
    cuadro_de_lienzo.grid(row=1, column=0, columnspan=2, pady=5)
    return cuadro_de_lienzo

def crear_barra_desplazamiento(canvas:tkinter.Canvas) -> None:
    """
    PRE:Canvas tiene que estar definido.
    POST:Crea y configura un 'scrollbar' para poder mostrar las imagenes restantes ubicadas en el cuadro de canvas.
    """
    scrollbar:ttk.Scrollbar = ttk.Scrollbar(orient="vertical", command=canvas.yview)
    style:ttk.Style = ttk.Style()
    style.theme_use('default')
    style.configure("TScrollbar", background="black")
    style.map("TScrollbar", background=[("active", "black")])
    scrollbar.grid(row=1, column=2, sticky=tkinter.N+tkinter.S, pady=5)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda event: limitar_barra_desplazamiento(canvas))

def crear_botones_posters(pantalla_principal, dato_cine:dict, id_posters:list, botones:list, posters_ref:list, canvas:tkinter.Canvas) -> None:
    """
    PRE:Dato_ine, id_posters, botones, posters_ref y canvas tienen que estar definidos.
    POST:Crea y confifura los botones para que tengan las imagenes de los posters de las peliculas del cine
        en que se encuentra.
    """
    for i in range(len(id_posters)):
        poster:ImageTk.PhotoImage = ImageTk.PhotoImage(file=f"poster_peliculas/poster{id_posters[i]}.png")
        posters_ref.append(poster)
        row:int = i // 2
        col:int = es_par(i)
        nuevo_comando = lambda i=i: Pantalla_Secundaria(pantalla_principal, dato_cine, id_posters[i])
        boton_poster:tkinter.Button = tkinter.Button(canvas, image=posters_ref[i], command=nuevo_comando)
        canvas.create_window((col * 215 + 10, row * 302), window=boton_poster, anchor='nw')
        botones.append(boton_poster)

def configurar_pantalla_principal(pantalla_principal:tkinter.Tk, dato_cine:dict) -> None:
    """
    PRE:Pantalla principal y dato_cine tiene que estar definidos.
    POST:Define las características básicas de la pantalla principal.
    """
    pantalla_principal.geometry("460x740")
    pantalla_principal.resizable(0, True)
    pantalla_principal.config(bg="black")
    pantalla_principal.title(f"CINEMA{dato_cine['location']} - Pantalla Principal")
    Encabezado(dato_cine['location'], pantalla_principal)

def Pantalla_Principal(dato_cine:dict, id_posters_cine:list) -> None:
    """
    PRE:Datos_cine e id_posters_cine tiene que estar definidos.
    POST:Crea un ventana con los posters de todas las películas ubicadas en botones
        que los llevará a otra ventana secundaria al hacer click en dichos posters.
    """
    pantalla_principal:tkinter.Tk = tkinter.Tk()
    configurar_pantalla_principal(pantalla_principal, dato_cine)
    posters_ref:list[ImageTk.PhotoImage] = []
    botones:list[tkinter.Button] = []
    cuadro_de_lienzo:tkinter.Canvas = crear_canvas()
    crear_barra_desplazamiento(cuadro_de_lienzo)
    pelicula_buscada:tkinter.Entry = crear_cuadro_buscar_pelicula()
    comando_boton_buscar = lambda: validar_ingreso(botones, posters_ref, id_posters_cine, pelicula_buscada.get())
    crear_boton_buscar_pelicula(comando_boton_buscar)
    crear_botones_posters(pantalla_principal, dato_cine, id_posters_cine, botones, posters_ref, cuadro_de_lienzo)
    pantalla_principal.mainloop()

def calcular_id_sede_cine(datos_cines:dict) -> str:
    """
    PRE:Datos cine debe estar definido.
    POST:Devuelve una posicion aleatoria respecto del total de elementos que contenga datos_cine.
    """
    id_cine:int = random.randint(1, len(datos_cines))
    return id_cine

def cargar_posters_cine(id_posters_cine:list)-> None:
    """
    PRE:Id_posters_cine tiene que estar definido
    POST:Envia cada id(str) a la función cargar_imagenes_posters para poder guardarlos.
    """
    for id_pelicula in id_posters_cine:
        cargar_imagenes_poster(URL_BASE, HEADERS, id_pelicula)

def app_cine()->None:
    datos_cines:list[dict] = completar_info_cine(URL_BASE, HEADERS)#Contiene la información completa de todos los cines
    id_cine:int = calcular_id_sede_cine(datos_cines)
    dato_cine:dict = datos_cines[id_cine - 1]#Contiene toda la información del cine obtenido aleatoriamente
    id_posters_cine:list[str] = list((dato_cine["peliculas"]).keys())
    cargar_posters_cine(id_posters_cine)
    Pantalla_Principal(dato_cine, id_posters_cine)
"""
#######################################################################################################################
                                        App de Lectura Código QR
#######################################################################################################################
"""
def buscar_nombres_archivos_pdf():
    pdf_filenames = []
    for filename in os.listdir("archivos_pdf"):
        if filename.endswith('.pdf'):
            pdf_filenames.append(os.path.splitext(filename)[0])
    return pdf_filenames

def calcular_id_codigo_QR(string_generado_id_qr:str) -> str:
    """
    PRE:String_generador tiene que estar definido.
    POST:Crea un cadena encriptada 'id_codigo_qr', usando el string_generador.
    """
    id_codigo_qr:str = ""
    lista_datos:list[str] = string_generado_id_qr.split('+')
    for dato in lista_datos:
        id_codigo_qr += dato[:2]
    return id_codigo_qr

def crear_archivo_strings_generadores(string_generador):
    with open("strings_generados.txt", "a") as texto:
        texto.write(string_generador+"\n")

def crear_agregar_datos_archivo_txt(datos_compra) -> None:
    """
    PRE:Datos_compra tiene que estar definido.
    POST:Crea un arhvico.txt si no está creado y/o agrega los datos de la compra:
        'timestamp,Id_QR,nombre_película,cant_entradas,total_consumido'.
    """
    with open("Ingresos.txt", "a") as texto:
        texto.write(datos_compra+"\n")

def buscar_string_generador(id_ingresado:str) -> str:
    strings_generadores = []
    string_generador = ""
    with open("strings_generados.txt", 'r', encoding='utf-8') as archivo:
            strings_generadores = archivo.readlines()
    for string in strings_generadores:
        datos_compra = string.split("+")
        datos_compra.pop(0)
        cadena_aux = "+".join(datos_compra)
        if calcular_id_codigo_QR(cadena_aux) == id_ingresado:
            string_generador = string
    compras_txt = string_generador.split("+")
    intercambiar_posiciones(compras_txt, 0, 1)
    string_generador = ",".join(compras_txt)
    return string_generador

def validar_id_codigo_qr(id_ingresado:str, ventana_id_qr) -> None:
    """
    PRE:Id_ingresado, ventana_id_qr e id_qr tienen que estar definidos.
    POST:Muestra un cuadro de mensaje, que dirá que el Id_qr es valiod o invalido, si es valido
        llamará a la función crear_agregar_datos_archivos_txt.
    """
    id_de_qrs:list[str] = buscar_nombres_archivos_pdf()
    mensaje:str = "ID QR válido, se generará un archivo(Ingresos.txt) de los compras de los clientes ingresados al cine."
    if id_ingresado in id_de_qrs:
        ventana_id_qr.destroy()
        messagebox.showinfo("Ventana de información", mensaje)
        string_generador = buscar_string_generador(id_ingresado)
        crear_agregar_datos_archivo_txt(string_generador)#Le pasaremos los datos recibidos como argumento.
    else:
        messagebox.showwarning("Ventanada de alartes", "ID del QR invalido!")

def abrir_ventana_id_QR() -> None:
    """
    PRE:-
    POST:Crea y abre una ventana con un un mensaje de ingrese id del código qr, un cuadro de entrada, y un botón para
        poder enviar dicha información ingresada, a la función validar_id_codigo_qr.
    """
    ventana_id_qr:tkinter.Toplevel = tkinter.Toplevel()
    ventana_id_qr.config(bg="#242424")#gris oscuro
    ventana_id_qr.geometry("200x70")
    ventana_id_qr.resizable(False, False)
    etiqueta:tkinter.Label = tkinter.Label(ventana_id_qr, text = "Ingresa el ID del codigo QR", bg="#C5C5ED")#C5C5ED, es azul magenta claro
    etiqueta.pack()
    cuadro_texto:tkinter.Entry = tkinter.Entry(ventana_id_qr)
    cuadro_texto.pack()
    nuevo_comando = lambda:validar_id_codigo_qr(cuadro_texto.get(), ventana_id_qr)
    boton_ingreso:tkinter.Button = tkinter.Button(ventana_id_qr, text="Ingresar", bg="#C5C5ED", command=nuevo_comando)
    boton_ingreso.pack()

def desactivar_escaneo_por_tiempo_limite(datos:list) -> tuple[bool]:
    """
    PRE:Datos tiene que estar definido.
    POST:Devuelve camara_activada y detector_qr con valor False, si se excedió el tiempo limite(10segundos)
        lo que llavará a apagar la webcam, y devuelve True respecto de las mismas variables, si no se excede
        del tiempo límite.
    """
    tiempo_limite, tiempo_inicio, camara_activada, detecto_qr = datos[0], datos[1], datos[2], datos[3]
    tiempo_actual:int = cv2.getTickCount()
    tiempo_transcurrido:float = (tiempo_actual - tiempo_inicio) / cv2.getTickFrequency()#obtener la frecuencia del temporizador
    if tiempo_transcurrido > tiempo_limite:
        camara_activada:bool = False
        detecto_qr:bool = False
    return camara_activada, detecto_qr

def modificar_dato_decodificado(dato_decodificado:str):
    nueva_cadena = ""
    datos_compra = dato_decodificado.split("+")
    intercambiar_posiciones(datos_compra, 0, 1)
    nueva_cadena = ",".join(datos_compra)
    return nueva_cadena

def mostrar_mensaje_escaneo_validado(detecto_qr:bool, dato_decodificado:str) -> None:
    """
    PRE:Detecto_qr y dato_decodificado tiene que estar definido.
    POST:Muestra un cuadro de mensaje, mostrando que se alcanzó el tiempo límite
        o mostrando 'dato_decodificado, se generó archivo ingresos.txt', para luego llamar
        a la función crear_agregar_datos_archivos_txt(), todo de acuerdo a si detecto_qr
        es False o True, respectivamente.
    """
    if detecto_qr == False:
        messagebox.showwarning("Ventanada de alartes", "Alcanzaste el limite de tiempo")
    else:
        mensaje:str = f"""
        Dato decodificado:\n
        {dato_decodificado}\n
        Se generará un archivo(Ingresos.txt) de los compras de los clientes ingresados al cine.
                    """
        messagebox.showinfo("Ventana de información", mensaje)
        dato_decodificado = modificar_dato_decodificado(dato_decodificado)
        crear_agregar_datos_archivo_txt(dato_decodificado)#Le pasaremos los datos recibidos como argumento.

def escanear_codigo_qr() -> None:
    """
    PRE:-.
    POST:Accede a la webcam predeterminda, lo prende y muestra una ventana de la imagen que perciba,
        y lo mantiene activa durante 10 segundos, tiempo en el cual tratará de detectar el código qr
        que perciba la webcam, si detecta código qr lo decodificará y mostrará un mensaje del código
        decodificado y generará un archivo Ingresos.txt con el mensaje decodificado para luego cerrar
        la ventanas que se generaron y apagar la webcam, si no detecta ningún código qr en esos 10(s),
        se cerrará la ventana generada y apagará la webcam.
    """
    tiempo_limite:int = 10 # segundos
    tiempo_inicio:int = cv2.getTickCount()#Obtiene el tiempo actual en milisegundos
    camara_activada:bool = True
    detecto_qr:bool = True
    dato_decodificado:str = ""
    camara:cv2.VideoCapture = cv2.VideoCapture(0)#Inicializa camara(el "0" es para que eliga la camara predeterminada)
    while camara_activada:
        fotograma = (camara.read())[1]#imagenes que captura la camara
        if cv2.waitKey(1) == ord('s'): camara_activada = False
        detector_qr = cv2.QRCodeDetector()# Intenta detectar un código QR en el fotograma
        dato_decodificado:str =  detector_qr.detectAndDecode(fotograma)[0]
        if len(dato_decodificado) > 0:
            camara_activada = False
        else:
            cv2.imshow("Capturador de imagenes", fotograma)# Muestra el fotograma en una ventana
        datos:list = [tiempo_limite, tiempo_inicio, camara_activada, detecto_qr]
        camara_activada, detecto_qr = desactivar_escaneo_por_tiempo_limite(datos)
    camara.release()
    cv2.destroyAllWindows()
    mostrar_mensaje_escaneo_validado(detecto_qr, dato_decodificado)

def crear_botones_pantalla_principal() -> None:
    """
    PRE:-
    POST:Crea dos botones, que al hacer click, uno llamará a la función escanear_codigo_qr,
        y el otro llamará a la función abrir_ventana_id_Qr.
    """
    boton_scaner:tkinter.Button = tkinter.Button(text="ScanearQR", bg="#C5C5ED", command=escanear_codigo_qr)
    boton_scaner.grid(row=2,column=0)
    nuevo_comando = lambda:abrir_ventana_id_QR()
    boton_digitar:tkinter.Button = tkinter.Button(text="DigitarQR", bg="#C5C5ED", command=nuevo_comando)
    boton_digitar.grid(row=2,column=2)

def crear_ventana_principal() -> None:
    """
    PRE:Los iconos e imagenes que se usen tienen que estar descargados y ubicados
        en la misma carpeta que se ejecuta este archivo.py.
    POST:Crea una ventana con un titulo, una etiqueta como encabezado, 2 imagenes y dos botones
        debajo de estos, para la cual uno llamará a la función escanear_codigo_qr() y el otro
        llamará a la función abrir_ventana_id_Qr().
    """
    ventana:tkinter.Tk = tkinter.Tk()
    ventana.iconbitmap("iconos_ventanas/scan.ico")
    ventana.geometry("400x200")
    ventana.resizable(False, False)
    ventana.config(bg="#242424")#color gris oscuro
    etiqueta_principal:tkinter.Label = tkinter.Label(ventana, text = "Lector de codigo QR", bg="#C5C5ED")#C5C5ED color azul magenta claro
    etiqueta_principal.grid(row=0,column=1)
    imagen_camara:tkinter.PhotoImage = tkinter.PhotoImage(file="iconos_ventanas/camara.png")
    etiqueta_imagen:tkinter.Label = tkinter.Label(image=imagen_camara,bg="#242424")
    etiqueta_imagen.grid(row=1,column=0)
    imagen_binaria:tkinter.PhotoImage = tkinter.PhotoImage(file="iconos_ventanas/binario.png")
    etiqueta_imagen:tkinter.Label = tkinter.Label(image=imagen_binaria,bg="#242424")
    etiqueta_imagen.grid(row=1,column=2)
    crear_botones_pantalla_principal()
    ventana.mainloop()

def app_lector_Qr() -> None:
    crear_ventana_principal()


"""
#######################################################################################################################
                                        FUNCIONES DEL MAIN
#######################################################################################################################
"""


def main():
    """
    PRE:Solo abri una aplicación a la vez, descomenta la que desea usar y comente la que no usará.
    POST:Abre la aplicación que eligió.
    """
    #app_cine()
    app_lector_Qr()
main()