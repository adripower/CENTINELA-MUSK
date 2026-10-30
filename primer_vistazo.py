import json

UMBRAL_BARATO = 15  # % de descuento: barato

UMBRAL_CARO = 5     # % de descuento: caro

with open("servidor/datos/catalogo.json", encoding="utf-8") as f:
    datos = json.load(f)

articulo = datos['articulos']

print("Artículos en el catálogo:", len(articulo))
print('primer articulo:', articulo[0]['nombre'])
print('ultimo articulo: ',articulo[-1]['nombre'])

# sacar datos, calcular el descuento y mostrarlo
def info_producto(posicion):

    nombre = articulo[posicion]['nombre']
    precio = articulo[posicion]['precio']
    referencia = articulo[posicion]['precio_referencia']
    stock =articulo[posicion]['stock']

    descuento = (1 - (precio / referencia)) * 100
    print(nombre)
    print('- ' * 20)
    print(f'Precio actual: {precio:.2f} €')
    print(f'Precio de referencia: {referencia:.2f} €')
    print(f'Descuento:{descuento:.2f} %')
    # print(f'stock disponible: {stock}')
    return descuento, nombre, precio, referencia, stock

# verifica que esta bien el codigo a buscar
def verificar_codigo(entrada):
    entrada = entrada.strip().upper()

    if entrada.startswith("ART-"):
        entrada = entrada.removeprefix('ART-')

    if not entrada.isdigit():
        print(' tiene que ser numeros')
        return None
    codigo_limpio = entrada.zfill(4)

    return codigo_limpio


# localizar por su posicion en la lista
def localizar(posicion):
    if 0 <= posicion < len(articulo):
        print('- ' * 20)
        print(f"Posición: {posicion +1} : {articulo[posicion]['nombre']}")
        return True
    print(f" No existe ningún artículo en la posición {posicion}")
    return False



# informa del tipo de descuento
def mejor_descuento(descuento):
    if descuento >= UMBRAL_BARATO and descuento >= 25:
        veredicto = '****CHOLLO****'        # RETO que diga CHOLLO
    elif descuento >= UMBRAL_BARATO:
        veredicto = "BARATO: está muy por debajo de su precio de referencia."
    
    elif descuento < UMBRAL_CARO:
        veredicto = "CARO: apenas tiene descuento."
    else:
        veredicto = "PRECIO NORMAL: ni chollo ni abuso."
    print(veredicto)        

# verificar stock
def verificar_stock(stock):
    #stock = articulo[posicion]['stock']
    if stock == 0:
        print('Stock: Agotado')
    elif stock == 1:                  # RETO añadir 1 unidad solo en el stock
        print('Stock: 1 unidad') 
    else:
        print(f'Quedan: {stock} disponibles')

# precio objetivo
def verificar_objetivo(precio, stock):
    objetivo_texto = input('¿Tienes un precio objetivo? (Enter para saltar): ').strip()
    if not objetivo_texto:
        return
    try:
        objetivo = float(objetivo_texto.replace(',', '.'))
    except ValueError:
        print('Error eso no es un numero: ')   
        return
    if precio <= objetivo and stock > 0:                     
        if precio <= objetivo and stock > 0:
            print(f"¡Cómpralo! Está {objetivo - precio:.2f} € por debajo de tu objetivo y hay stock."
      )
    elif precio <= objetivo:
      print("Está por debajo de tu objetivo, pero ahora mismo no hay stock.")
    else:
      print(
          f"Todavía le faltan {precio - objetivo:.2f} € para llegar a tu"
          " objetivo."
      )

if __name__ =='__main__':
    pedir_codigo = input('Pon el código del artículo a buscar (ej. ART-1): ')
    codigo = verificar_codigo(pedir_codigo)

    if codigo is not None:
        posicion = int(codigo) - 1
        if localizar(posicion):
            descuento, nombre, precio, referencia, stock= info_producto(posicion)
            mejor_descuento(descuento)
            verificar_stock(stock)
            verificar_objetivo(precio, stock)
