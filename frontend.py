import tkinter
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
FONDO_COLOR_QR = "white"
COLOR_QR="black"

TAMANIO_PANTALLA = '576x730'

FONDO_COLOR = 'Gray25'
LETRA_COLOR = 'Light gray'
MARCO_COLOR = 'gold3'
ENCABEZADO_COLOR = 'deeppink4'

TITULO_FONT = 'Rockwell 16'
BOTON_FONT = 'Rockwell 14'
TEXTO_FONT = 'Rockwell 11'
LIST_FONT = 'Rockwell 10'
TITULO_BOTON_FONT = "Rockwell 9"


def Encabezado(location: str, pantalla: tkinter) -> None:
    fondo_1 = tkinter.Frame(pantalla, width = 288, height = 80, bg = ENCABEZADO_COLOR)
    fondo_1.grid(column = 0, row = 0)
    fondo_2 = tkinter.Frame(pantalla, width = 288, height = 80, bg = ENCABEZADO_COLOR)
    fondo_2.grid(column = 1, row = 0)
    marco = tkinter.Frame(pantalla, width = 576, height = 25, bg = MARCO_COLOR)
    marco.grid(column = 0, row = 1, columnspan=2)
    titulo_cine = tkinter.Label(pantalla, text = f"CINEMA {location}", font = "Mincho 28", bg = ENCABEZADO_COLOR, fg = "white")
    titulo_cine.grid(column = 0, row = 0)   

def Checkout():
    #Esta es la informacion que debera recibir de la API
    #---------------------------------------------------    
    location = "Location"
    cant_tickets = 1
    list_snack = {"doritos": 4, "popcorn_xxl": 2}
    snacks = {"doritos": "2500.00", "popcorn_xxl": "4300.00"}
    precio_total = 45000
    #---------------------------------------------------
    pantalla_checkout = tkinter.Toplevel()
    pantalla_checkout.geometry(TAMANIO_PANTALLA)
    pantalla_checkout.configure(bg = FONDO_COLOR)
    pantalla_checkout.resizable(0, True)
    
    pantalla_checkout.focus()
    pantalla_checkout.grab_set()
    
    Encabezado(location, pantalla_checkout)    
    pantalla_checkout.title(f"CINEMA{location} - Pantalla Checkout")
    
    label_listado_titulo = tkinter.Label(pantalla_checkout, text = "SE COMPRO:", font = TITULO_FONT, bg = FONDO_COLOR,
                                   fg = LETRA_COLOR)
    label_listado_titulo.grid(row = 2, column = 0, ipady = 20, columnspan = 2, sticky = "w")
    label_listado_1 = tkinter.Label(pantalla_checkout, text = f"- {cant_tickets} : Tickets".upper(), font = LIST_FONT,
                    bg = FONDO_COLOR, fg = LETRA_COLOR)
    label_listado_1.grid(row = (3), column = 0, sticky = "e")
    i = 0
    for n in list_snack:
        label_listado_2 = tkinter.Label(pantalla_checkout, text = f"- {list_snack[n]} : {n}".upper(), font = LIST_FONT,
                    bg = FONDO_COLOR, fg = LETRA_COLOR)
        label_listado_2.grid(row = (4 + i), column = 0, sticky = "e")
        i += 1
    
    
    label_precio = tkinter.Label(pantalla_checkout, text = "PRECIO TOTAL:", font = TITULO_FONT, bg = FONDO_COLOR,
                                   fg = LETRA_COLOR)
    label_precio.grid(row = 10, column = 0, ipady = 20, columnspan = 2, sticky = "w")
    label_precio_total = tkinter.Label(pantalla_checkout, text = f"{precio_total}$", font = TITULO_FONT, bg = FONDO_COLOR,
                                   fg = LETRA_COLOR)
    label_precio_total.grid(row = 10, column = 1,)
       

    decoracion =  tkinter.Frame(pantalla_checkout, width = 576, height = 5, bg = FONDO_COLOR)
    decoracion.grid(column = 0, row = 20, ipady = 20, columnspan = 2)
    
    boton_comprar_entradas = tkinter.Button(pantalla_checkout, text = "Pagar", font = BOTON_FONT,
                                   bg = MARCO_COLOR)
    boton_comprar_entradas.grid(row = 21, column = 0, columnspan = 2)

def Snack(pantalla_reserva):
    #Esta es la informacion que debera recibir de la API
    #---------------------------------------------------    
    snacks = {"doritos": "2500.00", "popcorn_xxl": "4300.00"}
    cant_snacks = 0
    #---------------------------------------------------
    label_listado_titulo = tkinter.Label(pantalla_reserva, text = "LOS SNACKS DISPONIBLES SON:", font = TITULO_FONT, bg = FONDO_COLOR,
                                   fg = LETRA_COLOR)
    label_listado_titulo.grid(row = 4, column = 0, ipady = 20, columnspan = 2, sticky = "w")
    i = 0
    for n in snacks:
        label_listado = tkinter.Label(pantalla_reserva, text = f"{n} : {snacks[n]}".upper(), font = LIST_FONT,
                    bg = FONDO_COLOR, fg = LETRA_COLOR)
        label_listado.grid(row = (5 + i), column = 0, sticky = "e")
        i += 1

    label_entradas = tkinter.Label(pantalla_reserva, text = "EL SNACK A COMPRAR ES: ", font = TITULO_FONT, bg = FONDO_COLOR,
                                   fg = LETRA_COLOR)
    label_entradas.grid(row = 17, column = 0, ipady = 20, columnspan = 2, sticky = "w")
    cuadro_entrada = tkinter.Entry(pantalla_reserva, font = TEXTO_FONT)
    cuadro_entrada.insert(0, " Ingrese el Snack...")
    cuadro_entrada.grid(row = 17, column = 1)
    
    label_entradas = tkinter.Label(pantalla_reserva, text = F"CANTIDAD SNACKS: {cant_snacks}", font = TITULO_FONT, bg = FONDO_COLOR,
                                   fg = LETRA_COLOR)
    label_entradas.grid(row = 18, column = 0, ipady = 20, columnspan = 2, sticky = "w")
    boton_entradas = tkinter.Button(pantalla_reserva, font = BOTON_FONT, bg = FONDO_COLOR,
                                    fg = LETRA_COLOR, text = "Cantidad +1")
    boton_entradas.grid(row = 18, column = 1)

    boton_comprar_entradas = tkinter.Button(pantalla_reserva, text = "Añadir al Carrito", font = BOTON_FONT,
                                   bg = MARCO_COLOR)
    boton_comprar_entradas.grid(row = 19, column = 1)

def Pantalla_Reserva() -> None:
    #Esta es la informacion que debera recibir de la API
    #---------------------------------------------------    
    location = "Location"
    cant_entradas = 0
    #---------------------------------------------------
    pantalla_reserva = tkinter.Toplevel()
    pantalla_reserva.geometry(TAMANIO_PANTALLA)
    pantalla_reserva.configure(bg = FONDO_COLOR)
    pantalla_reserva.resizable(0, True)
    
    pantalla_reserva.focus()
    pantalla_reserva.grab_set()
    
    Encabezado(location, pantalla_reserva)    
    pantalla_reserva.title(f"CINEMA{location} - Pantalla Reserva")
    
    label_entradas = tkinter.Label(pantalla_reserva, text = F"CANTIDAD ENTRADAS: {cant_entradas}", font = TITULO_FONT, bg = FONDO_COLOR,
                                   fg = LETRA_COLOR)
    label_entradas.grid(row = 2, column = 0, ipady = 20, columnspan = 2, sticky = "w")
    
    boton_entradas = tkinter.Button(pantalla_reserva, font = BOTON_FONT, bg = FONDO_COLOR,
                                    fg = LETRA_COLOR, text = "Cantidad +1")
    boton_entradas.grid(row = 2, column = 1)
    
    boton_comprar_entradas = tkinter.Button(pantalla_reserva, text = "Añadir al Carrito", font = BOTON_FONT,
                                   bg = MARCO_COLOR)
    boton_comprar_entradas.grid(row = 3, column = 1)
    
    comando_snack = lambda: Snack(pantalla_reserva)
    boton_snack = tkinter.Button(pantalla_reserva, text = "Añadir Snacks", font = BOTON_FONT,
                                   bg = MARCO_COLOR, command = comando_snack)
    boton_snack.grid(row = 4, column = 0)
    
    decoracion =  tkinter.Frame(pantalla_reserva, width = 576, height = 5, bg = FONDO_COLOR)
    decoracion.grid(column = 0, row = 20, ipady = 20, columnspan = 2)
    
    boton_comprar_entradas = tkinter.Button(pantalla_reserva, text = "Finalizar Compra", font = BOTON_FONT,
                                   bg = MARCO_COLOR, command = Checkout)
    boton_comprar_entradas.grid(row = 21, column = 0, columnspan = 2)

def Pantalla_Secundaria() -> None:
    #Esta es la informacion que debera recibir de la API
    #---------------------------------------------------
    location = "Location"
    name = "BOOGEYMAN TU MIEDO ES REAL"
    synopsis = "Sadie Harper, una estudiante del colegio secundario y su hermana pequeña, Sawyer, están conmocionadas por la reciente muerte de su madre y no reciben mucho apoyo de su padre, Will, un terapeuta que está lidiando con su propio dolor. Cuando un paciente desesperado se presenta inesperadamente en su casa en busca de ayuda, deja tras de sí una aterradora entidad sobrenatural que se aprovecha de las familias y se alimenta del sufrimiento de sus víctimas."
    gender = "Terror"
    duration = "98min"
    actors = "Chris Messina, David Dastmalchian, Sophie Thatcher"
    directors = "Rob Savage"
    rating = "+13"
    #---------------------------------------------------
    pantalla_secundaria = tkinter.Toplevel()
    pantalla_secundaria.geometry(TAMANIO_PANTALLA)
    pantalla_secundaria.configure(bg = FONDO_COLOR)
    pantalla_secundaria.resizable(0, True)
    
    pantalla_secundaria.focus()
    pantalla_secundaria.grab_set()
    
    Encabezado(location, pantalla_secundaria)
    pantalla_secundaria.title(f"CINEMA{location} - Pantalla Pelicula")
    
    label_titulo = tkinter.Label(pantalla_secundaria, text = name, font = TITULO_FONT, 
                                 bg = FONDO_COLOR, fg = LETRA_COLOR)
    label_titulo.grid(row = 2, column = 0, ipady = 20, columnspan = 2, sticky = "w")
    
    label_info_5 = tkinter.Label(pantalla_secundaria, text = f"Género: {gender}", font = TEXTO_FONT, 
                                 fg = LETRA_COLOR, bg = FONDO_COLOR)
    label_info_5.grid(row = 3, column = 0)
     
    label_info_1 = tkinter.Label(pantalla_secundaria, text = f"Directores: {directors}", font = TEXTO_FONT, 
                                 fg = LETRA_COLOR, bg = FONDO_COLOR)
    label_info_1.grid(row = 3, column = 1)

    label_info_3 = tkinter.Label(pantalla_secundaria, text = f"Actores: {actors}", font = TEXTO_FONT, 
                                 bg = FONDO_COLOR, fg = LETRA_COLOR)
    label_info_3.grid(row = 4, columnspan=2)
    
    label_info_2 = tkinter.Label(pantalla_secundaria, text = f"Clasificación: {rating}", font = TEXTO_FONT, 
                                 fg = MARCO_COLOR, bg = FONDO_COLOR)
    label_info_2.grid(row = 5, column = 1)
    
    label_info_4 = tkinter.Label(pantalla_secundaria, text = f"Duración: {duration}", font = TEXTO_FONT, 
                                 fg = ENCABEZADO_COLOR, bg = FONDO_COLOR)
    label_info_4.grid(row = 5, column = 0)
    
    label_titulo_sinopsis = tkinter.Label(pantalla_secundaria, text = "SINOPSIS", font = TITULO_FONT,
                                          bg = FONDO_COLOR, fg = LETRA_COLOR)
    label_titulo_sinopsis.grid(row = 7, column = 0, ipady = 20, sticky="w")
    
    letra: int = 0
    for n in range(10):
        label_sinopsis = tkinter.Label(pantalla_secundaria, text = synopsis[letra*n :65 + letra*n], font = "Rockwell 11",
                                       bg = FONDO_COLOR, fg = LETRA_COLOR)
        label_sinopsis.grid(row = (8 + n), columnspan=2)
        letra = 65
        
    boton_regreso = tkinter.Button(pantalla_secundaria, text = "Volver a pantalla Anterior", font = BOTON_FONT,
                                   bg = MARCO_COLOR, command = pantalla_secundaria.destroy)
    boton_regreso.grid(row = 18, column = 0)
        
    boton_reserva = tkinter.Button(pantalla_secundaria, text = "Reservar", font = BOTON_FONT,
                                   bg = MARCO_COLOR, command = Pantalla_Reserva)
    boton_reserva.grid(row = 18, column = 1)

def Pantalla_Principal() -> None:
    #Esta es la informacion que debera recibir de la API
    #---------------------------------------------------
    location = "Location"
    peliculas_ids_disponibles = ["1", "2", "3", "4"]
    poster_1_id = "poster_1_id"
    poster_2_id = "poster_2_id"
    poster_3_id = "poster_3_id"
    poster_4_id = "poster_4_id"
    #---------------------------------------------------
    pantalla_principal = tkinter.Tk()
    pantalla_principal.geometry(TAMANIO_PANTALLA)
    pantalla_principal.configure(bg = FONDO_COLOR)
    pantalla_principal.resizable(0, True)

    Encabezado(location, pantalla_principal)
    pantalla_principal.title(f"CINEMA{location} - Pantalla Principal")
    
    cuadro_entrada = tkinter.Entry(pantalla_principal, font = TEXTO_FONT)
    cuadro_entrada.insert(0, " Ingrese película...")
    cuadro_entrada.grid(row = 1, column = 1)
    
    boton_busqueda = tkinter.Button(pantalla_principal, text = "BUSCAR", font = TITULO_BOTON_FONT, bg = MARCO_COLOR)
    boton_busqueda.grid(row = 1, column = 1, sticky="e")
    
    cant_posters: int = len(peliculas_ids_disponibles)
    boton_1 = tkinter.Button(pantalla_principal,
                             text=poster_1_id,
                             command = Pantalla_Secundaria
                             ).place(x = 68, y = 150)
    cant_posters -= 1
    
    if cant_posters != 0:
        boton_2 = tkinter.Button(pantalla_principal,
                                 text=poster_2_id,
                                 command = Pantalla_Secundaria
                                 ).place(x = 320, y = 150)
        cant_posters -= 1
        
    if cant_posters != 0:
        boton_3 = tkinter.Button(pantalla_principal,
                                 text=poster_3_id,
                                 command = Pantalla_Secundaria
                                 ).place(x = 68, y =440)
        cant_posters -= 1
        
    if cant_posters != 0:
        boton_3 = tkinter.Button(pantalla_principal,
                                 text=poster_4_id,
                                 command = Pantalla_Secundaria
                                 ).place(x = 320, y = 440)
        cant_posters -= 1
    
    pantalla_principal.mainloop()

def main():
    Pantalla_Principal()
main()