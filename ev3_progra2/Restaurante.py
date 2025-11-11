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

class AplicacionConPestanas(ctk.CTk):

    def __init__(self):
        super().__init__()
        
        self.title("Gestión de ingredientes y pedidos") # titulo ventana 
        self.geometry("870x700")  # tamaño de la ventana
        nametofont("TkHeadingFont").configure(size=14)  # tamaño de la fuente
        nametofont("TkDefaultFont").configure(size=11)   # tamaño de la fuente

        self.stock = Stock()  # objeto Stock
        self.menus_creados = set()  # set para guardar los nombres de los menus creados

        self.pedido = Pedido()  # objeto Pedido para manejar menus agregados 

        self.menus = get_default_menus()  # lista de menus predefinidos desde el catalogo

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
        if selected_tab == "carga de ingredientes":
            print('carga de ingredientes')
        if selected_tab == "Stock":
            self.actualizar_treeview()  # actualiza el treeview con los ingredientes del stock
        if selected_tab == "Pedido":
            self.actualizar_treeview()  # actualiza el treeview ver los pedidos
            print('pedido')
        if selected_tab == "Carta restorante":
            self.actualizar_treeview()  # actualiza el treeview para ver la carta
            print('Carta restorante')
        if selected_tab == "Boleta":
            self.actualizar_treeview()  # actualiza el treeview para ver la boleta
            print('Boleta')       

    def crear_pestanas(self):
        # se crean las pestañas(tabview) y se asocian las funciones que se ejecutan cuando cambie de pestaña
        self.tab3 = self.tabview.add("carga de ingredientes")  
        self.tab1 = self.tabview.add("Stock")
        self.tab4 = self.tabview.add("Carta restorante")  
        self.tab2 = self.tabview.add("Pedido")
        self.tab5 = self.tabview.add("Boleta")
        
        # se llama a las funciones que se ejecutan cuando cambie de pestaña
        self.configurar_pestana1()
        self.configurar_pestana2()
        self.configurar_pestana3()
        self._configurar_pestana_crear_menu()
        self._configurar_pestana_ver_boleta()

    def configurar_pestana3(self):
        
        # titulo de arriba
        label = ctk.CTkLabel(self.tab3, text="Carga de archivo CSV")
        label.pack(pady=20)

        # boton para seleccionar y cargar archivo CSV
        boton_cargar_csv = ctk.CTkButton(self.tab3, text="Cargar CSV", fg_color="#1976D2", text_color="white",command=self.cargar_csv)

        boton_cargar_csv.pack(pady=10)

        # contenedor para mostrar la tabla de los datos del CSV
        self.frame_tabla_csv = ctk.CTkFrame(self.tab3)
        self.frame_tabla_csv.pack(fill="both", expand=True, padx=10, pady=10)

        # Variables para manejar contenido CSV
        self.df_csv = None                  # DataFrame con los datos del CSV
        self.tabla_csv = None               # Widget para mostrar la tabla de los datos del CSV

        # boton para agregar los datos al stock
        self.boton_agregar_stock = ctk.CTkButton(self.frame_tabla_csv, text="Agregar al Stock")
        self.boton_agregar_stock.pack(side="bottom", pady=10)

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
        contenedor = ctk.CTkFrame(self.tab4)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)
        
        # boton para generar la carta PDF
        boton_menu = ctk.CTkButton(contenedor,text="Generar Carta (PDF)",command=self.generar_y_mostrar_carta_pdf)
        boton_menu.pack(pady=10)

        # marco para mostrar la carta PDF
        self.pdf_frame_carta = ctk.CTkFrame(contenedor)
        self.pdf_frame_carta.pack(expand=True, fill="both", padx=10, pady=10)

        self.pdf_viewer_carta = None # se inicializa vacio hasta que se genere el PDF

    def generar_y_mostrar_carta_pdf(self):
        try:
            # Filtrar los menús disponibles antes de crear el PDF
            menus_disponibles = [m for m in self.menus if self.menu_disponible(m)]

            # si no hay menús disponibles, muestra un mensaje de error
            if not menus_disponibles:
                CTkMessagebox(title="Carta vacía", message="No hay menús con ingredientes suficientes en stock.", icon="warning")
                return
            

            # nombre del archivo PDF
            pdf_path = "carta.pdf"

            # crea el PDF con los menús disponibles
            create_menu_pdf(
                menus_disponibles, 
                pdf_path,
                titulo_negocio="Restaurante",
                subtitulo="Carta Primavera 2025",
                moneda="$"
            )

            # si ya hay un PDF abieto, se destruye para mostrar el nuevo
            if self.pdf_viewer_carta is not None:
                try:
                    self.pdf_viewer_carta.pack_forget()
                    self.pdf_viewer_carta.destroy()
                except Exception:
                    pass
                self.pdf_viewer_carta = None

            # Muestra el PDF dentro del marco creado anteriormente
            abs_pdf = os.path.abspath(pdf_path) # se convierte la ruta relativa a absoluta
            self.pdf_viewer_carta = CTkPDFViewer(self.pdf_frame_carta, file=abs_pdf)
            self.pdf_viewer_carta.pack(expand=True, fill="both")

        except Exception as e:
            # Muestra un mensaje de error si hay algún error
            CTkMessagebox(title="Error", message=f"No se pudo generar/mostrar la carta.\n{e}", icon="warning")

    def _configurar_pestana_ver_boleta(self):
        contenedor = ctk.CTkFrame(self.tab5)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)
    
        boton_boleta = ctk.CTkButton(
            contenedor,
            text="Mostrar Boleta (PDF)",
            command=self.mostrar_boleta
        )
        boton_boleta.pack(pady=10)
    
        self.pdf_frame_boleta = ctk.CTkFrame(contenedor)
        self.pdf_frame_boleta.pack(expand=True, fill="both", padx=10, pady=10)
    
        self.pdf_viewer_boleta = None

    def mostrar_boleta(self):
        try:
            pdf_path = "boleta.pdf"
            if not os.path.exists(pdf_path):
                CTkMessagebox(title="Error", message="Primero debes generar una boleta.", icon="warning")
                return

            # Si ya hay un visor anterior, se destruye
            if self.pdf_viewer_boleta is not None:
                try:
                    self.pdf_viewer_boleta.pack_forget()
                    self.pdf_viewer_boleta.destroy()
                except Exception:
                    pass
                self.pdf_viewer_boleta = None

            abs_pdf = os.path.abspath(pdf_path)
            self.pdf_viewer_boleta = CTkPDFViewer(self.pdf_frame_boleta, file=abs_pdf)
            self.pdf_viewer_boleta.pack(expand=True, fill="both")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo mostrar la boleta.\n{e}", icon="warning")


    def configurar_pestana1(self):
        # Dividir la Pestaña 1 en dos frames
        frame_formulario = ctk.CTkFrame(self.tab1)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario en el primer frame
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Unidad:")
        label_cantidad.pack(pady=5)
        self.combo_unidad = ctk.CTkComboBox(frame_formulario, values=["unidad"])
        self.combo_unidad.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.pack(pady=5)

        self.boton_ingresar = ctk.CTkButton(frame_formulario, text="Ingresar Ingrediente")
        self.boton_ingresar.configure(command=self.ingresar_ingrediente)
        self.boton_ingresar.pack(pady=10)

        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white")
        self.boton_eliminar.configure(command=self.eliminar_ingrediente)
        self.boton_eliminar.pack(pady=10)

        self.tree = ttk.Treeview(self.tab1, columns=("Nombre", "Unidad", "Cantidad"), show="headings",height=25)
        
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_generar_menu = ctk.CTkButton(frame_treeview, text="Generar Menú", command=self.generar_menus)
        self.boton_generar_menu.pack(pady=10)

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

        self.tarjetas_frame = ctk.CTkFrame(frame_superior)
        self.tarjetas_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_eliminar_menu = ctk.CTkButton(frame_intermedio, text="Eliminar Menú", command=self.eliminar_menu)
        self.boton_eliminar_menu.pack(side="right", padx=10)

        self.label_total = ctk.CTkLabel(frame_intermedio, text="Total: $0.00", anchor="e", font=("Helvetica", 12, "bold"))
        self.label_total.pack(side="right", padx=10)

        frame_inferior = ctk.CTkFrame(self.tab2)
        frame_inferior.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        self.treeview_menu = ttk.Treeview(frame_inferior, columns=("Nombre", "Cantidad", "Precio Unitario"), show="headings")
        self.treeview_menu.heading("Nombre", text="Nombre del Menú")
        self.treeview_menu.heading("Cantidad", text="Cantidad")
        self.treeview_menu.heading("Precio Unitario", text="Precio Unitario")
        self.treeview_menu.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_generar_boleta=ctk.CTkButton(frame_inferior,text="Generar Boleta",command=self.generar_boleta)
        self.boton_generar_boleta.pack(side="bottom",pady=10)

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