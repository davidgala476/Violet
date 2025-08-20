import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from models import DollModel, ClienteModel, CartaModel
from datetime import datetime

class PostalCHApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compañía Postal CH - Gestión de Auto Memory Dolls")
        self.root.geometry("1200x700")
        
        self.style = ttk.Style()
        self.style.configure('Treeview', rowheight=25)
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=2)
        
        self.create_widgets()
        self.load_initial_data()
        self.setup_bindings()

    def setup_bindings(self):
        self.dolls_tree.bind('<Double-1>', lambda e: self.show_doll_report())
        self.clientes_tree.bind('<Double-1>', lambda e: self.edit_cliente())
        self.cartas_tree.bind('<Double-1>', lambda e: self.view_carta_detail())

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_dashboard_tab()
        self.create_dolls_tab()
        self.create_clientes_tab()
        self.create_cartas_tab()

    def create_dashboard_tab(self):
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        stats_frame = ttk.LabelFrame(dashboard_frame, text="Estadísticas Generales", padding=15)
        stats_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(stats_grid, text="Total Dolls:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=8)
        self.total_dolls_label = ttk.Label(stats_grid, text="0", font=('Arial', 10))
        self.total_dolls_label.grid(row=0, column=1, sticky='w', padx=10, pady=8)
        
        ttk.Label(stats_grid, text="Dolls Activas:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=10, pady=8)
        self.dolls_activas_label = ttk.Label(stats_grid, text="0", font=('Arial', 10))
        self.dolls_activas_label.grid(row=1, column=1, sticky='w', padx=10, pady=8)
        
        ttk.Label(stats_grid, text="Dolls Inactivas:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=10, pady=8)
        self.dolls_inactivas_label = ttk.Label(stats_grid, text="0", font=('Arial', 10))
        self.dolls_inactivas_label.grid(row=2, column=1, sticky='w', padx=10, pady=8)
        
        ttk.Label(stats_grid, text="Total Clientes:", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky='w', padx=10, pady=8)
        self.total_clientes_label = ttk.Label(stats_grid, text="0", font=('Arial', 10))
        self.total_clientes_label.grid(row=0, column=3, sticky='w', padx=10, pady=8)
        
        ttk.Label(stats_grid, text="Total Cartas:", font=('Arial', 10, 'bold')).grid(row=1, column=2, sticky='w', padx=10, pady=8)
        self.total_cartas_label = ttk.Label(stats_grid, text="0", font=('Arial', 10))
        self.total_cartas_label.grid(row=1, column=3, sticky='w', padx=10, pady=8)
        
        ttk.Label(stats_grid, text="Cartas Enviadas:", font=('Arial', 10, 'bold')).grid(row=2, column=2, sticky='w', padx=10, pady=8)
        self.cartas_enviadas_label = ttk.Label(stats_grid, text="0", font=('Arial', 10))
        self.cartas_enviadas_label.grid(row=2, column=3, sticky='w', padx=10, pady=8)
        
        ttk.Label(stats_grid, text="Cartas en Borrador:", font=('Arial', 10, 'bold')).grid(row=0, column=4, sticky='w', padx=10, pady=8)
        self.cartas_borrador_label = ttk.Label(stats_grid, text="0", font=('Arial', 10))
        self.cartas_borrador_label.grid(row=0, column=5, sticky='w', padx=10, pady=8)
        
        ttk.Label(stats_grid, text="Cartas en Revisión:", font=('Arial', 10, 'bold')).grid(row=1, column=4, sticky='w', padx=10, pady=8)
        self.cartas_revision_label = ttk.Label(stats_grid, text="0", font=('Arial', 10))
        self.cartas_revision_label.grid(row=1, column=5, sticky='w', padx=10, pady=8)
        
        ttk.Label(stats_grid, text="Cartas por Enviar:", font=('Arial', 10, 'bold')).grid(row=2, column=4, sticky='w', padx=10, pady=8)
        self.cartas_por_enviar_label = ttk.Label(stats_grid, text="0", font=('Arial', 10))
        self.cartas_por_enviar_label.grid(row=2, column=5, sticky='w', padx=10, pady=8)
        
        button_frame = ttk.Frame(stats_frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text=" Actualizar Estadísticas", 
                  command=self.update_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Reporte Completo", 
                  command=self.show_full_report).pack(side=tk.LEFT, padx=5)

    def create_dolls_tab(self):
        dolls_frame = ttk.Frame(self.notebook)
        self.notebook.add(dolls_frame, text="Auto Memory Dolls")
        
        list_frame = ttk.LabelFrame(dolls_frame, text="Lista de Dolls", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('id', 'nombre', 'edad', 'estado', 'cartas_escritas', 'cartas_en_proceso')
        self.dolls_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        self.dolls_tree.heading('id', text='ID')
        self.dolls_tree.heading('nombre', text='Nombre')
        self.dolls_tree.heading('edad', text='Edad')
        self.dolls_tree.heading('estado', text='Estado')
        self.dolls_tree.heading('cartas_escritas', text=' Escritas')
        self.dolls_tree.heading('cartas_en_proceso', text=' En Proceso')
        
        self.dolls_tree.column('id', width=50)
        self.dolls_tree.column('nombre', width=150)
        self.dolls_tree.column('edad', width=50)
        self.dolls_tree.column('estado', width=80)
        self.dolls_tree.column('cartas_escritas', width=80)
        self.dolls_tree.column('cartas_en_proceso', width=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.dolls_tree.yview)
        self.dolls_tree.configure(yscrollcommand=scrollbar.set)
        
        self.dolls_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        button_frame = ttk.Frame(dolls_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text=" Nueva Doll", command=self.new_doll).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Editar", command=self.edit_doll).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Eliminar", command=self.delete_doll).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Actualizar", command=self.load_dolls).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Ver Reporte", command=self.show_doll_report).pack(side=tk.LEFT, padx=5)

    def create_clientes_tab(self):
        clientes_frame = ttk.Frame(self.notebook)
        self.notebook.add(clientes_frame, text="Clientes")
        
        search_frame = ttk.Frame(clientes_frame)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(search_frame, text=" Buscar por ciudad:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<Return>', lambda e: self.search_clientes())
        
        ttk.Button(search_frame, text="Buscar", command=self.search_clientes).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Mostrar Todos", command=self.load_clientes).pack(side=tk.LEFT, padx=5)
        
        list_frame = ttk.LabelFrame(clientes_frame, text="Lista de Clientes", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('id', 'nombre', 'ciudad', 'motivo_carta', 'contacto')
        self.clientes_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        self.clientes_tree.heading('id', text='ID')
        self.clientes_tree.heading('nombre', text='Nombre')
        self.clientes_tree.heading('ciudad', text='Ciudad')
        self.clientes_tree.heading('motivo_carta', text='Motivo de Carta')
        self.clientes_tree.heading('contacto', text='Contacto')
        
        self.clientes_tree.column('id', width=50)
        self.clientes_tree.column('nombre', width=150)
        self.clientes_tree.column('ciudad', width=100)
        self.clientes_tree.column('motivo_carta', width=150)
        self.clientes_tree.column('contacto', width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.clientes_tree.yview)
        self.clientes_tree.configure(yscrollcommand=scrollbar.set)
        
        self.clientes_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        button_frame = ttk.Frame(clientes_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text=" Nuevo Cliente", command=self.new_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Editar", command=self.edit_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Eliminar", command=self.delete_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Actualizar", command=self.load_clientes).pack(side=tk.LEFT, padx=5)

    def create_cartas_tab(self):
        cartas_frame = ttk.Frame(self.notebook)
        self.notebook.add(cartas_frame, text="Cartas")
        
        filter_frame = ttk.Frame(cartas_frame)
        filter_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(filter_frame, text=" Filtrar por estado:").pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar(value="Todos")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["Todos", "borrador", "revisado", "enviado"], 
                                   state="readonly", width=15)
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.load_cartas())
        
        list_frame = ttk.LabelFrame(cartas_frame, text="Lista de Cartas", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('id', 'cliente', 'doll', 'estado', 'fecha', 'resumen')
        self.cartas_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        self.cartas_tree.heading('id', text='ID')
        self.cartas_tree.heading('cliente', text='Cliente')
        self.cartas_tree.heading('doll', text='Doll Asignada')
        self.cartas_tree.heading('estado', text='Estado')
        self.cartas_tree.heading('fecha', text='Fecha Creación')
        self.cartas_tree.heading('resumen', text='Resumen')
        
        self.cartas_tree.column('id', width=50)
        self.cartas_tree.column('cliente', width=150)
        self.cartas_tree.column('doll', width=150)
        self.cartas_tree.column('estado', width=80)
        self.cartas_tree.column('fecha', width=100)
        self.cartas_tree.column('resumen', width=250)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.cartas_tree.yview)
        self.cartas_tree.configure(yscrollcommand=scrollbar.set)
        
        self.cartas_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        button_frame = ttk.Frame(cartas_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text=" Nueva Carta", command=self.new_carta).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Ver Detalle", command=self.view_carta_detail).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Marcar como Revisado", 
                  command=lambda: self.update_carta_status('revisado')).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Marcar como Enviado", 
                  command=lambda: self.update_carta_status('enviado')).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Eliminar", command=self.delete_carta).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Actualizar", command=self.load_cartas).pack(side=tk.LEFT, padx=5)

    def load_initial_data(self):
        self.load_dolls()
        self.load_clientes()
        self.load_cartas()
        self.update_stats()

    def update_stats(self):
        dolls = DollModel.read_all()
        clientes = ClienteModel.read_all()
        cartas = CartaModel.read_all()
        
        dolls_activas = sum(1 for doll in dolls if doll[3] == 'activo')
        dolls_inactivas = sum(1 for doll in dolls if doll[3] == 'inactivo')
        
        cartas_enviadas = sum(1 for carta in cartas if carta[4] == 'enviado')
        cartas_borrador = sum(1 for carta in cartas if carta[4] == 'borrador')
        cartas_revision = sum(1 for carta in cartas if carta[4] == 'revisado')
        
        self.total_dolls_label.config(text=str(len(dolls)))
        self.dolls_activas_label.config(text=str(dolls_activas))
        self.dolls_inactivas_label.config(text=str(dolls_inactivas))
        self.total_clientes_label.config(text=str(len(clientes)))
        self.total_cartas_label.config(text=str(len(cartas)))
        self.cartas_enviadas_label.config(text=str(cartas_enviadas))
        self.cartas_borrador_label.config(text=str(cartas_borrador))
        self.cartas_revision_label.config(text=str(cartas_revision))
        self.cartas_por_enviar_label.config(text=str(cartas_revision))

    def load_dolls(self):
        for item in self.dolls_tree.get_children():
            self.dolls_tree.delete(item)
        
        dolls = DollModel.read_all()
        for doll in dolls:
            self.dolls_tree.insert('', 'end', values=doll)

    def load_clientes(self):
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        clientes = ClienteModel.read_all()
        for cliente in clientes:
            self.clientes_tree.insert('', 'end', values=cliente)

    def search_clientes(self):
        ciudad = self.search_var.get().strip()
        if not ciudad:
            self.load_clientes()
            return
        
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        clientes = ClienteModel.search_by_city(ciudad)
        for cliente in clientes:
            self.clientes_tree.insert('', 'end', values=cliente)

    def load_cartas(self):
        for item in self.cartas_tree.get_children():
            self.cartas_tree.delete(item)
        
        cartas = CartaModel.read_all()
        estado_filter = self.filter_var.get()
        
        for carta in cartas:
            if estado_filter == "Todos" or carta[4] == estado_filter:
                self.cartas_tree.insert('', 'end', values=(
                    carta[0], carta[7], carta[8], carta[4], carta[3], carta[6]
                ))

    def new_doll(self):
        self.open_doll_dialog()

    def edit_doll(self):
        selected = self.dolls_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una Doll para editar")
            return
        
        doll_id = self.dolls_tree.item(selected[0])['values'][0]
        doll = DollModel.read_by_id(doll_id)
        self.open_doll_dialog(doll)

    def open_doll_dialog(self, doll=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Nueva Doll" if not doll else "Editar Doll")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f'400x300+{x}+{y}')
        
        ttk.Label(dialog, text="Nombre:", font=('Arial', 10, 'bold')).pack(pady=5)
        nombre_var = tk.StringVar(value=doll[1] if doll else "")
        nombre_entry = ttk.Entry(dialog, textvariable=nombre_var, font=('Arial', 10))
        nombre_entry.pack(pady=5, padx=20, fill='x')
        
        ttk.Label(dialog, text="Edad:", font=('Arial', 10, 'bold')).pack(pady=5)
        edad_var = tk.StringVar(value=str(doll[2]) if doll and doll[2] else "")
        edad_entry = ttk.Entry(dialog, textvariable=edad_var, font=('Arial', 10))
        edad_entry.pack(pady=5, padx=20, fill='x')
        
        ttk.Label(dialog, text="Estado:", font=('Arial', 10, 'bold')).pack(pady=5)
        estado_var = tk.StringVar(value=doll[3] if doll else "activo")
        estado_combo = ttk.Combobox(dialog, textvariable=estado_var, 
                                   values=['activo', 'inactivo'], state='readonly', font=('Arial', 10))
        estado_combo.pack(pady=5, padx=20, fill='x')
        
        def save_doll():
            try:
                nombre = nombre_var.get().strip()
                edad = int(edad_var.get()) if edad_var.get().strip() else None
                estado = estado_var.get()
                
                if not nombre or not estado:
                    messagebox.showerror("Error", "Nombre y estado son obligatorios")
                    return
                
                if doll:
                    success = DollModel.update(doll[0], nombre=nombre, edad=edad, estado=estado)
                    if success:
                        messagebox.showinfo("Éxito", "Doll actualizada correctamente")
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar la Doll")
                else:
                    doll_id = DollModel.create(nombre, edad, estado)
                    if doll_id:
                        messagebox.showinfo("Éxito", f"Doll creada con ID: {doll_id}")
                    else:
                        messagebox.showerror("Error", "No se pudo crear la Doll")
                
                self.load_dolls()
                self.update_stats()
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "La edad debe ser un número válido")
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {e}")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Guardar", command=save_doll).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        nombre_entry.focus()

    def delete_doll(self):
        selected = self.dolls_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una Doll para eliminar")
            return
        
        doll_id = self.dolls_tree.item(selected[0])['values'][0]
        doll_nombre = self.dolls_tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Confirmar Eliminación", 
                              f"¿Estás seguro de eliminar a la Doll '{doll_nombre}'?\n\nEsta acción no se puede deshacer."):
            if DollModel.delete(doll_id):
                messagebox.showinfo("Éxito", "Doll eliminada correctamente")
                self.load_dolls()
                self.update_stats()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la Doll")

    def show_doll_report(self):
        selected = self.dolls_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una Doll para ver su reporte")
            return
        
        doll_id = self.dolls_tree.item(selected[0])['values'][0]
        doll = DollModel.read_by_id(doll_id)
        cartas = CartaModel.get_cartas_por_doll(doll_id)
        
        report_dialog = tk.Toplevel(self.root)
        report_dialog.title(f" Reporte de {doll[1]}")
        report_dialog.geometry("600x500")
        
        report_dialog.update_idletasks()
        x = (report_dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (report_dialog.winfo_screenheight() // 2) - (500 // 2)
        report_dialog.geometry(f'600x500+{x}+{y}')
        
        header_frame = ttk.Frame(report_dialog)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(header_frame, text=f"Reporte de Performance", font=('Arial', 14, 'bold')).pack()
        ttk.Label(header_frame, text=f"Doll: {doll[1]}", font=('Arial', 12)).pack()
        
        stats_frame = ttk.LabelFrame(report_dialog, text="Estadísticas", padding=10)
        stats_frame.pack(fill='x', padx=20, pady=5)
        
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(stats_grid, text="Cartas escritas:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(stats_grid, text=str(doll[4]), font=('Arial', 10)).grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(stats_grid, text="Cartas en proceso:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(stats_grid, text=str(doll[5]), font=('Arial', 10)).grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        clientes_unicos = len(set(carta[1] for carta in cartas))
        ttk.Label(stats_grid, text="Clientes únicos:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(stats_grid, text=str(clientes_unicos), font=('Arial', 10)).grid(row=2, column=1, sticky='w', padx=5, pady=2)
        
        eficiencia = doll[4] / clientes_unicos if clientes_unicos > 0 else 0
        ttk.Label(stats_grid, text="Eficiencia:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(stats_grid, text=f"{eficiencia:.2f} cartas/cliente", font=('Arial', 10)).grid(row=3, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(report_dialog, text=" Cartas Recientes:", font=('Arial', 11, 'bold')).pack(anchor='w', padx=20, pady=(10, 5))
        
        list_frame = ttk.Frame(report_dialog)
        list_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        tree = ttk.Treeview(list_frame, columns=('id', 'cliente', 'estado', 'fecha'), show='headings', height=8)
        tree.heading('id', text='ID')
        tree.heading('cliente', text='Cliente')
        tree.heading('estado', text='Estado')
        tree.heading('fecha', text='Fecha')
        
        tree.column('id', width=50)
        tree.column('cliente', width=150)
        tree.column('estado', width=80)
        tree.column('fecha', width=100)
        
        for carta in cartas[-10:]:
            tree.insert('', 'end', values=(carta[0], carta[7], carta[4], carta[3]))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')

    def show_full_report(self):
        dolls = DollModel.read_all()
        clientes = ClienteModel.read_all()
        cartas = CartaModel.read_all()
        
        report_dialog = tk.Toplevel(self.root)
        report_dialog.title(" Reporte Completo - Compañía Postal CH")
        report_dialog.geometry("700x600")
        
        report_dialog.update_idletasks()
        x = (report_dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (report_dialog.winfo_screenheight() // 2) - (600 // 2)
        report_dialog.geometry(f'700x600+{x}+{y}')
        
        ttk.Label(report_dialog, text="REPORTE COMPLETO", font=('Arial', 16, 'bold')).pack(pady=10)
        ttk.Label(report_dialog, text="Compañía Postal CH", font=('Arial', 12)).pack()
        ttk.Label(report_dialog, text=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}", font=('Arial', 10)).pack(pady=5)
        
        notebook = ttk.Notebook(report_dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="Resumen General")
        
        summary_text = scrolledtext.ScrolledText(summary_frame, wrap=tk.WORD, font=('Arial', 10))
        summary_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        summary_content = f"""
        RESUMEN GENERAL - COMPAÑÍA POSTAL CH
        
        DOLLS:
        • Total Dolls: {len(dolls)}
        • Dolls Activas: {sum(1 for d in dolls if d[3] == 'activo')}
        • Dolls Inactivas: {sum(1 for d in dolls if d[3] == 'inactivo')}
        • Total cartas escritas: {sum(d[4] for d in dolls)}
        
        Clientes:
        • Total clientes: {len(clientes)}
        • Ciudades únicas: {len(set(c[2] for c in clientes if c[2]))}
        
        Cartas:
        • Total cartas: {len(cartas)}
        • En borrador: {sum(1 for c in cartas if c[4] == 'borrador')}
        • En revisión: {sum(1 for c in cartas if c[4] == 'revisado')}
        • Enviadas: {sum(1 for c in cartas if c[4] == 'enviado')}
        • Tasa de envío: {(sum(1 for c in cartas if c[4] == 'enviado') / len(cartas) * 100 if len(cartas) > 0 else 0):.1f}%
        
         DOLL MÁS PRODUCTIVA:
        """
        
        if dolls:
            top_doll = max(dolls, key=lambda x: x[4])
            summary_content += f"{top_doll[1]} - {top_doll[4]} cartas escritas"
        
        summary_text.insert('1.0', summary_content)
        summary_text.config(state='disabled')
        
        top_frame = ttk.Frame(notebook)
        notebook.add(top_frame, text="Top Dolls")
        
        columns = ('nombre', 'cartas_escritas', 'cartas_proceso', 'eficiencia')
        top_tree = ttk.Treeview(top_frame, columns=columns, show='headings')
        
        top_tree.heading('nombre', text='Doll')
        top_tree.heading('cartas_escritas', text='Cartas Escritas')
        top_tree.heading('cartas_proceso', text='En Proceso')
        top_tree.heading('eficiencia', text='Eficiencia')
        
        top_tree.column('nombre', width=150)
        top_tree.column('cartas_escritas', width=100)
        top_tree.column('cartas_proceso', width=100)
        top_tree.column('eficiencia', width=100)
        
        sorted_dolls = sorted(dolls, key=lambda x: x[4], reverse=True)
        for doll in sorted_dolls:
            cartas_doll = CartaModel.get_cartas_por_doll(doll[0])
            clientes_unicos = len(set(c[1] for c in cartas_doll))
            eficiencia = doll[4] / clientes_unicos if clientes_unicos > 0 else 0
            
            top_tree.insert('', 'end', values=(
                doll[1], doll[4], doll[5], f"{eficiencia:.2f}"
            ))
        
        scrollbar = ttk.Scrollbar(top_frame, orient=tk.VERTICAL, command=top_tree.yview)
        top_tree.configure(yscrollcommand=scrollbar.set)
        
        top_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')

    def new_cliente(self):
        self.open_cliente_dialog()

    def edit_cliente(self):
        selected = self.clientes_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un Cliente para editar")
            return
        
        cliente_id = self.clientes_tree.item(selected[0])['values'][0]
        cliente = ClienteModel.read_by_id(cliente_id)
        self.open_cliente_dialog(cliente)

    def open_cliente_dialog(self, cliente=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuevo Cliente" if not cliente else "Editar Cliente")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f'400x300+{x}+{y}')
        
        ttk.Label(dialog, text="Nombre:*", font=('Arial', 10, 'bold')).pack(pady=5)
        nombre_var = tk.String
        ttk.Label(dialog, text="Nombre:*", font=('Arial', 10, 'bold')).pack(pady=5)
        nombre_var = tk.StringVar(value=cliente[1] if cliente else "")
        nombre_entry = ttk.Entry(dialog, textvariable=nombre_var, font=('Arial', 10))
        nombre_entry.pack(pady=5, padx=20, fill='x')
        
        ttk.Label(dialog, text="Ciudad:", font=('Arial', 10, 'bold')).pack(pady=5)
        ciudad_var = tk.StringVar(value=cliente[2] if cliente else "")
        ciudad_entry = ttk.Entry(dialog, textvariable=ciudad_var, font=('Arial', 10))
        ciudad_entry.pack(pady=5, padx=20, fill='x')
        
        ttk.Label(dialog, text="Motivo de la carta:", font=('Arial', 10, 'bold')).pack(pady=5)
        motivo_var = tk.StringVar(value=cliente[3] if cliente else "")
        motivo_entry = ttk.Entry(dialog, textvariable=motivo_var, font=('Arial', 10))
        motivo_entry.pack(pady=5, padx=20, fill='x')
        
        ttk.Label(dialog, text="Contacto:", font=('Arial', 10, 'bold')).pack(pady=5)
        contacto_var = tk.StringVar(value=cliente[4] if cliente else "")
        contacto_entry = ttk.Entry(dialog, textvariable=contacto_var, font=('Arial', 10))
        contacto_entry.pack(pady=5, padx=20, fill='x')
        
        def save_cliente():
            try:
                nombre = nombre_var.get().strip()
                ciudad = ciudad_var.get().strip()
                motivo = motivo_var.get().strip()
                contacto = contacto_var.get().strip()
                
                if not nombre:
                    messagebox.showerror("Error", "El nombre es obligatorio")
                    return
                
                if cliente:
                    success = ClienteModel.update(cliente[0], 
                                                nombre=nombre, 
                                                ciudad=ciudad, 
                                                motivo_carta=motivo, 
                                                contacto=contacto)
                    if success:
                        messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar el cliente")
                else:
                    cliente_id = ClienteModel.create(nombre, ciudad, motivo, contacto)
                    if cliente_id:
                        messagebox.showinfo("Éxito", f"Cliente creado con ID: {cliente_id}")
                    else:
                        messagebox.showerror("Error", "No se pudo crear el cliente")
                
                self.load_clientes()
                self.update_stats()
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {e}")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Guardar", command=save_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        nombre_entry.focus()

    def delete_cliente(self):
        selected = self.clientes_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un Cliente para eliminar")
            return
        
        cliente_id = self.clientes_tree.item(selected[0])['values'][0]
        cliente_nombre = self.clientes_tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Confirmar Eliminación", 
                              f"¿Estás seguro de eliminar al cliente '{cliente_nombre}'?\n\nEsta acción no se puede deshacer."):
            if ClienteModel.delete(cliente_id):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.load_clientes()
                self.update_stats()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente")

    def new_carta(self):
        self.open_carta_dialog()

    def open_carta_dialog(self, carta=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Nueva Carta")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f'600x500+{x}+{y}')
        
        ttk.Label(dialog, text="Cliente:*", font=('Arial', 10, 'bold')).pack(pady=5)
        clientes = ClienteModel.read_all()
        cliente_var = tk.StringVar()
        cliente_combo = ttk.Combobox(dialog, textvariable=cliente_var, state='readonly', font=('Arial', 10))
        cliente_combo['values'] = [f"{c[0]} - {c[1]} ({c[2]})" for c in clientes]
        cliente_combo.pack(pady=5, padx=20, fill='x')
        
        ttk.Label(dialog, text="Doll asignada:*", font=('Arial', 10, 'bold')).pack(pady=5)
        doll_label = ttk.Label(dialog, text="(Presiona 'Asignar Doll' para asignar automáticamente)", 
                              font=('Arial', 9), foreground='gray')
        doll_label.pack(pady=5)
        
        def assign_doll():
            available_dolls = DollModel.get_available()
            if available_dolls:
                doll = available_dolls[0]
                doll_label.config(text=f"{doll[0]} - {doll[1]} (Cartas en proceso: {doll[5]})", 
                                 foreground='black')
            else:
                messagebox.showerror("Error", "No hay Dolls disponibles en este momento")
                doll_label.config(text="No hay Dolls disponibles", foreground='red')
        
        ttk.Button(dialog, text="🔍 Asignar Doll Automática", command=assign_doll).pack(pady=5)
        
        ttk.Label(dialog, text="Contenido:*", font=('Arial', 10, 'bold')).pack(pady=5)
        contenido_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=50, height=10, font=('Arial', 10))
        contenido_text.pack(pady=5, padx=20, fill='both', expand=True)
        
        ttk.Label(dialog, text="Resumen:*", font=('Arial', 10, 'bold')).pack(pady=5)
        resumen_var = tk.StringVar()
        resumen_entry = ttk.Entry(dialog, textvariable=resumen_var, font=('Arial', 10))
        resumen_entry.pack(pady=5, padx=20, fill='x')
        
        def save_carta():
            try:
                if not cliente_var.get():
                    messagebox.showerror("Error", "Debes seleccionar un cliente")
                    return
                
                cliente_id = int(cliente_var.get().split(' - ')[0])
                doll_text = doll_label.cget("text")
                
                if doll_text.startswith("(Presiona") or doll_text.startswith("❌"):
                    messagebox.showerror("Error", "Debes asignar una Doll primero")
                    return
                
                doll_id = int(doll_text.split(' - ')[0])
                contenido = contenido_text.get("1.0", tk.END).strip()
                resumen = resumen_var.get().strip()
                
                if not contenido:
                    messagebox.showerror("Error", "El contenido de la carta es obligatorio")
                    return
                
                if not resumen:
                    messagebox.showerror("Error", "El resumen es obligatorio")
                    return
                
                carta_id = CartaModel.create(cliente_id, doll_id, contenido, resumen)
                if carta_id:
                    messagebox.showinfo("Éxito", f"Carta creada con ID: {carta_id}")
                    self.load_cartas()
                    self.load_dolls()
                    self.update_stats()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo crear la carta")
                
            except ValueError as e:
                messagebox.showerror("Error", f"Error en los datos: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {e}")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Guardar", command=save_carta).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def update_carta_status(self, new_status):
        selected = self.cartas_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una Carta")
            return
        
        carta_id = self.cartas_tree.item(selected[0])['values'][0]
        estado_actual = self.cartas_tree.item(selected[0])['values'][3]
        carta_resumen = self.cartas_tree.item(selected[0])['values'][5]
        
        try:
            if CartaModel.update_status(carta_id, new_status):
                messagebox.showinfo("Éxito", f"Carta '{carta_resumen}' marcada como {new_status}")
                self.load_cartas()
                self.load_dolls()
                self.update_stats()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el estado de la carta")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def delete_carta(self):
        selected = self.cartas_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una Carta para eliminar")
            return
        
        carta_id = self.cartas_tree.item(selected[0])['values'][0]
        carta_resumen = self.cartas_tree.item(selected[0])['values'][5]
        estado_actual = self.cartas_tree.item(selected[0])['values'][3]
        
        if estado_actual != 'borrador':
            messagebox.showerror("Error", f"Solo se pueden eliminar cartas en estado 'borrador'. Estado actual: {estado_actual}")
            return
        
        if messagebox.askyesno("Confirmar Eliminación", 
                              f"¿Estás seguro de eliminar la carta '{carta_resumen}'?\n\nEsta acción no se puede deshacer."):
            if CartaModel.delete(carta_id):
                messagebox.showinfo("Éxito", "Carta eliminada correctamente")
                self.load_cartas()
                self.load_dolls()
                self.update_stats()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la carta")

    def view_carta_detail(self):
        selected = self.cartas_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una Carta para ver detalles")
            return
        
        carta_id = self.cartas_tree.item(selected[0])['values'][0]
        carta = CartaModel.read_by_id(carta_id)
        
        if not carta:
            messagebox.showerror("Error", "No se pudo cargar la información de la carta")
            return
        
        detail_dialog = tk.Toplevel(self.root)
        detail_dialog.title(f"Detalles de Carta #{carta_id}")
        detail_dialog.geometry("600x500")
        
        detail_dialog.update_idletasks()
        x = (detail_dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (detail_dialog.winfo_screenheight() // 2) - (500 // 2)
        detail_dialog.geometry(f'600x500+{x}+{y}')
        
        info_frame = ttk.LabelFrame(detail_dialog, text="Información de la Carta", padding=10)
        info_frame.pack(fill='x', padx=10, pady=10)
        
        info_grid = ttk.Frame(info_frame)
        info_grid.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(info_grid, text="ID:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(info_grid, text=str(carta[0]), font=('Arial', 10)).grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(info_grid, text="Cliente:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(info_grid, text=carta[7], font=('Arial', 10)).grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(info_grid, text="Doll:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(info_grid, text=carta[8], font=('Arial', 10)).grid(row=2, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(info_grid, text="Estado:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', padx=5, pady=2)
        estado_label = ttk.Label(info_grid, text=carta[4], font=('Arial', 10))
        estado_label.grid(row=3, column=1, sticky='w', padx=5, pady=2)
        
        if carta[4] == 'enviado':
            estado_label.config(foreground='green')
        elif carta[4] == 'revisado':
            estado_label.config(foreground='blue')
        else:
            estado_label.config(foreground='orange')
        
        ttk.Label(info_grid, text="Fecha:", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(info_grid, text=carta[3], font=('Arial', 10)).grid(row=4, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(info_grid, text="Resumen:", font=('Arial', 10, 'bold')).grid(row=5, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(info_grid, text=carta[6], font=('Arial', 10), wraplength=400).grid(row=5, column=1, sticky='w', padx=5, pady=2)
        
        content_frame = ttk.LabelFrame(detail_dialog, text="Contenido Completo", padding=10)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        content_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, font=('Arial', 10))
        content_text.pack(fill='both', expand=True, padx=5, pady=5)
        content_text.insert('1.0', carta[5])
        content_text.config(state='disabled')

def main():
    try:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1200, 700))
        display.start()
        print("Display virtual iniciado - Ejecutando en modo headless")
        use_virtual_display = True
    except ImportError:
        print("pyvirtualdisplay no disponible - Ejecutando con display normal")
        use_virtual_display = False
    except Exception as e:
        print(f"Error con display virtual: {e} - Ejecutando con display normal")
        use_virtual_display = False
    
    try:
        root = tk.Tk()
        app = PostalCHApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error inesperado: {e}")
        messagebox.showerror("Error", f"Error inesperado: {e}")
    finally:
        if use_virtual_display:
            display.stop()

if __name__ == '__main__':
    main()
