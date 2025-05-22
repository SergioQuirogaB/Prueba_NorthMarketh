import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from urllib.request import urlopen
from urllib.error import URLError
import json
from datetime import datetime
import re

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry("500x700")
        self.resizable(False, False)
        
        self.tema = {
            "bg": "#ffffff",
            "fg": "#2d3436",
            "button_bg": "#f1f2f6",
            "button_fg": "#2d3436",
            "entry_bg": "#f1f2f6",
            "entry_fg": "#2d3436",
            "accent": "#0984e3",
            "card_bg": "#f1f2f6",
            "success": "#00b894",
            "error": "#d63031"
        }
        
        # variables
        self.password_visible = False
        self.characters_data = []
        self.current_page = 1
        self.items_per_page = 6
        self.filter_status = "all"
        self.filter_species = "all"
        self.modo_registro = False
        
        # Crear base de datos si no existe
        self.crear_base_datos()
        
        self.configurar_estilo()
        
        self.configure(bg="#f4f4f4")
        self.card = tk.Frame(self, bg="white", bd=0, highlightthickness=0)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=370, height=470)
        self.card.update()
        self.card.after(10, lambda: self.card.config(highlightbackground="#e0e0e0", highlightthickness=1))
        self.card.tkraise()
        
        self.shadow = tk.Frame(self, bg="#d1d1d1", bd=0, highlightthickness=0)
        self.shadow.place(relx=0.5, rely=0.5, anchor="center", width=380, height=480, y=8, x=4)
        self.shadow.lower(self.card)
        
        self.frame = ttk.Frame(self.card, padding=20, style="Card.TFrame")
        self.frame.pack(fill="both", expand=True)
        
        self.label = ttk.Label(
            self.frame, 
            text="NorthMarket",
            font=("Segoe UI", 26, "bold"),
            foreground=self.tema["accent"]
        )
        self.label.pack(pady=(0, 2))
        self.subtitle = ttk.Label(
            self.frame,
            text="Sistema de Autenticación",
            font=("Segoe UI", 12),
            foreground=self.tema["fg"]
        )
        self.subtitle.pack(pady=(0, 18))
        self.input_frame = ttk.Frame(self.frame)
        self.input_frame.pack(fill="x", pady=0)
        
        self.usuario_label = ttk.Label(
            self.input_frame,
            text="Usuario",
            font=("Segoe UI", 11),
            foreground=self.tema["fg"]
        )
        self.usuario_label.pack(anchor="w", pady=(0, 2))
        
        self.usuario = ttk.Entry(
            self.input_frame,
            font=("Segoe UI", 11)
        )
        self.usuario.pack(fill="x", pady=(0, 8), ipady=4)
        self.usuario.bind('<Return>', lambda e: self.password.focus())
        
        self.password_label = ttk.Label(
            self.input_frame,
            text="Contraseña",
            font=("Segoe UI", 11),
            foreground=self.tema["fg"]
        )
        self.password_label.pack(anchor="w", pady=(0, 2))
        
        #btn de ojo
        password_container = ttk.Frame(self.input_frame)
        password_container.pack(fill="x", pady=(0, 8))
        
        self.password = ttk.Entry(
            password_container,
            show="•",
            font=("Segoe UI", 11)
        )
        self.password.pack(side="left", fill="x", expand=True, ipady=4)
        self.password.bind('<Return>', lambda e: self.verificar_login())
        
        self.toggle_password_button = ttk.Button(
            password_container,
            text="👁️",
            width=3,
            command=self.toggle_password_visibility
        )
        self.toggle_password_button.pack(side="right", padx=(5, 0))
        
        self.remember_var = tk.BooleanVar(value=False)
        self.remember_checkbox = ttk.Checkbutton(
            self.input_frame,
            text="Recordar usuario",
            variable=self.remember_var,
            style="Accent.TCheckbutton"
        )
        self.remember_checkbox.pack(anchor="w", pady=(0, 5))
        
        self.mensaje = ttk.Label(
            self.input_frame,
            text="",
            font=("Segoe UI", 10),
            foreground=self.tema["error"],
            wraplength=320,
            justify="center"
        )
        self.mensaje.pack(pady=(0, 5))
        
        self.login_button = ttk.Button(
            self.input_frame,
            text="Iniciar Sesión",
            command=self.verificar_login,
            style="TButton"
        )
        self.login_button.pack(fill="x", pady=(5, 8), ipady=4)
        self.toggle_mode = ttk.Button(
            self.input_frame,
            text="¿No tienes cuenta? Regístrate",
            command=self.toggle_modo,
            style="Link.TButton"
        )
        self.toggle_mode.pack(pady=(0, 8))
        
        self.footer = ttk.Label(
            self.frame,
            text="© 2025 NorthMarket - SERGIO QUIROGA",
            font=("Segoe UI", 8),
            foreground=self.tema["fg"]
        )
        self.footer.pack(side="bottom", pady=0)

    def configurar_estilo(self):
        """Configura los estilos de la aplicación"""
        style = ttk.Style()
        
        style.configure("TFrame", background=self.tema["bg"])
        style.configure("TLabel", background="white", foreground=self.tema["fg"])
        style.configure("TButton", 
                       background=self.tema["button_bg"],
                       foreground=self.tema["button_fg"],
                       font=("Segoe UI", 11),
                       padding=8,
                       borderwidth=0,
                       relief="flat")
        style.configure("TEntry", 
                       fieldbackground=self.tema["entry_bg"],
                       foreground=self.tema["entry_fg"],
                       padding=8,
                       borderwidth=0)
        
        style.configure("Accent.TButton",
                       background=self.tema["accent"],
                       foreground="white",
                       font=("Segoe UI", 12, "bold"),
                       padding=10,
                       borderwidth=0,
                       relief="flat")
        style.map("Accent.TButton",
                  background=[('active', '#1877f2')])
        
        style.configure("Link.TButton",
                       background="white",
                       foreground=self.tema["accent"],
                       font=("Segoe UI", 11),
                       borderwidth=0)
        
        style.configure("Accent.TCheckbutton",
                       background="white",
                       foreground=self.tema["fg"],
                       font=("Segoe UI", 10))
        
        style.configure("Card.TFrame",
                       background="white",
                       relief="flat",
                       borderwidth=0)

    def toggle_modo(self):
        """Alterna entre modo login y registro"""
        self.modo_registro = not self.modo_registro
        
        if self.modo_registro:
            self.login_button.configure(text="Registrarse")
            self.toggle_mode.configure(text="¿Ya tienes cuenta? Inicia sesión")
            self.remember_checkbox.pack_forget()
        else:
            self.login_button.configure(text="Iniciar Sesión")
            self.toggle_mode.configure(text="¿No tienes cuenta? Regístrate")
            self.remember_checkbox.pack(anchor="w", pady=(0, 20))
        
        self.usuario.delete(0, 'end')
        self.password.delete(0, 'end')
        self.mensaje.configure(text="")

    def crear_base_datos(self):
        """Crea la base de datos SQLite y la tabla de usuarios si no existe"""
        try:
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    username TEXT PRIMARY KEY,
                    password TEXT
                )
            ''')
            
            # Verificar si existe el usuario admin
            cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO usuarios (username, password) VALUES (?, ?)",
                    ('admin', 'admin')
                )
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al crear la base de datos: {str(e)}")

    def verificar_login(self):
        """Verifica las credenciales o registra nuevo usuario"""
        if self.modo_registro:
            self.registrar_usuario()
        else:
            self.iniciar_sesion()

    def iniciar_sesion(self):
        """Inicia sesión con las credenciales proporcionadas"""
        usuario = self.usuario.get().strip()
        password = self.password.get().strip()
        
        if not usuario and not password:
            self.mensaje.configure(
                text="Por favor, ingrese usuario y contraseña",
                foreground=self.tema["error"]
            )
            self.usuario.focus()
            return
        elif not usuario:
            self.mensaje.configure(
                text="Por favor, ingrese el usuario",
                foreground=self.tema["error"]
            )
            self.usuario.focus()
            return
        elif not password:
            self.mensaje.configure(
                text="Por favor, ingrese la contraseña",
                foreground=self.tema["error"]
            )
            self.password.focus()
            return
        
        if len(usuario) < 3:
            self.mensaje.configure(
                text="El usuario debe tener al menos 3 caracteres",
                foreground=self.tema["error"]
            )
            self.usuario.focus()
            return
        
        if len(password) < 4:
            self.mensaje.configure(
                text="La contraseña debe tener al menos 4 caracteres",
                foreground=self.tema["error"]
            )
            self.password.focus()
            return
        
        try:
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM usuarios WHERE username = ?", (usuario,))
            user = cursor.fetchone()
            
            if not user:
                self.mensaje.configure(
                    text="El usuario no existe",
                    foreground=self.tema["error"]
                )
                self.usuario.focus()
                return
            
            cursor.execute(
                "SELECT * FROM usuarios WHERE username = ? AND password = ?",
                (usuario, password)
            )
            
            if cursor.fetchone():
                self.mensaje.configure(
                    text="¡Login exitoso! Redirigiendo...",
                    foreground=self.tema["success"]
                )
                self.usuario.delete(0, 'end')
                self.password.delete(0, 'end')
                self.after(1000, self.mostrar_api_data)
            else:
                self.mensaje.configure(
                    text="Contraseña incorrecta",
                    foreground=self.tema["error"]
                )
                self.password.delete(0, 'end')
                self.password.focus()
                
        except Exception as e:
            self.mensaje.configure(
                text=f"Error al iniciar sesión: {str(e)}",
                foreground=self.tema["error"]
            )
        finally:
            conn.close()

    def registrar_usuario(self):
        """Registra un nuevo usuario"""
        usuario = self.usuario.get().strip()
        password = self.password.get().strip()
        
        if not usuario and not password:
            self.mensaje.configure(
                text="Por favor, complete todos los campos",
                foreground=self.tema["error"]
            )
            self.usuario.focus()
            return
        elif not usuario:
            self.mensaje.configure(
                text="Por favor, ingrese el usuario",
                foreground=self.tema["error"]
            )
            self.usuario.focus()
            return
        elif not password:
            self.mensaje.configure(
                text="Por favor, ingrese la contraseña",
                foreground=self.tema["error"]
            )
            self.password.focus()
            return
        
        if len(usuario) < 3:
            self.mensaje.configure(
                text="El usuario debe tener al menos 3 caracteres",
                foreground=self.tema["error"]
            )
            self.usuario.focus()
            return
        
        if len(password) < 4:
            self.mensaje.configure(
                text="La contraseña debe tener al menos 4 caracteres",
                foreground=self.tema["error"]
            )
            self.password.focus()
            return
        
        try:
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM usuarios WHERE username = ?", (usuario,))
            if cursor.fetchone():
                self.mensaje.configure(
                    text="El usuario ya existe",
                    foreground=self.tema["error"]
                )
                self.usuario.focus()
                return
            
            cursor.execute(
                "INSERT INTO usuarios (username, password) VALUES (?, ?)",
                (usuario, password)
            )
            conn.commit()
            
            self.mensaje.configure(
                text="¡Registro exitoso! Puede iniciar sesión",
                foreground=self.tema["success"]
            )
            self.usuario.delete(0, 'end')
            self.password.delete(0, 'end')
            self.after(1500, self.toggle_modo)
            
        except Exception as e:
            self.mensaje.configure(
                text=f"Error al registrar: {str(e)}",
                foreground=self.tema["error"]
            )
        finally:
            conn.close()

    def mostrar_api_data(self):
        """Muestra los datos de la API en una nueva ventana"""
        # Crear ventana
        self.api_window = tk.Toplevel(self)
        self.api_window.title("Rick and Morty - Personajes")
        self.api_window.geometry("1200x800")
        
        # Frame principal
        main_frame = ttk.Frame(self.api_window, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 30))
        
        title = ttk.Label(
            header_frame,
            text="Personajes de Rick and Morty",
            font=("Segoe UI", 28, "bold"),
            foreground=self.tema["accent"]
        )
        title.pack(side="left")
        
        filters_frame = ttk.Frame(main_frame)
        filters_frame.pack(fill="x", pady=(0, 30))
        
        search_frame = ttk.Frame(filters_frame)
        search_frame.pack(side="left", fill="x", expand=True)
        
        search_label = ttk.Label(
            search_frame,
            text="Buscar:",
            font=("Segoe UI", 14),
            foreground=self.tema["fg"]
        )
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_entry = ttk.Entry(
            search_frame,
            width=30,
            font=("Segoe UI", 14)
        )
        self.search_entry.pack(side="left", padx=(0, 20))
        self.search_entry.bind('<Return>', self.aplicar_filtros)
        
        search_button = ttk.Button(
            search_frame,
            text="Buscar",
            command=self.aplicar_filtros,
            style="TButton"
        )
        search_button.pack(side="left")
        
        filters_label = ttk.Label(
            filters_frame,
            text="Filtros:",
            font=("Segoe UI", 14),
            foreground=self.tema["fg"]
        )
        filters_label.pack(side="left", padx=(20, 10))
        
        status_label = ttk.Label(
            filters_frame,
            text="Estado:",
            font=("Segoe UI", 14),
            foreground=self.tema["fg"]
        )
        status_label.pack(side="left", padx=(0, 10))
        
        self.status_var = tk.StringVar(value="Todos")
        status_menu = ttk.OptionMenu(
            filters_frame,
            self.status_var,
            "Todos",
            "Alive",
            "Dead",
            "unknown",
            command=self.aplicar_filtros
        )
        status_menu.pack(side="left", padx=(0, 20))
        
        species_label = ttk.Label(
            filters_frame,
            text="Especie:",
            font=("Segoe UI", 14),
            foreground=self.tema["fg"]
        )
        species_label.pack(side="left", padx=(0, 10))
        
        self.species_var = tk.StringVar(value="Todas")
        species_menu = ttk.OptionMenu(
            filters_frame,
            self.species_var,
            "Todas",
            "Human",
            "Alien",
            "Humanoid",
            "Animal",
            "Robot",
            "Mythological Creature",
            "Disease",
            "Cronenberg",
            "unknown",
            command=self.aplicar_filtros
        )
        species_menu.pack(side="left")
        
        self.characters_canvas = tk.Canvas(main_frame, background=self.tema["bg"], highlightthickness=0)
        self.characters_canvas.pack(fill="both", expand=True, pady=(0, 20))
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.characters_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar canvas
        self.characters_canvas.configure(yscrollcommand=scrollbar.set)
        self.characters_frame = ttk.Frame(self.characters_canvas)
        self.characters_canvas.create_window((0, 0), window=self.characters_frame, anchor="nw", width=self.characters_canvas.winfo_width())
        
        def _on_mousewheel(event):
            self.characters_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel(event):
            self.characters_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_mousewheel(event):
            self.characters_canvas.unbind_all("<MouseWheel>")
        
        self.characters_canvas.bind('<Enter>', _bind_mousewheel)
        self.characters_canvas.bind('<Leave>', _unbind_mousewheel)
        
        # Configurar scroll
        def configure_scroll(event):
            self.characters_canvas.configure(scrollregion=self.characters_canvas.bbox("all"))
            self.characters_canvas.itemconfig(self.characters_canvas.find_withtag("all")[0], width=event.width)
        
        self.characters_frame.bind("<Configure>", configure_scroll)
        self.characters_canvas.bind("<Configure>", configure_scroll)
        
        pagination_frame = ttk.Frame(main_frame)
        pagination_frame.pack(fill="x", pady=20)
        
        self.prev_button = ttk.Button(
            pagination_frame,
            text="← Anterior",
            command=self.pagina_anterior,
            style="TButton"
        )
        self.prev_button.pack(side="left")
        
        self.page_label = ttk.Label(
            pagination_frame,
            text="Página 1",
            font=("Segoe UI", 14),
            foreground=self.tema["fg"]
        )
        self.page_label.pack(side="left", padx=20)
        
        self.next_button = ttk.Button(
            pagination_frame,
            text="Siguiente →",
            command=self.pagina_siguiente,
            style="TButton"
        )
        self.next_button.pack(side="left")
        
        self.cargar_datos_api()

    def cargar_datos_api(self):
        """Carga los datos de la API usando urllib"""
        try:
            with urlopen("https://rickandmortyapi.com/api/character") as response: #API
                data = json.loads(response.read().decode())
                self.characters_data = data['results']
                self.original_characters_data = data['results']
                self.mostrar_personajes(self.get_pagina_actual())
        except URLError as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def mostrar_personajes(self, personajes):
        """Muestra la lista de personajes"""
        for widget in self.characters_frame.winfo_children():
            widget.destroy()
        
        for character in personajes:
            char_frame = ttk.Frame(
                self.characters_frame,
                style="Card.TFrame"
            )
            char_frame.pack(fill="x", pady=10, padx=10)
            
            name_label = ttk.Label(
                char_frame,
                text=character['name'],
                font=("Segoe UI", 16, "bold"),
                foreground=self.tema["accent"]
            )
            name_label.pack(anchor="w", pady=(15, 10), padx=15)
            
            info_frame = ttk.Frame(char_frame)
            info_frame.pack(fill="x", pady=5, padx=15)
            
            species_label = ttk.Label(
                info_frame,
                text=f"Especie: {character['species']}",
                font=("Segoe UI", 14),
                foreground=self.tema["fg"]
            )
            species_label.pack(anchor="w")
            
            status_label = ttk.Label(
                info_frame,
                text=f"Estado: {character['status']}",
                font=("Segoe UI", 14),
                foreground=self.tema["fg"]
            )
            status_label.pack(anchor="w")
            
            origin_label = ttk.Label(
                info_frame,
                text=f"Origen: {character['origin']['name']}",
                font=("Segoe UI", 14),
                foreground=self.tema["fg"]
            )
            origin_label.pack(anchor="w")
            details_button = ttk.Button(
                char_frame,
                text="Ver más detalles",
                command=lambda c=character: self.mostrar_detalles(c),
                style="TButton"
            )
            details_button.pack(pady=15, padx=15)
            separator = ttk.Separator(self.characters_frame, orient="horizontal")
            separator.pack(fill="x", pady=5)

    def mostrar_detalles(self, character):
        """Muestra un toast con detalles del personaje"""
        toast = tk.Toplevel(self.api_window)
        toast.overrideredirect(True)  # Quitar bordes de ventana
        
        x = self.api_window.winfo_x() + (self.api_window.winfo_width() // 2) - 200
        y = self.api_window.winfo_y() + (self.api_window.winfo_height() // 2) - 250
        toast.geometry(f"400x500+{x}+{y}")
        
        main_frame = ttk.Frame(toast, padding="20", style="Card.TFrame")
        main_frame.pack(fill="both", expand=True)
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = ttk.Label(
            header_frame,
            text=character['name'],
            font=("Segoe UI", 20, "bold"),
            foreground=self.tema["accent"]
        )
        title.pack(side="left")
        
        close_button = ttk.Button(
            header_frame,
            text="×",
            width=3,
            command=toast.destroy,
            style="TButton"
        )
        close_button.pack(side="right")
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.pack(fill="x", pady=10)
        
        details = [
            ("Especie", character['species']),
            ("Estado", character['status']),
            ("Origen", character['origin']['name']),
            ("Ubicación", character['location']['name']),
            ("Género", character['gender']),
            ("Episodios", f"{len(character['episode'])} apariciones")
        ]
        
        for label, value in details:
            frame = ttk.Frame(main_frame)
            frame.pack(fill="x", pady=10)
            
            label_widget = ttk.Label(
                frame,
                text=f"{label}:",
                font=("Segoe UI", 12, "bold"),
                foreground=self.tema["fg"]
            )
            label_widget.pack(side="left", padx=(0, 10))
            
            value_widget = ttk.Label(
                frame,
                text=value,
                font=("Segoe UI", 12),
                foreground=self.tema["fg"]
            )
            value_widget.pack(side="left")
        
        toast.bind('<Escape>', lambda e: toast.destroy())
        
        def on_click_outside(event):
            if event.widget == self.api_window:
                toast.destroy()
        
        self.api_window.bind('<Button-1>', on_click_outside)

    def get_pagina_actual(self):
        """Obtiene los personajes de la página actual"""
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        return self.characters_data[start_idx:end_idx]

    def pagina_anterior(self):
        """Muestra la página anterior"""
        if self.current_page > 1:
            self.current_page -= 1
            self.actualizar_paginacion()

    def pagina_siguiente(self):
        """Muestra la página siguiente"""
        max_pages = len(self.characters_data) // self.items_per_page + 1
        if self.current_page < max_pages:
            self.current_page += 1
            self.actualizar_paginacion()

    def actualizar_paginacion(self):
        """Actualiza la visualización de la paginación"""
        self.page_label.configure(text=f"Página {self.current_page}")
        self.mostrar_personajes(self.get_pagina_actual())

    def aplicar_filtros(self, _=None):
        """Aplica los filtros seleccionados"""
        texto_busqueda = self.search_entry.get().lower()
        status_filter = self.status_var.get()
        species_filter = self.species_var.get()
        

        personajes_filtrados = []
        for char in self.original_characters_data:
            # Verificar búsqueda por texto
            texto_coincide = (
                not texto_busqueda or
                texto_busqueda in char['name'].lower() or
                texto_busqueda in char['species'].lower() or
                texto_busqueda in char['origin']['name'].lower()
            )
            
            # Verificar filtro de estado
            estado_coincide = (
                status_filter == "Todos" or
                char['status'] == status_filter
            )
            
            # Verificar filtro de especie
            especie_coincide = (
                species_filter == "Todas" or
                char['species'] == species_filter
            )
            
            if texto_coincide and estado_coincide and especie_coincide:
                personajes_filtrados.append(char)
        
        self.characters_data = personajes_filtrados
        self.current_page = 1
        self.actualizar_paginacion()
        
        if not personajes_filtrados:
            messagebox.showinfo("Búsqueda", "No se encontraron personajes que coincidan con los filtros")
        else:
            messagebox.showinfo("Búsqueda", f"Se encontraron {len(personajes_filtrados)} personajes")

    def toggle_password_visibility(self):
        """Alterna la visibilidad de la contraseña"""
        if self.password['show'] == '•':
            self.password['show'] = ''
            self.toggle_password_button.configure(text="👁️‍🗨️")
        else:
            self.password['show'] = '•'
            self.toggle_password_button.configure(text="👁️")

if __name__ == "__main__":
    app = App()
    app.mainloop() 