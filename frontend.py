import tkinter


def Encabezado(locacion: str, pantalla: tkinter) -> None:
    tkinter.Frame(pantalla, width = 576, height = 25, bg = 'gold3').place(x=0, y=80)
    tkinter.Frame(pantalla, width = 576, height = 80, bg = 'deeppink4').place(x=0, y=0)
    tkinter.Label(pantalla, text = "CINEMA", font = "Mincho 40", bg = 'deeppink4', fg = "white").place(x = 12, y = 25, height = 40)
    tkinter.Label(pantalla, text = f"{locacion}", font = "Mincho 25", bg = 'deeppink4', fg = "white").place(x = 220, y = 32, height = 40)


def Pantalla_Secundaria() -> None:
    print("Hello World")
    return


def Pantalla_pantalla_Principal() -> None:
    #Esta es la informacion que debera recibir de la API
    #---------------------------------------------------
    locacion = "Location"
    peliculas_ids_disponibles = ["1", "2", "3", "4"]
    poster_1_id = "poster_1_id"
    poster_2_id = "poster_2_id"
    poster_3_id = "poster_3_id"
    poster_4_id = "images/image.png"
    #---------------------------------------------------
    
    pantalla_principal = tkinter.Tk()
    pantalla_principal.geometry("576x720")
    pantalla_principal.resizable(0, 0) 

    Encabezado(locacion, pantalla_principal)
    
    cant_posters: int = len(peliculas_ids_disponibles)
    #poster_1= tkinter.PhotoImage(file = poster_1_id).subsample(3)
    boton_1 = tkinter.Button(pantalla_principal, text=poster_1_id, command = Pantalla_Secundaria)
    boton_1.place(x = 68, y = 150)
    cant_posters -= 1
    if cant_posters != 0:
        #poster_2= tkinter.PhotoImage(file = poster_2_id).subsample(3)
        boton_2 = tkinter.Button(pantalla_principal, text=poster_2_id, command = Pantalla_Secundaria)
        boton_2.place(x = 320, y = 150)
        cant_posters -= 1
        
    if cant_posters != 0:
        #poster_3= tkinter.PhotoImage(file = poster_3_id).subsample(3)
        boton_3 = tkinter.Button(pantalla_principal, text=poster_3_id, command = Pantalla_Secundaria)
        boton_3.place(x = 68, y =440)
        cant_posters -= 1
        
    if cant_posters != 0:
        #poster_4= tkinter.PhotoImage(file = poster_4_id).subsample(3)
        boton_3 = tkinter.Button(pantalla_principal, text=poster_4_id, command = Pantalla_Secundaria)
        boton_3.place(x = 320, y = 440)
        cant_posters -= 1
    
    pantalla_principal.mainloop()




def main():
    Pantalla_pantalla_Principal()
main()