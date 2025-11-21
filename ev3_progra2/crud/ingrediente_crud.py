import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from models import Ingrediente

class IngredienteCRUD:
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
                    print(f"Intento {retries+1}/{max_retries}: la BD está bloqueada, reintentando...")
                    time.sleep(delay)
                    retries += 1
                else:
                    print(f"Error de BD: {e}")
                    db.rollback()
                    return False
            except SQLAlchemyError as e:
                print(f"Error al hacer commit: {e}")
                db.rollback()
                return False

        print("No fue posible guardar los cambios en la BD.")
        return False

    @staticmethod
    def crear_ingrediente(db: Session, nombre: str, stock: float, unidad: str):
        ingrediente = Ingrediente(nombre=nombre, stock=stock, unidad=unidad)
        db.add(ingrediente)

        if not IngredienteCRUD._try_commit(db):
            return None

        db.refresh(ingrediente)
        return ingrediente

    @staticmethod
    def leer_ingredientes(db: Session):
        return db.query(Ingrediente).all()

    @staticmethod
    def actualizar_ingrediente(db: Session, ingrediente_id: int, nombre: str = None, stock: float = None, unidad: str = None):
        ingrediente = db.query(Ingrediente).get(ingrediente_id)
        if not ingrediente:
            print(f"No se encontró el ingrediente ID {ingrediente_id}.")
            return None

        if nombre:
            ingrediente.nombre = nombre
        if stock is not None:
            ingrediente.stock = stock
        if unidad:
            ingrediente.unidad = unidad

        if not IngredienteCRUD._try_commit(db):
            return None

        db.refresh(ingrediente)
        return ingrediente

    @staticmethod
    def borrar_ingrediente(db: Session, ingrediente_id: int):
        ingrediente = db.query(Ingrediente).get(ingrediente_id)
        if not ingrediente:
            print(f"No se encontró el ingrediente ID {ingrediente_id}.")
            return None

        db.delete(ingrediente)

        if not IngredienteCRUD._try_commit(db):
            return None

        return ingrediente




