from backend import consultar_peliculas, consultar_sinopsis,consultar_posters, consultar_snacks
from backend import consultar_proyecciones, consultar_info_cines, consultar_peliculas_x_cine
from backend import descargar_poster,crear_qr, buscar_pelicula, buscar, revisar_disponibilidad_asientos
from backend import completar_info_cine, completar_peliculas_x_cine,reservar_pelicula

TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

headers={"Authorization" : TOKEN}

url_base ="http://vps-3701198-x.dattaweb.com:4000"

### prueba consultar peliculas ###
info_peliculas= consultar_peliculas(url_base,headers)
print()
print (info_peliculas)

### prueba consultar sinopsis ###
sinopsis_peliculas= consultar_sinopsis(url_base,"/12",headers=headers)
print()
print(sinopsis_peliculas)

### prueba consultar posters  / descargar poster ###
poster_bytes = consultar_posters(url_base,"/12",headers=headers)
descargar_poster(poster_bytes)

### prueba consultar snack ###
snack = consultar_snacks(url_base,headers)
print()
print(snack)

### prueba consultar proyecciones ###
proyecciones= consultar_proyecciones(url_base,"/12",headers=headers)
print()
print(proyecciones)

### prueba consultar info cines ###
info_cines=consultar_info_cines(url_base,headers=headers)
print()
print(info_cines)

### prueba consultar peliculas x cine ###
peliculas_x_cine= consultar_peliculas_x_cine(url_base,"/1",headers=headers)
print()
print(peliculas_x_cine)

### prueba crear qr ###
cadena_prueba="pelicula + ubicación_totem + cantidad_entradas + timestamp_compra"
crear_qr(cadena_prueba)

### prueba buscar pelicula / buscar ###
id_movie =buscar_pelicula(info_peliculas,"COCO")
assert id_movie == "2"

id_movie =buscar(info_peliculas,"PEPE")
assert id_movie == "0"

### prueba revisar_disponibilidad_asientos ###
assert revisar_disponibilidad_asientos(4,5) == True

### pruebas funciones estructura de datos ###
peliculas_x_cine_completo = completar_peliculas_x_cine(url_base,headers)

print()
print(peliculas_x_cine_completo)

info_cines = completar_info_cine(peliculas_x_cine_completo,url_base,headers)

print()
print(info_cines)

### pruebas reservar pelicula ###
reservar_pelicula(info_cines,10,"1","1")
print(info_cines)

