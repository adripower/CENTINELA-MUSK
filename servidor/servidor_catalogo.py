"""
Servidor local del catálogo de Centinela.

Simula la API de una tienda. No necesita internet ni dependencias externas:
funciona solo con la biblioteca estándar de Python.

    python servidor/servidor_catalogo.py

Deja el servidor escuchando en http://localhost:8000

Rutas disponibles
-----------------
GET /articulos                      lista completa
GET /articulos?categoria=moviles    filtra por categoría
GET /articulos?pagina=2&tam=20      paginación
GET /articulos/ART-0007             un artículo
GET /articulos/ART-0007/historico   su histórico de precios
GET /salud                          comprobación de que está vivo

El precio devuelto por /articulos varía ligeramente en cada llamada, para que
dos ejecuciones seguidas no den lo mismo. Una de cada doce peticiones responde
con un error 503 a propósito: la gestión de errores de la sesión 6 necesita que
la API falle de verdad de vez en cuando.
"""

import csv
import json
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

BASE = Path(__file__).parent / "datos"
PUERTO = 8000

with open(BASE / "catalogo.json", encoding="utf-8") as f:
    CATALOGO = json.load(f)["articulos"]

HISTORICO = {}
with open(BASE / "historico_precios.csv", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        HISTORICO.setdefault(fila["id"], []).append({
            "fecha": fila["fecha"],
            "precio": float(fila["precio"]),
            "stock": int(fila["stock"]),
        })


class Handler(BaseHTTPRequestHandler):

    def responder(self, codigo, cuerpo):
        datos = json.dumps(cuerpo, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def log_message(self, formato, *args):
        print(f"  {self.address_string()} - {formato % args}")

    def do_GET(self):
        ruta = urlparse(self.path)
        partes = [p for p in ruta.path.split("/") if p]
        params = parse_qs(ruta.query)

        if partes == ["salud"]:
            return self.responder(200, {"estado": "ok", "articulos": len(CATALOGO)})

        # fallo intencionado: 1 de cada 12 peticiones
        if random.random() < 1 / 12:
            return self.responder(503, {"error": "servicio no disponible, reintenta"})

        if partes == ["articulos"]:
            items = CATALOGO
            categoria = params.get("categoria", [None])[0]
            if categoria:
                items = [a for a in items if a["categoria"] == categoria]
            tam = int(params.get("tam", [25])[0])
            pagina = int(params.get("pagina", [1])[0])
            inicio = (pagina - 1) * tam
            trozo = [dict(a) for a in items[inicio:inicio + tam]]
            for a in trozo:
                a["precio"] = round(a["precio"] * random.uniform(0.985, 1.015), 2)
            return self.responder(200, {
                "pagina": pagina, "tam": tam, "total": len(items), "articulos": trozo,
            })

        if len(partes) == 2 and partes[0] == "articulos":
            art = next((a for a in CATALOGO if a["id"] == partes[1]), None)
            if art is None:
                return self.responder(404, {"error": f"no existe {partes[1]}"})
            copia = dict(art)
            copia["precio"] = round(art["precio"] * random.uniform(0.985, 1.015), 2)
            return self.responder(200, copia)

        if len(partes) == 3 and partes[0] == "articulos" and partes[2] == "historico":
            hist = HISTORICO.get(partes[1])
            if hist is None:
                return self.responder(404, {"error": f"no existe {partes[1]}"})
            return self.responder(200, {"id": partes[1], "historico": hist})

        self.responder(404, {"error": "ruta desconocida", "ruta": ruta.path})


if __name__ == "__main__":
    print(f"Catálogo de Centinela escuchando en http://localhost:{PUERTO}")
    print(f"Artículos cargados: {len(CATALOGO)}")
    print("Ctrl+C para parar.\n")
    try:
        HTTPServer(("localhost", PUERTO), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
