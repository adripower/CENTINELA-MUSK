# Centinela — paquete de arranque

Proyecto transversal del curso de Python en directo. Doce sesiones de 90 minutos
construyendo una sola herramienta.

El enunciado que ve el alumno está en `ENUNCIADO.md`. Este fichero es para quien
imparte.

## Contenido

```
ENUNCIADO.md                       el encargo, tal y como se entrega al alumno
servidor/servidor_catalogo.py      API local del proveedor (solo stdlib)
servidor/datos/catalogo.json       60 artículos en seis categorías
servidor/datos/historico_precios.csv   7.200 filas, 120 días
centinela/__init__.py              paquete vacío, con el mapa de lo que irá dentro
tests/test_arranque.py             test mínimo para validar el entorno
requirements.txt                   dependencias, comentadas por sesión
generar_datos.py                   regenera el catálogo y el histórico (semilla 42)
.gitignore
```

## Puesta en marcha

```bash
python -m venv .venv && source .venv/bin/activate   # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python servidor/servidor_catalogo.py
```

En otra terminal:

```bash
curl http://localhost:8000/salud
pytest
```

## Por qué una API local y no una web real

El scraping de tiendas reales se rompe en clase: cambian el HTML, bloquean la IP
del aula o directamente no hay internet. Este servidor usa solo la biblioteca
estándar, arranca en un segundo y se comporta igual en todos los equipos.

Además permite inyectar a propósito los dos problemas que el curso necesita:

- **El precio varía en cada llamada** (±1,5 %). Obliga al alumno a guardar estado
  en lugar de comparar dos respuestas consecutivas.
- **Una de cada doce peticiones devuelve un 503.** Es lo que hace que la sesión 6,
  sobre gestión de errores y reintentos, tenga un problema real que resolver.

Si en alguna sesión interesa desactivar los fallos, basta con comentar el bloque
marcado en `servidor_catalogo.py`. Para endurecer el ejercicio, subir la frecuencia.

## Regenerar los datos

`generar_datos.py` crea el catálogo y el histórico con semilla fija 42. Cambiando la semilla se obtiene un
dataset equivalente pero con otras soluciones, útil para una segunda edición.

## Dónde debería estar el proyecto en cada sesión

| Tras la sesión | El alumno tiene |
|---|---|
| 2 | Un script que pide un artículo por teclado y decide si es caro o barato |
| 3 | El catálogo cargado en memoria, filtrado y ordenado con estructuras de datos |
| 4 | La lógica repartida en funciones con responsabilidad única |
| 5 | La lista de vigilancia guardada en JSON y el histórico leído de CSV |
| 6 | Un programa que no se rompe con la API caída y deja traza en un log |
| 7 | `Articulo` y `Aviso` como clases, con las reglas dentro del dominio |
| 8 | El código repartido en módulos dentro del paquete |
| 9 | El cliente HTTP real contra el servidor, con reintentos |
| 10 | El estado en SQLite en lugar de en JSON |
| 11 | Tests de las cuatro reglas de aviso y un refactor hecho con red |
| 12 | CLI, empaquetado, README y la defensa preparada |

## Nota honesta

Las cuatro reglas de aviso están escogidas para que cada una exija una técnica
distinta (umbral simple, media móvil, comparación de estado anterior, variación
porcentual). No son las reglas que usaría un sistema real de vigilancia de precios,
pero cubren el temario sin forzar.
