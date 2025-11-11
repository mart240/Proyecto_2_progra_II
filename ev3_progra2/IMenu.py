# IMenu.py
from typing import Protocol, List, Optional
from Ingrediente import Ingrediente
from Stock import Stock

class IMenu(Protocol):
    def __init__(self,chorrillana,pepsi,coca_cola,empanada,completo,papas_fritas,hamburguesa):
        self.chorrillana = chorrillana
        self.pepsi = pepsi
        self.coca_cola = coca_cola
        self.empanada = empanada
        self.completo = completo
        self.papas_fritas = papas_fritas
        self.hamburguesa = hamburguesa

    def Combo_Tradicional(self,hamburguesa,papas_fritas,coca_cola,pepsi):
        pass
