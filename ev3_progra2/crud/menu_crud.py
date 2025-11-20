import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from models import Menu

class MenuCRUD:
    @staticmethod
    def crear_menu(db: Session, nombre: str, precio: float, ingredientes: list):
        menu_existente = db.query(Menu).filter_by(nombre=nombre).first()
        if menu_existente:
            print(f"El menu con el nombre '{nombre}' ya existe.")
            return menu_existente

        menu = Menu(nombre=nombre, precio=precio, ingredientes=ingredientes)
        db.add(menu)
        try:
            db.commit()
            db.refresh(menu)
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error al crear el menu: {e}")
            return None
        return menu

    @staticmethod
    def leer_menus(db: Session):
        """Obtiene todos los menus en la base de datos."""
        return db.query(Menu).all()

    @staticmethod  
    def actualizar_menu(db: Session, nombre_actual: str, nuevo_nombre: str, precio: float = None, ingredientes: list = None):
        menu = db.query(Menu).get(nombre_actual)
        if not menu:
            print(f"No se encontró el menu con el nombre '{nombre_actual}'.")
            return None

        if nuevo_nombre and nuevo_nombre != nombre_actual:
            nuevo_menu = Menu(nombre=nuevo_nombre, precio=precio, ingredientes=ingredientes)
            db.add(nuevo_menu)
            try:
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                print(f"Error al actualizar el menu con nuevo nombre: {e}")
                return None

            db.delete(menu)
            try:
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                print(f"Error al eliminar el menu antiguo: {e}")
                return None

            return nuevo_menu      