import tkinter


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


def Snack():
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


def Pantalla_Reserva() -> None:
    #Esta es la informacion que debera recibir de la API
    #---------------------------------------------------    
    location = "Location"
    #---------------------------------------------------
    global pantalla_reserva
    pantalla_reserva = tkinter.Toplevel()
    pantalla_reserva.geometry("576x720")
    pantalla_reserva.resizable(0, True)
    
    pantalla_reserva.focus()
    pantalla_reserva.grab_set()
    
    pantalla_reserva.title(f"CINEMA{location} - Pantalla Reserva")
    Encabezado(location, pantalla_reserva)
    
    tkinter.Label(pantalla_reserva,
                text = "INGRESE LA CANTIDAD DE ENTRADAS:",
                font = "Rockwell 12"
                ).place(x = 20, y = 130, height = 17)
    pantalla_reserva.ingresar_cant_entradas = tkinter.Entry(pantalla_reserva
                                                ).place(x = 330, y = 130, width= 230)

    pantalla_reserva.boton_comprar = tkinter.Button(pantalla_reserva,
                                                    text = "COMPRAR",
                                                    font = "Rockwell 20",
                                                    bg = 'gold3'
                                                    ).place(x = 210, y = 170)
    
    pantalla_reserva.boton_snack = tkinter.Button(pantalla_reserva,
                                                text = "AÑADIR SNACK",
                                                font = "Rockwell 20",
                                                bg = 'gold3',
                                                command=Snack
                                                ).place(x = 170, y = 250)


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
    global pantalla_secundaria
    pantalla_secundaria = tkinter.Toplevel()
    pantalla_secundaria.geometry("576x720")
    pantalla_secundaria.resizable(0, True)
    
    pantalla_secundaria.focus()
    pantalla_secundaria.grab_set()
    
    pantalla_secundaria.title(f"CINEMA{location} - Pantalla Pelicula")
    Encabezado(location, pantalla_secundaria)
    
    tkinter.Label(pantalla_secundaria,
                  text = name,
                  font = "Rockwell 15"
                ).place(x = 20, y = 130, height = 17)
    tkinter.Label(pantalla_secundaria,
                  text = f"[] {duration}",
                  font = "Rockwell 12",
                  fg = 'deeppink4'
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
                             command = Pantalla_Reserva
                             ).place(x = 410, y = 600)


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
    global pantalla_principal
    pantalla_principal = tkinter.Tk()
    pantalla_principal.geometry("576x720")
    pantalla_principal.resizable(0, True)

    pantalla_principal.title(f"CINEMA{location} - Pantalla Principal")
    Encabezado(location, pantalla_principal)
    
    cant_posters: int = len(peliculas_ids_disponibles)
    
    #poster_1= tkinter.PhotoImage(file = poster_1_id).subsample(3)
    boton_1 = tkinter.Button(pantalla_principal,
                             text=poster_1_id,
                             command = Pantalla_Secundaria
                             ).place(x = 68, y = 150)
    cant_posters -= 1
    
    if cant_posters != 0:
        #poster_2= tkinter.PhotoImage(file = poster_2_id).subsample(3)
        boton_2 = tkinter.Button(pantalla_principal,
                                 text=poster_2_id,
                                 command = Pantalla_Secundaria
                                 ).place(x = 320, y = 150)
        cant_posters -= 1
        
    if cant_posters != 0:
        #poster_3= tkinter.PhotoImage(file = poster_3_id).subsample(3)
        boton_3 = tkinter.Button(pantalla_principal,
                                 text=poster_3_id,
                                 command = Pantalla_Secundaria
                                 ).place(x = 68, y =440)
        cant_posters -= 1
        
    if cant_posters != 0:
        #poster_4= tkinter.PhotoImage(file = poster_4_id).subsample(3)
        boton_3 = tkinter.Button(pantalla_principal,
                                 text=poster_4_id,
                                 command = Pantalla_Secundaria
                                 ).place(x = 320, y = 440)
        cant_posters -= 1
    
    pantalla_principal.mainloop()


def main():
    Pantalla_Principal()
main()