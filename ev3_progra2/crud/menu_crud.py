import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from models import Menu

class MenuCRUD:
    @staticmethod
    def _try_commit(db: Session, max_retries=3, delay=0.5):
        retries = 0
        while retries < max_retries:
            try:
                db.commit()
                return True
            except OperationalError as e:
                if "database is locked" in str(e):
                    db.rollback()
                    print(f"Intento {retries+1}/{max_retries}: la base de datos está bloqueada, reintentando...")
                    time.sleep(delay)
                    retries += 1
                else:
                    print(f"Error de base de datos: {e}")
                    db.rollback()
                    return False
            except SQLAlchemyError as e:
                print(f"Error al hacer commit: {e}")
                db.rollback()
                return False
        print("No se pudo hacer commit después de varios intentos.")
        return False

    @staticmethod
    def crear_menu(db: Session, nombre: str, precio: float, descripcion: str = None):
        menu = Menu(nombre=nombre, precio=precio, descripcion=descripcion)
        db.add(menu)

        if not MenuCRUD._try_commit(db):
            return None

        db.refresh(menu)
        return menu

    @staticmethod
    def leer_menus(db: Session):
        return db.query(Menu).all()

    @staticmethod
    def actualizar_menu(db: Session, menu_id: int, nuevo_nombre: str = None, nuevo_precio: float = None, nueva_descripcion: str = None):
        menu = db.query(Menu).get(menu_id)
        if not menu:
            print(f"No se encontró el menú con ID {menu_id}.")
            return None

        if nuevo_nombre:
            menu.nombre = nuevo_nombre
        if nuevo_precio is not None:
            menu.precio = nuevo_precio
        if nueva_descripcion is not None:
            menu.descripcion = nueva_descripcion

        if not MenuCRUD._try_commit(db):
            return None

        db.refresh(menu)
        return menu

    @staticmethod
    def borrar_menu(db: Session, menu_id: int):
        menu = db.query(Menu).get(menu_id)
        if not menu:
            print(f"No se encontró el menú con ID {menu_id}.")
            return None

        db.delete(menu)

        if not MenuCRUD._try_commit(db):
            return None

        return menu
