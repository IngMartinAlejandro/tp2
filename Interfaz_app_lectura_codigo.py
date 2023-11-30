import os
import qrcode
import cv2
import tkinter
from tkinter import messagebox
from PIL import Image, ImageDraw,ImageFont

def generar_codigo_qr(string_generador:str) -> None:
    imagen:qrcode.make = qrcode.make(string_generador)
    imagen.save("qrcode.png")

def generar_pdf_código_e_id_qr(id_codigo_qr:str) -> None:
    nombre_pdf:str = "completar"
    imagen_qr:Image = Image.open('qrcode.png').convert('RGB')
    modificador_imagen:ImageDraw = ImageDraw.Draw(imagen_qr)
    texto:str = f"ID codigoQR: {id_codigo_qr}"
    posiciones:tuple[int] = (150, 10)#coordenadas x,y
    color:tuple[int] = (0, 0, 0)#color negro
    tipo_letra:ImageFont = ImageFont.truetype('arial.ttf', 16)
    modificador_imagen.text(posiciones, texto, fill=color, font=tipo_letra)
    os.remove("qrcode.png")
    if not os.path.exists("archivos_pdf"):
        os.makedirs("archivos_pdf")
    imagen_qr.save(os.path.join("archivos_pdf", f"{nombre_pdf}.pdf"))

def calcular_id_codigo_QR(string_generado_id_qr:str) -> str:
    """
    PRE:String_generador tiene que estar definido.
    POST:Crea un cadena encriptada 'id_codigo_qr', usando el string_generador.
    """
    id_codigo_qr:str = ""
    lista_datos:list[str] = string_generado_id_qr.split(' + ')
    for dato in lista_datos:
        id_codigo_qr += dato[:2]
    return id_codigo_qr

def crear_agregar_datos_archivo_txt(encabezado:str = "timestamp, Id_QR, nombre_pelicula, cant_entradas, total_consumido") -> None:
    """
    PRE:Encabezado tiene que star definido.
    POST:Crea un arhvico.txt si no está creado,  y/o agrega "encabezado" a la última linea del archivo.
    """
    with open("Ingresos.txt", "a") as texto:
        texto.write(encabezado+"\n")

def validar_id_codigo_qr(id_ingresado:str, ventana_id_qr, id_qr:str) -> None:
    """
    PRE:Id_ingresado, ventana_id_qr e id_qr tienen que estar definidos.
    POST:Muestra un cuadro de mensaje, que dirá que el Id_qr es valiod o invalido, si es valido
        llamará a la función crear_agregar_datos_archivos_txt.
    """
    mensaje:str = "ID QR válido, se generará un archivo(Ingresos.txt) de los compras de los clientes ingresados al cine."
    if id_qr == id_ingresado:
        ventana_id_qr.destroy()
        messagebox.showinfo("Ventana de información", mensaje)
        crear_agregar_datos_archivo_txt()#Le pasaremos los datos recibidos como argumento.
    else:
        messagebox.showwarning("Ventanada de alartes", "ID del QR invalido!")
        abrir_ventana_id_QR(id_qr)

def abrir_ventana_id_QR(id_qr:str) -> None:
    """
    PRE:Id_qr tiene que estar definido.
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
    nuevo_comando = lambda:validar_id_codigo_qr(cuadro_texto.get(), ventana_id_qr, id_qr)
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
        crear_agregar_datos_archivo_txt()#Le pasaremos los datos recibidos como argumento.

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

def crear_botones_pantalla_principal(id_qr) -> None:
    """
    PRE:Id_qr tiene que estar definido.
    POST:Crea dos botones, que al hacer click, uno llamará a la función escanear_codigo_qr,
        y el otro llamará a la función abrir_ventana_id_Qr.
    """
    boton_scaner:tkinter.Button = tkinter.Button(text="ScanearQR", bg="#C5C5ED", command=escanear_codigo_qr)
    boton_scaner.grid(row=2,column=0)
    nuevo_comando = lambda:abrir_ventana_id_QR(id_qr)
    boton_digitar:tkinter.Button = tkinter.Button(text="DigitarQR", bg="#C5C5ED", command=nuevo_comando)
    boton_digitar.grid(row=2,column=2)

def crear_ventana_principal(id_qr:str) -> None:
    """
    PRE:Id_qr debe estar definido, los iconos e imagenes que se usen tienen que estar descargados y ubicados
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
    crear_botones_pantalla_principal(id_qr)
    ventana.mainloop()

def main() -> None:
    # String_generador será el que se reciba de la app cine al comprar entradas y/o snacks de la película elegida.
    string_generador_QR:str = "pelicula + ubicación_totem + cantidad_entradas + timestamp_compra + total_consumido"
    id_qr:str = calcular_id_codigo_QR(string_generador_QR)
    crear_ventana_principal(id_qr)
main()