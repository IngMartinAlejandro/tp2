from backend import consultar_peliculas, consultar_sinopsis,consultar_posters, consultar_snacks
from backend import consultar_proyecciones, consultar_info_cines, consultar_peliculas_x_cine
from backend import descargar_poster

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