from backend import consultar_peliculas, consultar_sinopsis,consultar_posters, consultar_snacks
from backend import consultar_proyecciones, consultar_info_cines, consultar_peliculas_x_cine
from backend import descargar_poster,crear_qr, buscar_pelicula, buscar, revisar_disponibilidad_asientos
from backend import completar_info_cine, completar_peliculas_x_cine,reservar_pelicula

TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

headers={"Authorization" : TOKEN}

url_base ="http://vps-3701198-x.dattaweb.com:4000"

info_peliculas= consultar_peliculas(url_base,headers)

print (info_peliculas)

sinopsis_peliculas= consultar_sinopsis(url_base,"/12",headers=headers)

print(sinopsis_peliculas)

poster_bytes = consultar_posters(url_base,"/12",headers=headers)

descargar_poster(poster_bytes)

snack = consultar_snacks(url_base,headers)

print(snack)

proyecciones= consultar_proyecciones(url_base,"/12",headers=headers)

print(proyecciones)

info_cines=consultar_info_cines(url_base,headers=headers)

print(info_cines)

peliculas_x_cine= consultar_peliculas_x_cine(url_base,"/1",headers=headers)

print(peliculas_x_cine)

cadena_prueba="ID_QR + pelicula + ubicación_totem + cantidad_entradas + timestamp_compra"

crear_qr(cadena_prueba)

id_movie =buscar_pelicula(info_peliculas,"COCO")

assert id_movie == "2"

id_movie =buscar(info_peliculas,"PEPE")
assert id_movie == "0"

assert revisar_disponibilidad_asientos(4,5) == True

peliculas_x_cine_completo = completar_peliculas_x_cine(info_cines,url_base,headers)

completar_info_cine(info_cines,peliculas_x_cine_completo)

print(info_cines)

reservar_pelicula(info_cines,10,"1","1")

print(info_cines)

