import os
from ElementoMenu import CrearMenu
import customtkinter as ctk
from tkinter import ttk, Toplevel, Label, messagebox
from Ingrediente import Ingrediente
from Stock import Stock
import re
from PIL import Image
from CTkMessagebox import CTkMessagebox
from Pedido import Pedido
from BoletaFacade import BoletaFacade
import pandas as pd
from tkinter import filedialog
from Menu_catalog import get_default_menus
from menu_pdf import create_menu_pdf
from ctk_pdf_viewer import CTkPDFViewer
import os 
from tkinter.font import nametofont
from database import get_session
from crud.cliente_crud import ClienteCRUD
from crud.pedido_crud import PedidoCRUD
from database import get_session, engine, Base
from models import Cliente

# Crear tablas si no existen 
Base.metadata.create_all(bind=engine)


class AplicacionConPestanas(ctk.CTk):

    def __init__(self):
        super().__init__()
        
        self.title("Gestión de ingredientes y pedidos") # titulo ventana 
        self.geometry("870x700")  # tamaño de la ventana
        nametofont("TkHeadingFont").configure(size=14)  # tamaño de la fuente
        nametofont("TkDefaultFont").configure(size=11)   # tamaño de la fuente

        # widget para manejar las pestañas(tabview) y asigna la funcion on_tab_change que se ejecuta cuando cambie de pestaña
        self.tabview = ctk.CTkTabview(self,command=self.on_tab_change) 

        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)

        self.crear_pestanas()

    def actualizar_treeview(self):

        # borra los elementos existentes en el treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # inserta los ingredientes del stock en el treeview
        for ingrediente in self.stock.lista_ingredientes:
            # Values define las columnas: Nombre, unidad y cantidad
            self.tree.insert("", "end", values=(ingrediente.nombre,ingrediente.unidad, ingrediente.cantidad))    

    def on_tab_change(self):
        selected_tab = self.tabview.get()   # obtiene el nombre de la pestaña seleccionada
        if selected_tab == "Ingredientes":
            print('carga de ingredientes')
        if selected_tab == "Menu":
            self.actualizar_treeview()  # actualiza el treeview con los ingredientes del stock
        if selected_tab == "Pedido":
            self.actualizar_treeview()  # actualiza el treeview ver los pedidos
            print('pedido')
        if selected_tab == "Panel de compra":
            self.actualizar_treeview()  # actualiza el treeview para ver la carta
            print('Panel de compra')
        if selected_tab == "Cliente":
            self.actualizar_treeview()  # actualiza el treeview para ver el registro
            print('Cliente')    
        if selected_tab == "Graficos":
            self.actualizar_treeview()  # actualiza el treeview para ver los graficos   
            print('Graficos')

    def crear_pestanas(self):
        # se crean las pestañas(tabview) y se asocian las funciones que se ejecutan cuando cambie de pestaña
        self.tab6 = self.tabview.add("Cliente")
        self.tab3 = self.tabview.add("Ingredientes")  
        self.tab1 = self.tabview.add("Menu")
        self.tab4 = self.tabview.add("Panel de compra")  
        self.tab2 = self.tabview.add("Pedido")
        self.tab7 = self.tabview.add("Graficos")
        
        # se llama a las funciones que se ejecutan cuando cambie de pestaña
        self.configurar_pestana1()
        self.configurar_pestana2()
        self.configurar_pestana3()
        self._configurar_pestana_crear_menu()
        self._configurar_pestana_cliente()
        self._configurar_pestana_ver_graficos()

    def configurar_pestana3(self):
        # titulo de arriba
        label = ctk.CTkLabel(self.tab3, text="Carga de archivo CSV")
        label.pack(pady=20)

        # boton para seleccionar y cargar archivo CSV
        boton_cargar_csv = ctk.CTkButton(self.tab3, text="Cargar CSV", fg_color="#1976D2", text_color="white",command=self.cargar_csv)
        boton_cargar_csv.pack(pady=10)

        frame_superior = ctk.CTkFrame(self.tab3)
        frame_superior.pack(pady=10)

        frame_nombre = ctk.CTkFrame(frame_superior)
        frame_nombre.pack(side= "left", padx=10)

        frame_cantidad = ctk.CTkFrame(frame_superior)
        frame_cantidad.pack(side= "left", padx=10)

        label_nombre = ctk.CTkLabel(frame_nombre, text="Nombre:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_nombre)
        self.entry_nombre.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_cantidad, text="Cantidad:")
        label_cantidad.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_cantidad)
        self.entry_cantidad.pack(pady=5)

        self.boton_agregar = ctk.CTkButton(frame_superior, text="Agregar Ingrediente", command=self.agregar_ingrediente, fg_color="green")
        self.boton_agregar.pack(pady=10)    

        self.boton_eliminar = ctk.CTkButton(frame_superior, text="Eliminar Ingrediente", command=self.eliminar_ingrediente, fg_color="red")
        self.boton_eliminar.pack(pady=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(self.tab3)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los clientes
        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("ID", "Nombre", "Stock"), show="headings")
        self.treeview_clientes.heading("ID", text="ID")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.heading("Stock", text="Stock")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)

    def agregar_ingrediente(self):
        pass

    def eliminar_ingrediente(self): 
        pass

    def agregar_csv_al_stock(self):

        # verifica si hay un DataFrame cargado
        if self.df_csv is None:
            CTkMessagebox(title="Error", message="Primero debes cargar un archivo CSV.", icon="warning")
            return
        
        # verifica si el CSV tiene las columnas necesarias
        if 'nombre' not in self.df_csv.columns or 'cantidad' not in self.df_csv.columns:
            CTkMessagebox(title="Error", message="El CSV debe tener columnas 'nombre' y 'cantidad'.", icon="warning")
            return
        
        # recorre cada fila del CSV
        for _, row in self.df_csv.iterrows():  # 'iterrows()' devuelve pares (índice, fila) que se pueden recorrer como un diccionario
            nombre = str(row['nombre'])
            cantidad = str(row['cantidad'])
            unidad = str(row['unidad'])
            ingrediente = Ingrediente(nombre=nombre,unidad=unidad,cantidad=cantidad)
            self.stock.agregar_ingrediente(ingrediente)


        # Mensaje de confirmación y se actualiza el treeview
        CTkMessagebox(title="Stock Actualizado", message="Ingredientes agregados al stock correctamente.", icon="info")
        self.actualizar_treeview()   

    def cargar_csv(self):
        # ventana para seleccionar el archivo CSV desde el sistema 
        ruta_csv = filedialog.askopenfilename(  # 'filedialog.askopenfilename()' devuelve la ruta completa del archivo seleccionado
            title="Seleccione el archivo CSV",
            filetypes=(("CSV", "*.csv"), ("todos los archivos", "*.*"))
        )

        # si se selecciono el archivo, se lee
        if ruta_csv:
            try:
                # carga el archivo CSV
                self.df_csv = pd.read_csv(ruta_csv)  # "pd" = pandas

                # mostrar la tabla de los datos del CSV en la ventana
                self.mostrar_dataframe_en_tabla(self.df_csv)

                # configura el boton para agregar los datos al stock
                self.boton_agregar_stock.configure(command=self.agregar_csv_al_stock)
            except Exception as e:
                # si hay un error, muestra un mensaje de error
                CTkMessagebox(title="Error", message=f"No se pudo cargar el archivo CSV.\n{e}", icon="warning")

    def mostrar_dataframe_en_tabla(self, df):

        # si ya existe una tabla, se destruye
        if self.tabla_csv:
            self.tabla_csv.destroy()

        # crea una tabla con los datos del CSV
        self.tabla_csv = ttk.Treeview(self.frame_tabla_csv, columns=list(df.columns), show="headings")
        
        # configura encabezados y ancho de columnas
        for col in df.columns:
            self.tabla_csv.heading(col, text=col)       # titulo de columna
            self.tabla_csv.column(col, width=100, anchor="center")  # centra el texto

        # inserta cada fila del CSV en la tabla
        for _, row in df.iterrows():
            self.tabla_csv.insert("", "end", values=list(row))

        # muestra la tabla en la ventana
        self.tabla_csv.pack(expand=True, fill="both", padx=10, pady=10)

    def actualizar_treeview_pedido(self):

        # limpia la tabla pedidos
        for item in self.treeview_menu.get_children():
            self.treeview_menu.delete(item)

        # inserta los menus actuales en la tabla
        for menu in self.pedido.menus:
            self.treeview_menu.insert("", "end", values=(menu.nombre, menu.cantidad, f"${menu.precio:.2f}"))

    def _configurar_pestana_crear_menu(self):
        label = ctk.CTkLabel(self.tab4, text="Panel de compra")
        label.pack(pady=20)

        contenedor = ctk.CTkFrame(self.tab4)
        contenedor.pack(pady=10)

        frame_nombre = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_nombre.pack(side= "left", padx=10)

        frame_menu = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_menu.pack(side= "left", padx=10)

        frame_cantidad = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_cantidad.pack(side= "left", padx=10)

        label_nombre = ctk.CTkLabel(frame_nombre, text="Cliente:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_nombre)
        self.entry_nombre.pack(pady=5)

        label_menu = ctk.CTkLabel(frame_menu, text="Menu:")
        label_menu.pack(pady=5)
        self.entry_menu = ctk.CTkEntry(frame_menu)
        self.entry_menu.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_cantidad, text="Cantidad:")
        label_cantidad.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_cantidad)
        self.entry_cantidad.pack(pady=5)

        self.boton_añadir = ctk.CTkButton(contenedor, text="Añadir al pedido", command=self.Añadir_pedido)
        self.boton_añadir.pack(pady=10) 

        self.boton_eliminar = ctk.CTkButton(contenedor, text="Eliminar pedido", command=self.eliminar_pedido, fg_color="red")
        self.boton_eliminar.pack(pady=10)
        
        self.boton_finalizar = ctk.CTkButton(contenedor, text="Finalizar pedido", command=self.finalizar_pedido, fg_color="green")
        self.boton_finalizar.pack(pady=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(self.tab4)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los clientes
        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("ID", "Menu", "Precio Unitario", "Cantidad", "Subtotal"), show="headings")
        self.treeview_clientes.heading("ID", text="ID")
        self.treeview_clientes.heading("Menu", text="Menu")
        self.treeview_clientes.heading("Precio Unitario", text="Precio Unitario")
        self.treeview_clientes.heading("Cantidad", text="Cantidad")
        self.treeview_clientes.heading("Subtotal", text="Subtotal")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)

        

    def Añadir_pedido(self):
        pass

    def eliminar_pedido(self):
        pass
    
    def finalizar_pedido(self):
        pass


    def _configurar_pestana_cliente(self):
        label = ctk.CTkLabel(self.tab6, text="Gestión de clientes")
        label.pack(pady=10)

        contenedor = ctk.CTkFrame(self.tab6)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)

        frame_formulario = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_formulario.pack(pady=10)

        frame_nombre = ctk.CTkFrame(frame_formulario, fg_color="transparent")
        frame_nombre.pack(side="left", padx=20)

        ctk.CTkLabel(frame_nombre, text="Nombre:").pack()
        self.entry_nombre = ctk.CTkEntry(frame_nombre)
        self.entry_nombre.pack()

        frame_email = ctk.CTkFrame(frame_formulario, fg_color="transparent")
        frame_email.pack(side="left", padx=20)

        ctk.CTkLabel(frame_email, text="Correo:").pack()
        self.entry_email = ctk.CTkEntry(frame_email, placeholder_text="usuario123")
        self.entry_email.pack()

        frame_dominio = ctk.CTkFrame(frame_formulario, fg_color="transparent")
        frame_dominio.pack(side="left", padx=20)

        ctk.CTkLabel(frame_dominio, text="Dominio:").pack()

        self.combo_dominio = ctk.CTkComboBox(
            frame_dominio,
            values=["@gmail.com", "@hotmail.com", "@yahoo.com"]
        )
        self.combo_dominio.set("@gmail.com")   # Valor inicial correcto
        self.combo_dominio.pack()

        self.boton_crear_cliente = ctk.CTkButton(frame_nombre, text="Crear Cliente",fg_color="green", command=self.Crear_cliente)
        self.boton_crear_cliente.pack(pady=10)

        self.boton_editar_cliente = ctk.CTkButton(frame_email, text="Editar Cliente",command=self.Editar_cliente)
        self.boton_editar_cliente.pack(pady=10)

        self.boton_eliminar_cliente = ctk.CTkButton(frame_dominio, text="Eliminar Cliente",fg_color="red", command=self.Eliminar_cliente)
        self.boton_eliminar_cliente.pack(pady=10)

    
        frame_inferior = ctk.CTkFrame(contenedor)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        self.treeview_clientes = ttk.Treeview(frame_inferior,columns=("Email", "Nombre"),show="headings")
        self.treeview_clientes.heading("Email", text="Email")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.pack(fill="both", expand=True)

        self.cargar_clientes()


    def cargar_clientes(self):
        db = next(get_session())
        datos = ClienteCRUD.leer_clientes(db)
        db.close()

        # Limpiar tabla
        self.treeview_clientes.delete(*self.treeview_clientes.get_children())

        # Insertar clientes
        for c in datos:
            self.treeview_clientes.insert("", "end", values=(c.email, c.nombre))


    def Crear_cliente(self):
        nombre = self.entry_nombre.get().strip()
        parte_email = self.entry_email.get().strip()
        dominio = self.combo_dominio.get().strip()

        # Validaciones
        if not nombre:
            messagebox.showwarning("Error", "Debe ingresar el nombre.")
            return

        if not parte_email:
            messagebox.showwarning("Error", "Debe escribir la parte antes del @ del correo.")
            return

        if not dominio:
            messagebox.showwarning("Error", "Debe seleccionar un dominio.")
            return

        # Armar correo final
        email = f"{parte_email}{dominio}".lower()

        # Validación regex
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messagebox.showwarning("Error", "El correo no tiene un formato válido.")
            return

        db = next(get_session())

        # Pauta: usar filter + lambda para validar unicidad
        existe = list(filter(lambda c: c.email == email, ClienteCRUD.leer_clientes(db)))
        if existe:
            messagebox.showwarning("Error", "El correo ya está registrado.")
            db.close()
            return

        ClienteCRUD.crear_cliente(db, nombre, email)
        db.close()

        self.cargar_clientes()

        self.entry_nombre.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.combo_dominio.set("@gmail.com")

        messagebox.showinfo("Éxito", "Cliente creado correctamente.")

    
    def Eliminar_cliente(self):
        seleccion = self.treeview_clientes.selection()

        if not seleccion:
            messagebox.showwarning("Error", "Seleccione un cliente para eliminar.")
            return

        email = self.treeview_clientes.item(seleccion[0], "values")[0]

        db = next(get_session())

        cliente = db.query(Cliente).filter_by(email=email).first()

        if cliente and cliente.pedidos:
            messagebox.showwarning("Error", "No se puede eliminar: tiene pedidos asociados.")
            db.close()
            return

        ClienteCRUD.borrar_cliente(db, email)
        db.close()

        self.cargar_clientes()
        messagebox.showinfo("Éxito", "Cliente eliminado.")



    def Editar_cliente(self):
        seleccion = self.treeview_clientes.selection()

        if not seleccion:
            messagebox.showwarning("Error", "Seleccione un cliente para editar.")
            return

        old_email = self.treeview_clientes.item(seleccion[0], "values")[0]

        nombre = self.entry_nombre.get().strip()
        parte_email = self.entry_email.get().strip()
        dominio = self.combo_dominio.get().strip()

        if not nombre or not parte_email:
            messagebox.showwarning("Error", "Debe ingresar nombre y correo.")
            return

        email = f"{parte_email}{dominio}".lower()

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messagebox.showwarning("Error", "Correo no válido.")
            return

        db = next(get_session())
        ClienteCRUD.actualizar_cliente(db, old_email, nombre, email)
        db.close()

        self.cargar_clientes()
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")



    def configurar_pestana1(self):

        label = ctk.CTkLabel(self.tab1, text="Menu")
        label.pack(pady=20)
        # Dividir la Pestaña 1 en dos frames
        frame_formulario = ctk.CTkFrame(self.tab1)
        frame_formulario.pack(pady=10)

        self.boton_editar = ctk.CTkButton(frame_formulario, text="Editar Menu", command=self.editar_menu)
        self.boton_editar.pack(side = "left", pady=10, padx=10)

        self.boton_eliminar = ctk.CTkButton(frame_formulario, text="Eliminar Menu", command=self.eliminar_menu, fg_color="red")
        self.boton_eliminar.pack(side = "left", pady=10, padx=10)

        self.nueva_menu = ctk.CTkButton(frame_formulario, text="Nueva Menu", command=self.crear_menu, fg_color="green")
        self.nueva_menu.pack(side = "left", pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(self.tab1)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los clientes
        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("ID", "Nombre", "Precio", "Descripcion"), show="headings")
        self.treeview_clientes.heading("ID", text="ID")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.heading("Precio", text="Precio")
        self.treeview_clientes.heading("Descripcion", text="Descripcion")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)

    def editar_menu(self):
        pass

    def eliminar_menu(self):
        pass

    def crear_menu(self):
        """Abre una ventana para crear un nuevo menú"""
        ventana_menu = ctk.CTkToplevel(self)
        ventana_menu.title("Crear Nuevo Menú")
        ventana_menu.geometry("600x800")
        ventana_menu.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(ventana_menu)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        label_titulo = ctk.CTkLabel(main_frame, text="Crear Nuevo Menú", font=("Helvetica", 16, "bold"))
        label_titulo.pack(pady=10)
        
        # Frame para datos básicos del menú
        frame_datos = ctk.CTkFrame(main_frame)
        frame_datos.pack(pady=10, padx=10, fill="x")
        
        # Nombre del menú
        label_nombre = ctk.CTkLabel(frame_datos, text="Nombre del Menú:")
        label_nombre.pack(padx=10, pady=5)
        entry_nombre_menu = ctk.CTkEntry(frame_datos)
        entry_nombre_menu.pack(padx=10, pady=5)
        
        # Precio del menú
        label_precio=ctk.CTkLabel(frame_datos, text="Precio:")
        label_precio.pack(padx=10, pady=5)
        entry_precio = ctk.CTkEntry(frame_datos, placeholder_text="Ej: 5000")
        entry_precio.pack(padx=10, pady=5)
        
        # Descripción del menú
        label_descripcion=ctk.CTkLabel(frame_datos, text="Descripción:")
        label_descripcion.pack(padx=10, pady=5)
        entry_descripcion = ctk.CTkTextbox(frame_datos, height=80)
        entry_descripcion.pack(padx=10, pady=5)
        
        # Frame para selección de ingredientes
        frame_ingredientes = ctk.CTkFrame(main_frame)
        frame_ingredientes.pack(pady=10, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(frame_ingredientes, text="Ingredientes del Menú:").pack(padx=10, pady=5)
        
        # Frame para agregar ingredientes
        frame_agregar = ctk.CTkFrame(frame_ingredientes)
        frame_agregar.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(frame_agregar, text="Ingrediente:").pack(side="left", padx=5)
        entry_ingrediente = ctk.CTkEntry(frame_agregar, width=150)
        entry_ingrediente.pack(side="left", padx=5)
        
        ctk.CTkLabel(frame_agregar, text="Cantidad:").pack(side="left", padx=5)
        entry_cantidad = ctk.CTkEntry(frame_agregar, width=80)
        entry_cantidad.pack(side="left", padx=5)
        
        boton_agregar = ctk.CTkButton(frame_agregar, text="+", width=40)
        boton_agregar.pack(side="left", padx=5)
        
        # Frame para lista de ingredientes agregados
        frame_lista = ctk.CTkScrollableFrame(frame_ingredientes, height=100)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame_lista, text="Lista de ingredientes agregados", text_color="gray").pack(pady=10)
        
        # Frame para botones de acción
        frame_botones = ctk.CTkFrame(main_frame)
        frame_botones.pack(side="bottom", pady=10, fill="x")  # Cambiado aquí
        
        btn_guardar = ctk.CTkButton(frame_botones, text="Guardar Menú", fg_color="green", width=150)
        btn_guardar.pack(side="left", padx=10, expand=True)  # Cambiado aquí
        
        btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", command=ventana_menu.destroy, fg_color="red", width=150)
        btn_cancelar.pack(side="left", padx=10, expand=True)  # Cambiado aquí


    def tarjeta_click(self, event, menu):
        suficiente_stock = True
        if not self.stock.lista_ingredientes:
            suficiente_stock=False
        
        for ingrediente_necesario in menu.ingredientes:
            for ingrediente_stock in self.stock.lista_ingredientes:
                if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                    if int(ingrediente_stock.cantidad) < int(ingrediente_necesario.cantidad):
                        suficiente_stock = False
                        break
            if not suficiente_stock:
                break
        
        if suficiente_stock:
            for ingrediente_necesario in menu.ingredientes:
                for ingrediente_stock in self.stock.lista_ingredientes:
                    if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                        ingrediente_stock.cantidad = str(int(ingrediente_stock.cantidad) - int(ingrediente_necesario.cantidad))
            
            self.pedido.agregar_menu(menu)
            self.actualizar_treeview_pedido()
            total = self.pedido.calcular_total()
            self.label_total.configure(text=f"Total: ${total:.2f}")
        
        else:
            CTkMessagebox(title="Stock Insuficiente", message=f"No hay suficientes ingredientes para preparar el menú '{menu.nombre}'.", icon="warning")

    def cargar_icono_menu(self, ruta_icono):
        base_path = os.path.dirname(os.path.abspath(__file__))
        ruta_completa = os.path.join(base_path, ruta_icono)

        imagen = Image.open(ruta_completa)
        icono_menu = ctk.CTkImage(imagen, size=(64, 64))
        return icono_menu

    def generar_menus(self):
    # Limpiar las tarjetas existentes
        for widget in self.tarjetas_frame.winfo_children():
            widget.destroy()

        self.menus_creados = [] 

        # Filtrar los menús que tienen todos los ingredientes disponibles en stock
        menus_disponibles = [m for m in self.menus if self.menu_disponible(m)]

        if not menus_disponibles:
            CTkMessagebox(title="Carta vacía", message="No hay menús con ingredientes suficientes en stock.", icon="warning")
            return

        # Crear tarjetas solo para los menús disponibles
        for menu in menus_disponibles:
            self.crear_tarjeta(menu)

        CTkMessagebox(title="Carta generada", message="Los menús disponibles se han generado correctamente.", icon="info")

    def menu_disponible(self, menu):
        if not getattr(menu, "ingredientes", None):
            return False
        for ingr_req in menu.ingredientes:
            encontrado = False
            for ingr_stock in self.stock.lista_ingredientes:
                if ingr_req.nombre == ingr_stock.nombre:
                    try:
                        if int(ingr_stock.cantidad) >= int(ingr_req.cantidad):
                            encontrado = True
                            break
                    except Exception:
                        # si hay datos no numéricos, considerar no disponible
                        return False
            if not encontrado:
                return False
        return True

    def eliminar_menu(self):
        seleccionado = self.treeview_menu.selection()
        if not seleccionado:
            CTkMessagebox(title="Error", message="Por favor, selecciona un menú para eliminar.", icon="warning")
            return

        item = self.treeview_menu.item(seleccionado)
        nombre_menu = item['values'][0]
        cantidad_menu = int(item['values'][1])  # Obtener la cantidad del menú a eliminar

        # Recuperar el menú completo del pedido
        menu_a_eliminar = next((menu for menu in self.pedido.menus if menu.nombre == nombre_menu), None)

        if not menu_a_eliminar:
            CTkMessagebox(title="Error", message="No se encontró el menú seleccionado en el pedido.", icon="warning")
            return

        # Devolver los ingredientes al stock
        for ingrediente_necesario in menu_a_eliminar.ingredientes:
            for _ in range(cantidad_menu):  # Iterar según la cantidad del menú
                for ingrediente_stock in self.stock.lista_ingredientes:
                    if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                        ingrediente_stock.cantidad = str(int(ingrediente_stock.cantidad) + int(ingrediente_necesario.cantidad))
                        break  # Salir del bucle interno una vez que se ha encontrado y actualizado el ingrediente

        # Eliminar el menú del pedido
        exito = self.pedido.eliminar_menu(nombre_menu)

        if exito:
            self.actualizar_treeview_pedido()
            total = self.pedido.calcular_total()
            self.label_total.configure(text=f"Total: ${total:.2f}")
            CTkMessagebox(title="Menú Eliminado", message=f"El menú '{nombre_menu}' ha sido eliminado del pedido y los ingredientes devueltos al stock.", icon="info")
        else:
            CTkMessagebox(title="Error", message=f"No se pudo eliminar el menú '{nombre_menu}' del pedido.", icon="warning")

    def generar_boleta(self):
        if not self.pedido.menus:
            CTkMessagebox(title="Error", message="No hay menús en el pedido para generar una boleta.", icon="warning")
            return

        try:
            boleta = BoletaFacade(self.pedido)
            mensaje = boleta.generar_boleta()
            CTkMessagebox(title="Boleta Generada", message=mensaje, icon="info")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo generar la boleta.\n{e}", icon="warning")


    def configurar_pestana2(self):
        frame_superior = ctk.CTkFrame(self.tab2)
        frame_superior.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        frame_intermedio = ctk.CTkFrame(self.tab2)
        frame_intermedio.pack(side="top", fill="x", padx=10, pady=5)

        label_filtro = ctk.CTkLabel(frame_superior, text="Filtro:")
        label_filtro.pack(side="left", padx=10)
        self.entry_filtro = ctk.CTkEntry(frame_superior)
        self.entry_filtro.pack(side="left", padx=10)

        self.boton_filtrar = ctk.CTkButton(frame_superior, text="Filtrar", command=self.filtrar_menus)
        self.boton_filtrar.pack(side="left", padx=10)
        
        self.boton_eliminar_menu = ctk.CTkButton(frame_superior, text="Eliminar Menú", command=self.eliminar_menu, fg_color="red")
        self.boton_eliminar_menu.pack(side="right", padx=10)

        self.treeview_menu = ttk.Treeview(frame_intermedio, columns=("ID", "Fecha", "Cliente", "Total"), show="headings")
        self.treeview_menu.heading("ID", text="ID")
        self.treeview_menu.heading("Fecha", text="Fecha")
        self.treeview_menu.heading("Cliente", text="Cliente")
        self.treeview_menu.heading("Total", text="Total")
        self.treeview_menu.pack(expand=True, fill="both", padx=10, pady=10)

        frame_inferior = ctk.CTkFrame(self.tab2)
        frame_inferior.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        label_arriba = ctk.CTkLabel(frame_inferior, text="Detalle del pedido:")
        label_arriba.pack(side="top", pady=10)

        self.treeview_menu = ttk.Treeview(frame_inferior, columns=("Menu", "Cantidad", "Precio Unitario", "Subtotal"), show="headings")
        self.treeview_menu.heading("Menu", text="Menu")
        self.treeview_menu.heading("Cantidad", text="Cantidad")
        self.treeview_menu.heading("Precio Unitario", text="Precio Unitario")
        self.treeview_menu.heading("Subtotal", text="Subtotal")
        self.treeview_menu.pack(expand=True, fill="both", padx=10, pady=10)

    def filtrar_menus(self):
        pass

    def _configurar_pestana_ver_graficos(self):
        label = ctk.CTkLabel(self.tab7, text="Graficos")
        label.pack(pady=10)
        
        contenedor = ctk.CTkFrame(self.tab7)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)

        frame_superior = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_superior.pack(pady=10, padx=30)

        label_grafico = ctk.CTkLabel(frame_superior, text="Grafico:")
        label_grafico.pack(pady=5)
        self.combo_unidad = ctk.CTkComboBox(frame_superior, values=["Ventas diarias", "Menu más comprado"])
        self.combo_unidad.pack(pady=10)

        self.boton_cargar_grafico = ctk.CTkButton(frame_superior, text="Cargar Grafico", command=self.cargar_grafico)
        self.boton_cargar_grafico.pack(pady=10)

    def cargar_grafico(self):
        pass

    def crear_tarjeta(self, menu):
        cols = 6
        num_tarjetas = len(self.menus_creados)
        fila = num_tarjetas // cols
        columna = num_tarjetas % cols

        tarjeta = ctk.CTkFrame(
            self.tarjetas_frame,
            corner_radius=10,
            border_width=1,
            border_color="#4CAF50",
            width=64,
            height=140,
            fg_color="gray",
        )
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")

        tarjeta.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))
        tarjeta.bind("<Enter>", lambda event: tarjeta.configure(border_color="#FF0000"))
        tarjeta.bind("<Leave>", lambda event: tarjeta.configure(border_color="#4CAF50"))

        if getattr(menu, "icono_path", None):
            try:
                icono = self.cargar_icono_menu(menu.icono_path)
                imagen_label = ctk.CTkLabel(
                    tarjeta, image=icono, width=64, height=64, text="", bg_color="transparent"
                )
                imagen_label.image = icono
                imagen_label.pack(anchor="center", pady=5, padx=10)
                imagen_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))
            except Exception as e:
                print(f"No se pudo cargar la imagen '{menu.icono_path}': {e}")

        texto_label = ctk.CTkLabel(
            tarjeta,
            text=f"{menu.nombre}",
            text_color="black",
            font=("Helvetica", 12, "bold"),
            bg_color="transparent",
        )
        texto_label.pack(anchor="center", pady=1)
        texto_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))

        self.menus_creados.append(menu)

    def validar_nombre(self, nombre):
        if re.match(r"^[a-zA-Z\s]+$", nombre):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="El nombre debe contener solo letras y espacios.", icon="warning")
            return False

    def validar_cantidad(self, cantidad):
        if cantidad.isdigit():
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="La cantidad debe ser un número entero positivo.", icon="warning")
            return False

    def ingresar_ingrediente(self):
        nombre = self.entry_nombre.get()
        nombre = nombre.title()
        unidad = self.combo_unidad.get()
        cantidad = self.entry_cantidad.get()
        
        if not self.validar_nombre(nombre) or not self.validar_cantidad(cantidad):
            return
        
        ingrediente = Ingrediente(nombre=nombre, unidad=unidad, cantidad=cantidad)
        self.stock.agregar_ingrediente(ingrediente)
        self.actualizar_treeview()

    def eliminar_ingrediente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            CTkMessagebox(title="Error", message="Por favor, selecciona un ingrediente para eliminar.", icon="warning")
            return
        # proceso de borrar el item seleccionado
        item = self.tree.item(seleccionado)
        nombre_ingrediente = item['values'][0]
        exito = self.stock.eliminar_ingrediente(nombre_ingrediente)

        if exito:
            self.actualizar_treeview()
            CTkMessagebox(title="Ingrediente Eliminado", message=f"El ingrediente '{nombre_ingrediente}' ha sido eliminado del stock.", icon="info")
        else:
            CTkMessagebox(title="Error", message=f"No se pudo encontrar el ingrediente '{nombre_ingrediente}' en el stock.", icon="warning")

    def actualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for ingrediente in self.stock.lista_ingredientes:
            self.tree.insert("", "end", values=(ingrediente.nombre, ingrediente.unidad, ingrediente.cantidad))      

if __name__ == "__main__":
    import customtkinter as ctk
    from tkinter import ttk

    ctk.set_appearance_mode("Dark")  
    ctk.set_default_color_theme("blue") 
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)

    app = AplicacionConPestanas()

    try:
        style = ttk.Style(app)   
        style.theme_use("clam")
    except Exception:
        pass

    app.mainloop()