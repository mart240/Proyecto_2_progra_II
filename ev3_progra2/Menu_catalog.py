# menu_catalog.py
from typing import List
from ElementoMenu import CrearMenu
from Ingrediente import Ingrediente
from IMenu import IMenu

def get_default_menus() -> List[IMenu]:
    return [
        CrearMenu(
            "Papas fritas",
            [
                Ingrediente("Papas","unidad", 5)
            ],
            precio=500,
            icono_path="IMG/icono_papas_fritas_64x64.png",
        ),
        CrearMenu(
            "Pepsi",
            [
                Ingrediente("Pepsi","unidad", 1),
            ],
            precio=1100,
            icono_path="IMG/icono_cola_64x64.png",
        ),
        CrearMenu(
            "Completo",
            [
                Ingrediente("Vienesa","unidad", 1),
                Ingrediente("Pan de completo","unidad", 1),
                Ingrediente("Palta","unidad",1),
                Ingrediente("Tomate","unidad",1),
            ],
            precio=1800,
            icono_path="IMG/icono_hotdog_sin_texto_64x64.png",
        ),
        CrearMenu(
            "Hamburguesa",
            [
                Ingrediente("Pan de hamburguesa","unidad", 1),
                Ingrediente("Lamina de queso","unidad", 1),
                Ingrediente("Churrasco de carne","unidad", 1),
            ],
            precio=3500,
            icono_path="IMG/icono_hamburguesa_negra_64x64.png",
        ),
        CrearMenu(
            "Panqueques",
            [
                Ingrediente("Panqueques","unidad", 2),
                Ingrediente("Manjar","unidad", 1),
                Ingrediente("Azucar Flor","unidad", 1),
            ],
            precio=2000,
            icono_path="IMG/icono_panqueques_64x64.png",
        ),
        CrearMenu(
            "Pollo frito",
            [
                Ingrediente("Presa De Pollo","unidad", 1),
                Ingrediente("Harina","unidad", 1),
                Ingrediente("Aceite","unidad", 1),
            ],
            precio=2800,
            icono_path="IMG/icono_pollo_frito_64x64.png",
        ),
        CrearMenu(
            "Ensalada mixta",
            [
                Ingrediente("Lechuga", "unidad", 1),
                Ingrediente("Tomate", "unidad", 1),
                Ingrediente("Zanahoria Rallada", "unidad", 1),
            ],
            precio=1500,
            icono_path="IMG/ensalada_mixta_64x64.png",
        ),
         CrearMenu(
            "Coca cola",
            [
                Ingrediente("Coca cola", "unidad", 1),
            ],
            precio=1000,
            icono_path="IMG/icono_cola_lata_64x64.png",
        ),
        CrearMenu(
            "Chorrillana",
            [
                Ingrediente("Carne", "unidad", 1),
                Ingrediente("Cebolla", "unidad", 1),
                Ingrediente("Papas", "unidad", 6),
                Ingrediente("Huevos", "unidad", 2),
            ],
            precio=10000,
            icono_path="IMG/icono_chorrillana_64x64.png",
        ), 
        CrearMenu(
            "Empanada queso",
            [
                Ingrediente("Masa de empanada", "unidad", 1),
                Ingrediente("Queso", "unidad", 1),
            ],
            precio=2200,
            icono_path="IMG/icono_empanada_queso_64x64.png",
        )

    ]
