from tkinter import *
from tkinter import messagebox
import qrcode
import cv2
from PIL import Image, ImageDraw,ImageFont

def generar_codigo_qr(string_generador:str) -> None:
    imagen = qrcode.make(string_generador)
    imagen.save("qrcode.png")

def generar_pdf_código_e_id_qr(id_codigo_qr:str):
    imagen = Image.open('qrcode.png').convert('RGB')
    draw = ImageDraw.Draw(imagen)
    texto:str = f"ID codigoQR: {id_codigo_qr}"
    posiciones:tuple[int] = (150, 10)#coordenadas x,y
    color:tuple[int] = (0, 0, 0)#color negro
    tipo_letra = ImageFont.truetype('arial.ttf', 16)
    draw.text(posiciones, texto, fill=color, font=tipo_letra)
    imagen.save('qrcode.png')
    imagen.save("archivo.pdf")

def calcular_id_codigo_QR(string_generado_id_qr:str) -> str:
    id_codigo_qr:str = ""
    lista_datos:list[str] = string_generado_id_qr.split(' + ')
    for dato in lista_datos:
        id_codigo_qr += dato[:2]
    return id_codigo_qr

def crear_agregar_datos_archivo_txt(encabezado:str = "timestamp, Id_QR, nombre_pelicula, cant_entradas, total_consumido"):
    with open("Ingresos.txt", "a") as texto:
        texto.write(encabezado)

def validar_id_codigo_qr(id_ingresado:str, ventana_id_qr, id_qr:str):
    mensaje:str = "ID QR válido, se generará un archivo(Ingresos.txt) de los compras de los clientes ingresados al cine."
    if id_qr == id_ingresado:
        ventana_id_qr.destroy()
        messagebox.showinfo("Ventana de información", mensaje)
        crear_agregar_datos_archivo_txt()#Le pasaremos los datos recibidos como argumento.
    else:
        messagebox.showwarning("Ventanada de alartes", "ID del QR invalido!")
        abrir_ventana_id_QR(id_qr)

def abrir_ventana_id_QR(id_qr:str) -> None:
    ventana_id_qr = Toplevel()
    ventana_id_qr.config(bg="#242424")#gris oscuro
    ventana_id_qr.geometry("200x70")
    etiqueta = Label(ventana_id_qr, text = "Ingresa el ID del codigo QR", bg="#C5C5ED")#C5C5ED, es azul magenta claro
    etiqueta.pack()
    cuadro_texto = Entry(ventana_id_qr)
    cuadro_texto.pack()
    nuevo_comando = lambda:validar_id_codigo_qr(cuadro_texto.get(), ventana_id_qr, id_qr)
    boton_ingreso = Button(ventana_id_qr, text="Ingresar", bg="#C5C5ED", command=nuevo_comando)
    boton_ingreso.pack()

def desactivar_escaneo_por_tiempo_limite(datos:list) -> tuple[bool]:
    tiempo_limite, tiempo_inicio, camara_activada, detecto_qr = datos[0], datos[1], datos[2], datos[3]
    tiempo_actual:int = cv2.getTickCount()
    tiempo_transcurrido:float = (tiempo_actual - tiempo_inicio) / cv2.getTickFrequency()#obtener la frecuencia del temporizador
    if tiempo_transcurrido > tiempo_limite:
        camara_activada = False
        detecto_qr = False
    return camara_activada, detecto_qr

def mostrar_mensaje_escaneo_validado(detecto_qr, dato_decodificado:str) -> None:
    if detecto_qr == False:
        messagebox.showwarning("Ventanada de alartes", "Alcanzaste el limite de tiempo")
    else:
        mensaje = f"""
        Dato decodificado:\n
        {dato_decodificado}\n
        Se generará un archivo(Ingresos.txt) de los compras de los clientes ingresados al cine.
                    """
        messagebox.showinfo("Ventana de información", mensaje)
        crear_agregar_datos_archivo_txt()#Le pasaremos los datos recibidos como argumento.

def escanear_codigo_qr() -> None:
    tiempo_limite:int = 10 # segundos
    tiempo_inicio:int = cv2.getTickCount()#Obtiene el tiempo actual en milisegundos
    camara_activada:bool = True
    detecto_qr = True
    dato_decodificado:str = ""
    camara = cv2.VideoCapture(0)#Inicializa camara(el "0" es para que eliga la camara predeterminada)
    while camara_activada:
        ret, fotograma = camara.read()
        if cv2.waitKey(1) == ord('s'): camara_activada = False
        detector_qr = cv2.QRCodeDetector()# Intenta detectar un código QR en el fotograma
        dato_decodificado, vertices_qr, imagen_rectificada = detector_qr.detectAndDecode(fotograma)
        if len(dato_decodificado) > 0:
            camara_activada = False
        else:
            cv2.imshow("Capturador de imagenes", fotograma)# Muestra el fotograma en una ventana
        datos:list = [tiempo_limite, tiempo_inicio, camara_activada, detecto_qr]
        camara_activada, detecto_qr = desactivar_escaneo_por_tiempo_limite(datos)
    camara.release()
    cv2.destroyAllWindows()
    mostrar_mensaje_escaneo_validado(detecto_qr, dato_decodificado)

def crear_ventana_principal(id_qr:str):
    ventana = Tk()
    etiqueta_principal = Label(ventana, text = "Lector de codigo QR", bg="#C5C5ED")#C5C5ED color azul magenta claro
    etiqueta_principal.grid(row=0,column=1)
    imagen_camara = PhotoImage(file="camara.png")
    etiqueta_imagen = Label(ventana, image=imagen_camara,bg="#242424")
    etiqueta_imagen.grid(row=1,column=0)
    imagen_binaria = PhotoImage(file="binario.png")
    etiqueta_imagen = Label(ventana, image=imagen_binaria,bg="#242424")
    etiqueta_imagen.grid(row=1,column=2)
    ventana.iconbitmap("scan.ico")
    ventana.geometry("400x200")
    ventana.config(bg="#242424")#color gris oscuro
    boton_scaner = Button(ventana, text="ScanearQR", bg="#C5C5ED", command=escanear_codigo_qr)
    boton_scaner.grid(row=2,column=0)
    nuevo_comando = lambda:abrir_ventana_id_QR(id_qr)
    boton_digitar = Button(ventana, text="DigitarQR", bg="#C5C5ED", command=nuevo_comando)
    boton_digitar.grid(row=2,column=2)
    ventana.mainloop()

def app_lectura_codigo():
    # Luego se mejorarán algunos de los parametros de las funciones, cuando reciba los datos y juntemos las ramas.
    string_generador_QR:str = "pelicula + ubicación_totem + cantidad_entradas + timestamp_compra + total_consumido"
    id_qr:str = calcular_id_codigo_QR(string_generador_QR)
    generar_codigo_qr(string_generador_QR)
    generar_pdf_código_e_id_qr(id_qr)
    crear_ventana_principal(id_qr)
app_lectura_codigo()