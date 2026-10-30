# Centinela — el encargo

## La situación

Una pequeña distribuidora de electrónica compra en tres tiendas online y revende.
Hoy, una persona del equipo dedica la primera hora de cada mañana a abrir las webs
de los proveedores, mirar precios y anotar en una hoja de cálculo lo que ha bajado.
Cuando se le olvida, pierden la oportunidad: las bajadas duran poco.

Te piden que lo automatices.

## Qué tienes que construir

Una herramienta de línea de comandos, escrita en Python, que consulte el catálogo
del proveedor, guarde el estado, detecte cambios relevantes y avise de ellos.

Al terminar el curso, `centinela` debe permitir:

```
centinela seguir ART-0042 --objetivo 450
centinela revisar
centinela avisos
centinela informe --categoria moviles
```

- **seguir** añade un artículo a la lista de vigilancia, con un precio objetivo opcional.
- **revisar** consulta la API, compara con lo guardado y genera avisos.
- **avisos** muestra lo que ha cambiado desde la última revisión.
- **informe** resume la situación de una categoría.

## Las reglas de aviso

Se genera un aviso cuando se cumple cualquiera de estas condiciones:

1. El precio baja de un umbral que el usuario ha fijado para ese artículo.
2. El precio cae más de un 10 % respecto a la media de los últimos treinta días.
3. Un artículo que estaba agotado vuelve a tener stock.
4. El precio sube más de un 20 % de golpe, que casi siempre significa un error de
   la tienda o un cambio de referencia, y conviene mirarlo.

## Qué tienes a mano

```
servidor/servidor_catalogo.py     la API del proveedor, en local
servidor/datos/catalogo.json      60 artículos
servidor/datos/historico_precios.csv   120 días de precios
centinela/                        el paquete, vacío: es lo que vas a escribir
tests/                            un test de arranque para comprobar el entorno
requirements.txt                  las dependencias, que se instalan por el camino
```

Arranca el servidor en una terminal aparte y déjalo corriendo:

```
python servidor/servidor_catalogo.py
```

Comprueba que responde:

```
curl http://localhost:8000/salud
```

## Dos advertencias sobre la API

El precio que devuelve varía ligeramente en cada llamada. Es intencionado: tu
código no puede dar por hecho que dos consultas seguidas devuelven lo mismo.

Y una de cada doce peticiones falla con un error 503. También es intencionado. A
partir de la sesión 6 tu programa tiene que sobrevivir a eso sin romperse.

## Cómo se evalúa

| Criterio | Peso |
|---|---|
| Funciona: las cuatro órdenes hacen lo que deben | 30 % |
| El código está organizado en módulos con responsabilidades claras | 20 % |
| Gestiona los errores y no se rompe con la API caída | 15 % |
| Tiene tests que cubren las reglas de aviso | 15 % |
| Está documentado y cualquiera puede instalarlo y ejecutarlo | 10 % |
| La defensa final explica las decisiones tomadas | 10 % |

## Una sugerencia

No intentes adelantarte. El proyecto está pensado para construirse en el orden de
las sesiones, y cada una introduce justo lo necesario para el paso siguiente. Si en
la sesión 3 resuelves algo con una clase, la sesión 7 pierde su sentido.
