"""Primer test del proyecto. Sirve para comprobar que pytest funciona.

    pytest

A partir de la sesión 11 este fichero se sustituye por tests de verdad.
"""


def test_el_entorno_funciona():
    assert 2 + 2 == 4


def test_se_puede_importar_el_paquete():
    import centinela
    assert centinela.__version__
