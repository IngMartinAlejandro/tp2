import qrcode
import cv2
import time
import os


def generar_codigo_qr(string_generador:str) -> None:
    img = qrcode.make(string_generador)
    img.save("qrcode.png")

def desactivar_escaneo_por_tiempo_limite(tiempo_limite:int, tiempo_inicio:int, camara_activada:bool) -> bool:
    tiempo_actual:int = cv2.getTickCount()
    tiempo_transcurrido:float = (tiempo_actual - tiempo_inicio) / cv2.getTickFrequency()#obtener la frecuencia del temporizador
    if tiempo_transcurrido > tiempo_limite:
        camara_activada = False
    return camara_activada

def escanear_codigo_qr() -> str:
    tiempo_limite:int = 15 # segundos
    tiempo_inicio:int = cv2.getTickCount()#Obtiene el tiempo actual en milisegundos
    camara = cv2.VideoCapture(0)#Inicializa camara(el "0" es para que eliga la camara predeterminada)
    camara_activada:bool = True
    dato_decodificado:str = ""
    while camara_activada:
        ret, fotograma = camara.read()
        if cv2.waitKey(1) == ord('s'):
            camara_activada = False
        detector_qr = cv2.QRCodeDetector()# Intenta detectar un código QR en el fotograma
        dato_decodificado, vertices_qr, imagen_rectificada = detector_qr.detectAndDecode(fotograma)
        if len(dato_decodificado) > 0:
            print(f"Dato decodificado: {dato_decodificado}")
            camara_activada = False
        else:
            cv2.imshow("Capturador de imagenes", fotograma)# Muestra el fotograma en una ventana
        camara_activada = desactivar_escaneo_por_tiempo_limite(tiempo_limite, tiempo_inicio, camara_activada)
    camara.release()
    cv2.destroyAllWindows()
    return dato_decodificado


def calcular_id_codigo_QR(string_generado_id_qr:str) -> str:
    id_codigo_qr = ""
    lista_datos = string_generado_id_qr.split(' + ')
    for dato in lista_datos:
        id_codigo_qr += dato[:2]
    return id_codigo_qr

def pedir_id_codigo_QR(id_codigo_qr_generado:str) -> bool:
    id_valido:bool = True
    intentos:int = 4
    id_codigo:str = input("Ingrese id del código QR: ")
    while (id_codigo != id_codigo_qr_generado) and (0 < intentos):
        id_codigo = input(f"Id del código QR invalido, te quedan {intentos} intentos: ")
        intentos -= 1
    if id_codigo != id_codigo_qr_generado:
        id_valido = False
        print("Se regresará al menú principal!")
        time.sleep(2)
        limpiar_terminal()
    else:
        print("\nId valido,se generará un archivo(Ingresos.txt) de los compras de los clientes ingresados al cine.")
    return id_valido

def validar_QR(string_generador_QR:str, dato_decodificado:str) -> bool:
    qr_valido:bool = False
    if dato_decodificado == string_generador_QR:
        print("\nCódigo QR valido, se generará un archivo(Ingresos.txt) de los compras de los clientes ingresados al cine.")
        qr_valido = True
    else:
        print("Por Código QR invalido o tiempo límite alcanzado, se regresará al menú principal")
        time.sleep(3)
        limpiar_terminal()
    return qr_valido

def valor_invalido(valor:str, valores_validos:list[str]) -> bool:
    return valor not in valores_validos

def limpiar_terminal() -> None:
    os.system('cls')

def cargar_archivo_txt():
    None#Falta completar

def mostrar_menu_alc() -> None:
    print("""
    -----Aplicacion de lectura de codigos----
    
    1) Ingresar id del código QR.
    2) Escanear código QR(vía Webcam).
    3) Salir.
    
    """)

def seleccionar_opcion() -> str:
    mostrar_menu_alc()
    opcion:str = input("Ingrese una opcion: ")
    while valor_invalido(opcion, ['1', '2']):
        opcion = input(f"La opcion {opcion} es invalida. Por favor, seleccione una opcion valida('1' o '2'): ")
    return opcion

def aplicacion_lectura_codigos() -> None:
    string_generador_QR:str = "ID_QR + pelicula + ubicación_totem + cantidad_entradas + timestamp_compra"#reemplazar
    string_generador_id_QR:str = "pelicula + ubicación_totem + cantidad_entradas + timestamp_compra"#reemplazar
    generar_codigo_qr(string_generador_QR)
    id_codigo_qr:str = calcular_id_codigo_QR(string_generador_id_QR)
    opcion:str = seleccionar_opcion()
    while opcion != "3":
        if opcion == "1":
            id_valido:bool = pedir_id_codigo_QR(id_codigo_qr)
            if id_valido == True:
                cargar_archivo_txt()
                opcion = "3"
            else:
                opcion:str = seleccionar_opcion()
        elif opcion == "2":
            dato_decodificado = escanear_codigo_qr()
            qr_valido:bool = validar_QR(string_generador_QR, dato_decodificado)
            if qr_valido == True:
                opcion = "3"
                cargar_archivo_txt()
            else:
                opcion:str = seleccionar_opcion()
    print("Gracias por usar nuestra aplicación!\n")

aplicacion_lectura_codigos()
