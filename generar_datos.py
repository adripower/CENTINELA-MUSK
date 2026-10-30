"""Genera los datos de partida del proyecto Centinela: catálogo e histórico."""

import csv
import json
import random
from datetime import date, timedelta

random.seed(42)
RAIZ = "servidor/datos"

CATEGORIAS = {
    "portatiles": (520, 2100),
    "moviles": (160, 1350),
    "monitores": (120, 900),
    "audio": (25, 480),
    "perifericos": (12, 220),
    "almacenamiento": (18, 340),
}
MARCAS = ["Nexora", "Kuvio", "Trilan", "Beltek", "Orvia", "Zandor"]
SINGULAR = {
    "portatiles": "Portatil", "moviles": "Movil", "monitores": "Monitor",
    "audio": "Altavoz", "perifericos": "Teclado", "almacenamiento": "SSD",
}
TIENDAS = ["tecnomas", "clickstore", "latienda"]

catalogo = []
pid = 1
for cat, (low, high) in CATEGORIAS.items():
    for _ in range(10):
        base = round(random.uniform(low, high), 2)
        catalogo.append({
            "id": f"ART-{pid:04d}",
            "nombre": f"{random.choice(MARCAS)} {SINGULAR[cat]} {random.randint(100, 999)}",
            "categoria": cat,
            "tienda": random.choice(TIENDAS),
            "precio": base,
            "precio_referencia": round(base * random.uniform(1.0, 1.35), 2),
            "stock": random.choice([0, 0, 1, 3, 5, 12, 40]),
            "valoracion": round(random.uniform(2.5, 5.0), 1),
            "url": f"https://ejemplo.test/p/ART-{pid:04d}",
        })
        pid += 1

with open(f"{RAIZ}/catalogo.json", "w", encoding="utf-8") as f:
    json.dump({"articulos": catalogo}, f, ensure_ascii=False, indent=2)

# histórico de 120 días con tendencia, ruido y alguna bajada fuerte
hoy = date.today()
filas = []
for art in catalogo:
    precio = art["precio_referencia"]
    bajada = random.randint(20, 110) if random.random() < 0.45 else None
    for d in range(120, 0, -1):
        dia = hoy - timedelta(days=d)
        precio *= random.uniform(0.997, 1.003)
        if bajada and 120 - d == bajada:
            precio *= random.uniform(0.70, 0.88)
        filas.append({
            "fecha": dia.isoformat(),
            "id": art["id"],
            "precio": round(precio, 2),
            "stock": max(0, art["stock"] + random.randint(-3, 3)),
        })

with open(f"{RAIZ}/historico_precios.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["fecha", "id", "precio", "stock"])
    w.writeheader()
    w.writerows(filas)

print("articulos:", len(catalogo), "| filas de historico:", len(filas))
