from ElementoMenu import CrearMenu
from Ingrediente import Ingrediente

class Pedido:
    def __init__(self):
        self.menus = []  

    def agregar_menu(self, menu: CrearMenu,cantidad: int = 1):
        # Verificar si el menu ya esta en el pedido
        for item in self.menus:
            if item.nombre == menu.nombre:
                item.cantidad += cantidad
                return
        # Si no esta, se agrega con la cantidad inicial 
        menu.cantidad = cantidad
        self.menus.append(menu)

    def eliminar_menu(self, nombre_menu: str):
        for menu in self.menus:
            if menu.nombre == nombre_menu:
                self.menus.remove(menu)
                return True
        return False

    def mostrar_pedido(self):
        return [(m.nombre, m.cantidad, m.precio, m.precio * m.cantidad) for m in self.menus]

    def calcular_total(self) -> float:
        return sum(m.precio * m.cantidad for m in self.menus)

