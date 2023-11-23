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
COLOR_FONDO_QR = "white"
COLOR_QR="black"

TAMANIO_PANTALLA = '576x730'
COLOR_BG = 'Gray25'
COLOR_FG = 'Light gray'
TITULO_FONT = 'Rockwell 16'
BOTON_FONT = 'Rockwell 14'
LIST_FONT = 'Rockwell 11'
TEXTO_FONT = 'Rockwell 12'


def Encabezado(location: str, pantalla: tkinter) -> None:
    tkinter.Frame(pantalla,
                  width = 576,
                  height = 25,
                  bg = 'gold3'
                  ).place(x=0, y=80)
    tkinter.Frame(pantalla,
                  width = 576,
                  height = 80,
                  bg = 'deeppink4'
                  ).place(x=0, y=0)
    tkinter.Label(pantalla,
                  text = "CINEMA",
                  font = "Mincho 40",
                  bg = 'deeppink4',
                  fg = "white"
                  ).place(x = 12, y = 25, height = 40)
    tkinter.Label(pantalla,
                  text = f"{location}",
                  font = "Mincho 25",
                  bg = 'deeppink4',
                  fg = "white"
                  ).place(x = 220, y = 32, height = 40)


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
    pantalla_checkout.configure(bg = COLOR_BG)
    pantalla_checkout.resizable(0, True)
    
    pantalla_checkout.focus()
    pantalla_checkout.grab_set()
    
    Encabezado(location, pantalla_checkout)    
    pantalla_checkout.title(f"CINEMA{location} - Pantalla Checkout")
    
    tkinter.Label(pantalla_checkout,
                  text = "SE COMPRO:",
                  font = TITULO_FONT,
                  bg = COLOR_BG,
                  fg = COLOR_FG
                ).place(x = 20, y = 160)
    tkinter.Label(pantalla_checkout,
                  text = f"- {cant_tickets} : Tickets".upper(),
                  font = LIST_FONT,
                  bg = COLOR_BG,
                  fg = COLOR_FG
                ).place(x = 40, y = 190)
    i = 0
    for n in list_snack:
        tkinter.Label(pantalla_checkout,
                    text = f"- {list_snack[n]} : {n}".upper(),
                    font = LIST_FONT,
                    bg = COLOR_BG,
                    fg = COLOR_FG
                    ).place(x = 40, y = 215 + i*25)
        i += 1
        
    tkinter.Label(pantalla_checkout,
                text = "PRECIO TOTAL:",
                font = TITULO_FONT,
                bg = COLOR_BG,
                fg = COLOR_FG
                ).place(x = 20, y = 500)
    tkinter.Label(pantalla_checkout,
                text = f"{precio_total}$",
                font = TEXTO_FONT,
                bg = COLOR_BG,
                fg = COLOR_FG
                ).place(x = 40, y = 530)

    tkinter.Button(pantalla_checkout,
                   text = "PAGAR",
                   font = 'Rockwell 16',
                   bg = 'gold3'
                ).place(x = 410, y = 610)


def Snack(pantalla_reserva):
    #Esta es la informacion que debera recibir de la API
    #---------------------------------------------------    
    snacks = {"doritos": "2500.00", "popcorn_xxl": "4300.00"}
    #---------------------------------------------------
    tkinter.Label(pantalla_reserva,
                text = "ESTOS SON LOS SNACKS DISPONIBLES:",
                  font = TITULO_FONT,
                  bg = COLOR_BG,
                  fg = COLOR_FG
                ).place(x = 20, y = 290)
    i = 0
    for n in snacks:
        tkinter.Label(pantalla_reserva,
                    text = f"{n} : {snacks[n]}".upper(),
                    font = LIST_FONT,
                    bg = COLOR_BG,
                    fg = COLOR_FG
                    ).place(x = 40, y = 320 + i*25)
        i += 1

    tkinter.Label(pantalla_reserva,
                text = "INGRESE EL SNACK:",
                font = TEXTO_FONT,
                bg = COLOR_BG,
                fg = COLOR_FG
                ).place(x = 20, y = 500, height = 17)
    tkinter.Entry(pantalla_reserva
                ).place(x = 189, y = 500, width= 370)

    tkinter.Label(pantalla_reserva,
                text = "INGRESE LA CANTIDAD:",
                font = TEXTO_FONT,
                bg = COLOR_BG,
                fg = COLOR_FG
                ).place(x = 20, y = 530, height = 17)
    tkinter.Entry(pantalla_reserva
                ).place(x = 220, y = 530, width= 339)

    tkinter.Button(pantalla_reserva,
                   text = "Comprar Snack",
                   font = BOTON_FONT,
                   bg = 'gold3',
                   command = Checkout
                ).place(x = 375, y = 565)


def Pantalla_Reserva() -> None:
    #Esta es la informacion que debera recibir de la API
    #---------------------------------------------------    
    location = "Location"
    #---------------------------------------------------
    pantalla_reserva = tkinter.Toplevel()
    pantalla_reserva.geometry(TAMANIO_PANTALLA)
    pantalla_reserva.configure(bg = COLOR_BG)
    pantalla_reserva.resizable(0, True)
    
    pantalla_reserva.focus()
    pantalla_reserva.grab_set()
    
    Encabezado(location, pantalla_reserva)    
    pantalla_reserva.title(f"CINEMA{location} - Pantalla Reserva")
    
    tkinter.Button(pantalla_reserva,
                   text = "Volver a pantalla Anterior",
                   font = BOTON_FONT,
                   bg = COLOR_BG,
                   fg = COLOR_FG,
                   command = pantalla_reserva.destroy
                ).place(x = 335, y = 105)

    tkinter.Label(pantalla_reserva,
                  text = "INGRESE LA CANTIDAD DE ENTRADAS:",
                  font = TITULO_FONT,
                  bg = COLOR_BG,
                  fg = COLOR_FG
                ).place(x = 20, y = 160)
    tkinter.Entry(pantalla_reserva
                ).place(x = 40, y = 200, width= 490)
    
    Comando_Snack = lambda: Snack(pantalla_reserva)
    tkinter.Button(pantalla_reserva,
                   text = "Añadir Snack",
                   font = BOTON_FONT,
                   bg = 'gold3',
                   command = Comando_Snack
                ).place(x = 380, y = 230)
    
    tkinter.Button(pantalla_reserva,
                   text = "Añadir Carrito",
                   font = BOTON_FONT,
                   bg = 'gold3',
                   command = Checkout
                ).place(x = 380, y = 610)


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
    pantalla_secundaria.configure(bg = COLOR_BG)
    pantalla_secundaria.resizable(0, True)
    
    pantalla_secundaria.focus()
    pantalla_secundaria.grab_set()
    
    Encabezado(location, pantalla_secundaria)
    pantalla_secundaria.title(f"CINEMA{location} - Pantalla Pelicula")
    
    tkinter.Button(pantalla_secundaria,
                   text = "Volver a pantalla Anterior",
                   font = BOTON_FONT,
                   bg = COLOR_BG,
                   fg = COLOR_FG,
                   command = pantalla_secundaria.destroy
                ).place(x = 335, y = 105)
    
    tkinter.Label(pantalla_secundaria,
                  text = name,
                  font = TITULO_FONT,
                  bg = COLOR_BG,
                  fg = COLOR_FG
                ).place(x = 20, y = 160)
    tkinter.Label(pantalla_secundaria,
                  text = f"[] {duration}",
                  font = TEXTO_FONT,
                  fg = 'deeppink4',
                  bg = COLOR_BG
                ).place(x = 40, y = 190)
    tkinter.Label(pantalla_secundaria,
                  text = f"Actores: {directors}",
                  font = TEXTO_FONT,
                  bg = COLOR_BG,
                  fg = COLOR_FG
                ).place(x = 40, y = 220)
    tkinter.Label(pantalla_secundaria,
                  text = f"Directores: {actors}",
                  font = TEXTO_FONT,
                  bg = COLOR_BG,
                  fg = COLOR_FG
                ).place(x = 40, y = 250)
    tkinter.Label(pantalla_secundaria,
                  text = f"Género: {gender}",
                  font = TEXTO_FONT,
                  bg = COLOR_BG,
                  fg = COLOR_FG
                ).place(x = 40, y = 280)
    tkinter.Label(pantalla_secundaria,
                  text = f"Clasificación: {rating}",
                  font = TITULO_FONT,
                  fg = 'deeppink4',
                  bg = COLOR_BG
                ).place(x = 360, y = 280)
    
    tkinter.Label(pantalla_secundaria,
                  text = "SINOPSIS",
                  font = TITULO_FONT,
                  bg = COLOR_BG,
                  fg = COLOR_FG
                ).place(x = 20, y = 340)
    letra: int = 0
    for n in range(7):
        tkinter.Label(pantalla_secundaria,
                      text = synopsis[letra*n :65 + letra*n],
                      font = "Rockwell 11",
                      bg = COLOR_BG,
                      fg = COLOR_FG
                    ).place(x = 40, y = 370 + n*25)
        letra = 65
    
    tkinter.Button(pantalla_secundaria,
                   text = "Reservar",
                   font = BOTON_FONT,
                   bg = 'gold3',
                   command = Pantalla_Reserva
                ).place(x = 410, y = 610)


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
    pantalla_principal.configure(bg = COLOR_BG)
    pantalla_principal.resizable(0, True)

    Encabezado(location, pantalla_principal)
    pantalla_principal.title(f"CINEMA{location} - Pantalla Principal")
    
    tkinter.Label(pantalla_principal,
                  text = "BUSCAR:",
                  font = TEXTO_FONT,
                  bg = 'gold3'
                ).place(x = 345, y = 80)
    tkinter.Entry(pantalla_principal
                ).place(x = 420, y = 83, width= 150)
    
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