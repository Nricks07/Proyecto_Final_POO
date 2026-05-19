from Backend import Piezas_Consola
from Backend import *
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

# --- CONFIGURACIÓN ESTÉTICA GLOBAL ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- INSTANCIACIÓN DE SERVICES DEL BACKEND ---
# Se inicializan los controladores que sirven de puente con las tablas de Supabase
sist_admin = Administrador()
sist_stock = Stock()
sist_solicitud = Solicitudes()
sist_usuario = Persona()
sist_consolas = Piezas_Consola()
sist_celulares = Piezas_Celular()
sist_laptops = Piezas_Laptop()
sist_controles = controles()

def aplicar_estilo_tabla(ventana):
    """ Injecta estilos personalizados sobre el widget nativo Treeview de Tkinter """
    style = ttk.Style(ventana)
    style.theme_use("default")
    
    # Configuración del cuerpo de las tablas (Filas)
    style.configure("Treeview", 
                    background="#1E1E24", 
                    foreground="#ECEFF1", 
                    rowheight=28, 
                    fieldbackground="#1E1E24",
                    font=("Segoe UI", 10))
    # Color de realce al seleccionar un registro
    style.map('Treeview', background=[('selected', '#1F618D')], foreground=[('selected', '#FFFFFF')])
    
    # Configuración visual de las cabeceras de columnas
    style.configure("Treeview.Heading", 
                    background="#2C3E50", 
                    foreground="#A6ACAF", 
                    font=("Segoe UI", 11, "bold"),
                    relief="flat")
    style.map("Treeview.Heading", background=[('active', '#34495E')])

def ventana_login(sist_usuario):
    ventana_login = ctk.CTk()
    ventana_login.title("TechFix - Inicio de Sesión")
    ventana_login.geometry("400x350")

    titulo = ctk.CTkLabel(ventana_login, text="INICIAR SESIÓN", font=("Segoe UI", 18, "bold"), text_color="#1ABC9C")
    titulo.pack(pady=20)

    correo = ctk.CTkLabel(ventana_login, text="Correo Electrónico:", font=("Segoe UI", 12))
    correo.pack(pady=5)
    entrada_correo = ctk.CTkEntry(ventana_login, placeholder_text="ejemplo@correo.com", width=250)
    entrada_correo.pack(pady=5)

    contra = ctk.CTkLabel(ventana_login, text="Contraseña:", font=("Segoe UI", 12))
    contra.pack(pady=5)
    entrada_contra = ctk.CTkEntry(ventana_login, placeholder_text="••••••••", show="*", width=250)
    entrada_contra.pack(pady=5)

    btn_login = ctk.CTkButton(ventana_login, text="Ingresar al Sistema", fg_color="#1ABC9C", hover_color="#16A085",
                              command=lambda: [sist_usuario.login(entrada_correo.get(), entrada_contra.get()), ventana_login.destroy(), ventana_administrador(sist_admin)])
    btn_login.pack(pady=25)
    
    ventana_login.mainloop()

def ventana_administrador(sist_admin):
    root_admin = ctk.CTk()
    root_admin.title("TechFix Panel - Administrador")
    root_admin.geometry("450x500")

    titulo = ctk.CTkLabel(root_admin, text="PANEL DE CONTROL GENERAL", font=("Segoe UI", 16, "bold"), text_color="#3498DB")
    titulo.pack(pady=20)

    frame_menu = ctk.CTkFrame(root_admin, fg_color="transparent")
    frame_menu.pack(fill="both", expand=True, padx=40)

    btn_gest_soli = ctk.CTkButton(frame_menu, text="📋 Gestión de Solicitudes", fg_color="#2980B9", hover_color="#2471A3", command=lambda: ventana_solicitudes(sist_admin))
    btn_gest_soli.pack(fill="x", pady=8)

    btn_gest_stock = ctk.CTkButton(frame_menu, text="📦 Inventario y Repuestos (Stock)", fg_color="#27AE60", hover_color="#1E8449", command=ventana_stock)
    btn_gest_stock.pack(fill="x", pady=8)

    btn_gest_clientes = ctk.CTkButton(frame_menu, text="👥 Directorio de Clientes", fg_color="#8E44AD", hover_color="#7D3C98", command=lambda: ventana_gest_clientes(sist_admin))
    btn_gest_clientes.pack(fill="x", pady=8)

    btn_ingresos = ctk.CTkButton(frame_menu, text="💰 Reporte de Ingresos", fg_color="#D4AC0D", hover_color="#B7950B", text_color="#1A252C", command=lambda: ventana_ingresos(sist_admin))
    btn_ingresos.pack(fill="x", pady=8)

    btn_gastos = ctk.CTkButton(frame_menu, text="📉 Reporte de Gastos", fg_color="#E67E22", hover_color="#D35400", command=lambda: ventana_gastos(sist_admin))
    btn_gastos.pack(fill="x", pady=8)

    btn_contactar_distribuidores = ctk.CTkButton(frame_menu, text="🚛 Contactar Distribuidores", fg_color="#16A085", hover_color="#117A65", command=lambda: ventana_distribuidores(sist_admin))
    btn_contactar_distribuidores.pack(fill="x", pady=8)

    btn_salir = ctk.CTkButton(root_admin, text="Cerrar Sistema", fg_color="#C0392B", hover_color="#922B21", command=root_admin.destroy)
    btn_salir.pack(pady=25)
    
    root_admin.mainloop()

def ventana_solicitudes(sist_admin):
    """ Ventana de control de órdenes. Implementa CTkToplevel para no romper el mainloop """
    ventana_soli = ctk.CTkToplevel()
    ventana_soli.title("Módulo - Gestión de Solicitudes de Servicio")
    ventana_soli.geometry("1000x500")
    ventana_soli.grab_set() # Bloquea la interacción con la ventana padre

    try:
        respuesta = sist_admin.gest_soli()
        datos = respuesta.data
    except Exception as e:
        messagebox.showerror("Error de Conexión", f"No se pudieron sincronizar las solicitudes: {e}")
        return

    aplicar_estilo_tabla(ventana_soli)

    # CONSTRUCCIÓN DINÁMICA DE LA TABLA (TREEVIEW)
    columnas = ("id", "id_cliente", "tipo", "categoria", "descripcion", "estado", "costo", "fecha_recibo")
    tabla = ttk.Treeview(ventana_soli, columns=columnas, show="headings")
    
    headers = ["ID Ticket", "ID Cliente", "Tipo Servicio", "Categoría", "Descripción de Falla", "Estado", "Costo", "Fecha Recibo"]
    widths = [70, 80, 110, 110, 250, 100, 80, 120]
    
    for col, h, w in zip(columnas, headers, widths):
        tabla.heading(col, text=h)
        tabla.column(col, width=w, anchor="center" if col != "descripcion" else "w")

    scrollbar = ttk.Scrollbar(ventana_soli, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True, padx=20, pady=20)

    # Inyección de los datos del Backend en las filas de la tabla
    if datos:
        for fila in datos:
            tabla.insert("", "end", values=(fila.get("id", ""), fila.get("id_cliente", ""), fila.get("tipo", ""), fila.get("categoria", ""), fila.get("descripcion", ""), fila.get("estado", ""), f"${fila.get('costo', 0)}", fila.get("fecha_recibo", "")))

    def actualizar_estado_logica():
        """ Obtiene el registro seleccionado del UI, lo actualiza en DB y refresca la tabla en caliente """
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una fila para modificar el estado.")
            return
        nuevo_estado = menu_estado.get()
        item_id = seleccion[0]
        valores_actuales = list(tabla.item(item_id, "values"))
        
        # Petición remota al Backend
        sist_admin.cambiar_estado_soli(valores_actuales[0], nuevo_estado)
        
        # Sincronización visual inmediata (Evita recargar toda la ventana)
        valores_actuales[5] = nuevo_estado
        tabla.item(item_id, values=valores_actuales)
        messagebox.showinfo("Éxito", f"El pedido {valores_actuales[0]} cambió a: {nuevo_estado}")

    def eliminar_pedido_logica():
        """ Eliminación física/lógica en BD y remoción de fila en Treeview """
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un registro para eliminar.")
            return
        item_id = seleccion[0]
        id_db = tabla.item(item_id, "values")[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente el ticket ID {id_db}?"):
            sist_solicitud.eliminar_soli(id_db)
            tabla.delete(item_id) 

    frame_controles = ctk.CTkFrame(ventana_soli, fg_color="#2C3E50")
    frame_controles.pack(pady=10, padx=20, fill="x")

    label = ctk.CTkLabel(frame_controles, text="Modificar Estado:", font=("Segoe UI", 11, "bold"))
    label.pack(side="left", padx=15, pady=10)

    menu_estado = ctk.CTkOptionMenu(frame_controles, values=["En progreso", "Listo", "Cancelado"], button_color="#2980B9")
    menu_estado.pack(side="left", padx=10)

    btn_actualizar = ctk.CTkButton(frame_controles, text="Actualizar Estado", fg_color="#27AE60", hover_color="#2196F3", command=actualizar_estado_logica)
    btn_actualizar.pack(side="left", padx=10)

    btn_eliminar = ctk.CTkButton(frame_controles, text="Eliminar Ticket", fg_color="#C0392B", hover_color="#A93226", command=eliminar_pedido_logica)
    btn_eliminar.pack(side="right", padx=15)

    btn_salir = ctk.CTkButton(ventana_soli, text="Regresar al Panel", fg_color="#7F8C8D", command=ventana_soli.destroy)
    btn_salir.pack(pady=15)

def ventana_gest_clientes(sist_admin):
    ventana_cli = ctk.CTkToplevel()
    ventana_cli.title("Módulo - Directorio de Clientes")
    ventana_cli.geometry("700x450")
    ventana_cli.grab_set()

    try:
        respuesta = sist_admin.gest_clientes()
        datos = respuesta.data
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo consultar clientes: {e}")
        return

    aplicar_estilo_tabla(ventana_cli)
    columnas = ("id", "nombre", "email", "celular")
    tabla = ttk.Treeview(ventana_cli, columns=columnas, show="headings")
    
    headers = ["ID Cliente", "Nombre Completo", "Correo Electrónico", "Teléfono Celular"]
    widths = [100, 200, 220, 140]
    for col, h, w in zip(columnas, headers, widths):
        tabla.heading(col, text=h)
        tabla.column(col, width=w, anchor="center" if col != "nombre" else "w")

    tabla.pack(fill="both", expand=True, padx=20, pady=20)

    # Conversión de Supabase a celdas legibles del Treeview
    if datos:
        for f in datos:
            tabla.insert("", "end", values=(f.get("id", ""), f.get("Nombre", ""), f.get("Email", ""), f.get("Celular", "")))

    frame_btn = ctk.CTkFrame(ventana_cli, fg_color="transparent")
    frame_btn.pack(pady=10)
    ctk.CTkButton(frame_btn, text="➕ Registrar", fg_color="#27AE60").pack(side="left", padx=5)
    ctk.CTkButton(frame_btn, text="✏️ Modificar", fg_color="#E67E22").pack(side="left", padx=5)
    ctk.CTkButton(frame_btn, text="🗑️ Dar de Baja", fg_color="#C0392B").pack(side="left", padx=5)

    ctk.CTkButton(ventana_cli, text="Regresar", fg_color="#7F8C8D", command=ventana_cli.destroy).pack(pady=10)

def ventana_ingresos(sist_admin):
    ventana_ing = ctk.CTkToplevel()
    ventana_ing.title("Contabilidad - Historial de Ingresos")
    ventana_ing.geometry("600x400")
    ventana_ing.grab_set()

    try:
        datos = sist_admin.ingresos().data
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar finanzas: {e}")
        return

    aplicar_estilo_tabla(ventana_ing)
    columnas = ("Id", "Descripción", "Monto", "Fecha")
    tabla = ttk.Treeview(ventana_ing, columns=columnas, show="headings")
    
    for col, h in zip(columnas, ["ID", "Concepto de Ingreso", "Monto Neto", "Fecha Registro"]):
        tabla.heading(col, text=h)
        tabla.column(col, width=120, anchor="center" if col != "Descripción" else "w")

    tabla.pack(fill="both", expand=True, padx=20, pady=20)
    
    if datos:
        for f in datos:
            tabla.insert("", "end", values=(f.get("id", ""), f.get("descripcion", ""), f"${f.get('monto', 0)}", f.get("fecha", "")))

    ctk.CTkButton(ventana_ing, text="Cerrar Reporte", fg_color="#7F8C8D", command=ventana_ing.destroy).pack(pady=15)

def ventana_gastos(sist_admin):
    ventana_gas = ctk.CTkToplevel()
    ventana_gas.title("Contabilidad - Historial de Egresos")
    ventana_gas.geometry("600x400")
    ventana_gas.grab_set()

    try:
        datos = sist_admin.gastos().data
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar egresos: {e}")
        return

    aplicar_estilo_tabla(ventana_gas)
    columnas = ("Id", "Descripción", "Monto", "Fecha")
    tabla = ttk.Treeview(ventana_gas, columns=columnas, show="headings")
    
    for col, h in zip(columnas, ["ID Operación", "Descripción del Gasto", "Monto Pagado", "Fecha"]):
        tabla.heading(col, text=h)
        tabla.column(col, width=120, anchor="center" if col != "Descripción" else "w")

    tabla.pack(fill="both", expand=True, padx=20, pady=20)
    
    if datos:
        for f in datos:
            tabla.insert("", "end", values=(f.get("id", ""), f.get("descripcion", ""), f"${f.get('monto', 0)}", f.get("fecha", "")))

    ctk.CTkButton(ventana_gas, text="Cerrar Reporte", fg_color="#7F8C8D", command=ventana_gas.destroy).pack(pady=15)

def ventana_distribuidores(sist_admin):
    ventana_dist = ctk.CTkToplevel()
    ventana_dist.title("Directorio - Proveedores Oficiales")
    ventana_dist.geometry("650x400")
    ventana_dist.grab_set()
    
    try:
        datos = sist_admin.contactar_distribuidores().data
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar proveedores: {e}")
        return

    aplicar_estilo_tabla(ventana_dist)
    columnas = ("Id", "Nombre", "Email", "Celular")
    tabla = ttk.Treeview(ventana_dist, columns=columnas, show="headings")
    
    for col, h in zip(columnas, ["ID Prov", "Razón Social / Distribuidor", "Email de Contacto", "Teléfono"]):
        tabla.heading(col, text=h)
        tabla.column(col, width=130, anchor="center" if col != "Nombre" else "w")

    tabla.pack(fill="both", expand=True, padx=20, pady=20)
    
    if datos:
        for f in datos:
            tabla.insert("", "end", values=(f.get("id", ""), f.get("nombre", ""), f.get("email", ""), f.get("celular", "")))

    ctk.CTkButton(ventana_dist, text="Regresar", fg_color="#7F8C8D", command=ventana_dist.destroy).pack(pady=15)

def ventana_stock():
    """ Menú principal para el inventario"""
    v_stock = ctk.CTkToplevel()
    v_stock.title("Inventario Central")
    v_stock.geometry("300x380")
    v_stock.grab_set()

    label = ctk.CTkLabel(v_stock, text="SELECCIONE CATEGORÍA", font=("Segoe UI", 13, "bold"), text_color="#27AE60")
    label.pack(pady=15)

    ctk.CTkButton(v_stock, text="🎮 Consolas", fg_color="#2E4053", command=ventana_consolas).pack(pady=6, fill="x", padx=30)
    ctk.CTkButton(v_stock, text="📱 Celulares", fg_color="#2E4053", command=ventana_celulares).pack(pady=6, fill="x", padx=30)
    ctk.CTkButton(v_stock, text="💻 Laptops", fg_color="#2E4053", command=ventana_laptops).pack(pady=6, fill="x", padx=30)
    ctk.CTkButton(v_stock, text="🕹️ Controles", fg_color="#2E4053", command=ventana_controles).pack(pady=6, fill="x", padx=30)

    ctk.CTkButton(v_stock, text="Regresar Menu", fg_color="#7F8C8D", command=v_stock.destroy).pack(pady=25)

def ventana_consolas():
    v_cons = ctk.CTkToplevel()
    v_cons.title("Inventario - Repuestos y Servicios de Consolas")
    v_cons.geometry("950x450")
    v_cons.grab_set()

    try:
        datos = sist_consolas.mostrar_consola().data
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer tabla Consola: {e}")
        return

    aplicar_estilo_tabla(v_cons)
    columnas = ("id", "marca", "modelo", "m_sencillo", "m_estandar", "m_completo", "r_ruido", "r_video", "r_prende")
    tabla = ttk.Treeview(v_cons, columns=columnas, show="headings")
    
    headers = ["ID", "Marca", "Modelo", "Mante Sencillo", "Mante Estándar", "Mante Completo", "Rep. Ruido", "Rep. Video", "Rep. Prende"]
    for col, h in zip(columnas, headers):
        tabla.heading(col, text=h)
        tabla.column(col, width=95, anchor="center" if col not in ["marca", "modelo"] else "w")

    tabla.pack(fill="both", expand=True, padx=15, pady=15)

    if datos:
        for f in datos:
            tabla.insert("", "end", values=(f.get("id", ""), f.get("Marca", ""), f.get("Modelo", ""), f"${f.get('Mantenimiento Sencillo', 0)}", f"${f.get('Mantenimiento Estandar', 0)}", f"${f.get('Mantenimiento Completo', 0)}", f"${f.get('Reparación Ruido', 0)}", f"${f.get('Reparación No Da Video', 0)}", f"${f.get('Reparación No Prende', 0)}"))

    frame_ops = ctk.CTkFrame(v_cons, fg_color="transparent")
    frame_ops.pack(pady=10)
    ctk.CTkButton(frame_ops, text="➕ Agregar Modelo", fg_color="#27AE60").pack(side="left", padx=6)
    ctk.CTkButton(frame_ops, text="✏️ Modificar Precios", fg_color="#E67E22").pack(side="left", padx=6)
    ctk.CTkButton(frame_ops, text="🗑️ Eliminar Producto", fg_color="#C0392B").pack(side="left", padx=6)

    ctk.CTkButton(v_cons, text="Regresar al Stock", fg_color="#7F8C8D", command=v_cons.destroy).pack(pady=10)

def ventana_celulares():
    v_cel = ctk.CTkToplevel()
    v_cel.title("Inventario - Piezas y Refacciones de Celulares")
    v_cel.geometry("1000x450")
    v_cel.grab_set()

    try:
        datos = sist_celulares.mostrar_celular().data
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer catálogo Celular: {e}")
        return

    aplicar_estilo_tabla(v_cel)
    
    columnas = ("id", "marca", "modelo", "p_venta", "p_prov", "b_venta", "b_prov", "c_venta", "c_prov", "cant_p", "cant_b")
    tabla = ttk.Treeview(v_cel, columns=columnas, show="headings")
    
    headers = ["ID", "Marca", "Modelo", "Pantalla Venta", "Pantalla Prov", "Batería Venta", "Batería Prov", "Centro Carga Venta", "Centro Carga Prov", "Stock Pant", "Stock Bat"]
    for col, h in zip(columnas, headers):
        tabla.heading(col, text=h)
        tabla.column(col, width=90, anchor="center" if col not in ["marca", "modelo"] else "w")

    tabla.pack(fill="both", expand=True, padx=15, pady=15)

    if datos:
        for f in datos:
            tabla.insert("", "end", values=(f.get("id", ""), f.get("Marca", ""), f.get("Modelo", ""), f"${f.get('Pantalla Venta', 0)}", f"${f.get('Pantalla Provedor', 0)}", f"${f.get('Bateria Venta', 0)}", f"${f.get('Bateria Provedor', 0)}", f"${f.get('C/Carga Venta', 0)}", f"${f.get('C/Carga Provedor', 0)}", f.get("Cantidad Pantalla", 0), f.get("Cantidad Bateria", 0)))

    frame_ops = ctk.CTkFrame(v_cel, fg_color="transparent")
    frame_ops.pack(pady=10)
    ctk.CTkButton(frame_ops, text="➕ Añadir Componente", fg_color="#27AE60").pack(side="left", padx=6)
    ctk.CTkButton(frame_ops, text="✏️ Actualizar Precios/Cantidades", fg_color="#E67E22").pack(side="left", padx=6)
    ctk.CTkButton(frame_ops, text="🗑️ Eliminar Stock", fg_color="#C0392B").pack(side="left", padx=6)

    ctk.CTkButton(v_cel, text="Regresar al Stock", fg_color="#7F8C8D", command=v_cel.destroy).pack(pady=10)

def ventana_laptops():
    v_lap = ctk.CTkToplevel()
    v_lap.title("Inventario - Piezas de Laptop")
    v_lap.geometry("850x450")
    v_lap.grab_set()

    try:
        datos = sist_laptops.mostrar_laptop().data
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar refacciones de Laptop: {e}")
        return

    aplicar_estilo_tabla(v_lap)
    columnas = ("id", "marca", "categoria", "modelo", "proveedor", "venta", "cantidad")
    tabla = ttk.Treeview(v_lap, columns=columnas, show="headings")
    
    headers = ["ID Componente", "Marca", "Categoría Componente", "Modelo Equipo", "Costo Proveedor", "Precio Venta", "Cantidad Disponible"]
    widths = [100, 110, 150, 130, 110, 110, 110]
    
    for col, h, w in zip(columnas, headers, widths):
        tabla.heading(col, text=h)
        tabla.column(col, width=w, anchor="center" if col not in ["marca", "modelo", "categoria"] else "w")

    tabla.pack(fill="both", expand=True, padx=15, pady=15)

    if datos:
        for f in datos:
            tabla.insert("", "end", values=(f.get("id", ""), f.get("Marca", ""), f.get("Categoria", ""), f.get("Modelo", ""), f"${f.get('Proveedor', 0)}", f"${f.get('Venta', 0)}", f.get("Cantidad", 0)))

    frame_ops = ctk.CTkFrame(v_lap, fg_color="transparent")
    frame_ops.pack(pady=10)
    ctk.CTkButton(frame_ops, text="➕ Agregar Repuesto", fg_color="#27AE60").pack(side="left", padx=6)
    ctk.CTkButton(frame_ops, text="✏️ Modificar Repuesto", fg_color="#E67E22").pack(side="left", padx=6)
    ctk.CTkButton(frame_ops, text="🗑️ Descartar Repuesto", fg_color="#C0392B").pack(side="left", padx=6)

    ctk.CTkButton(v_lap, text="Regresar al Stock", fg_color="#7F8C8D", command=v_lap.destroy).pack(pady=10)

def ventana_controles():
    v_ctrl = ctk.CTkToplevel()
    v_ctrl.title("Inventario - Servicios y Diagnósticos de Controles/Mandos")
    v_ctrl.geometry("950x450")
    v_ctrl.grab_set()

    try:
        datos = sist_controles.mostrar_controles().data
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar base de datos de mandos: {e}")
        return

    aplicar_estilo_tabla(v_ctrl)
    columnas = ("id", "marca", "modelo", "m_sencillo", "m_estandar", "m_completo", "r_joystick", "r_botones", "r_prende")
    tabla = ttk.Treeview(v_ctrl, columns=columnas, show="headings")
    
    headers = ["ID Mando", "Marca", "Modelo Mando", "Mante Sencillo", "Mante Estándar", "Mante Completo", "Rep. Joystick", "Rep. Botones", "Rep. No Prende"]
    for col, h in zip(columnas, headers):
        tabla.heading(col, text=h)
        tabla.column(col, width=100, anchor="center" if col not in ["marca", "modelo"] else "w")

    tabla.pack(fill="both", expand=True, padx=15, pady=15)

    if datos:
        for f in datos:
            tabla.insert("", "end", values=(f.get("id", ""), f.get("Marca", ""), f.get("Modelo", ""), f"${f.get('Mantenimiento Sencillo', 0)}", f"${f.get('Mantenimiento Estandar', 0)}", f"${f.get('Mantenimiento Completo', 0)}", f"${f.get('Reparacion Joystick', 0)}", f"${f.get('Reparacion Botones', 0)}", f"${f.get('Reparacion No Prende', 0)}"))

    frame_ops = ctk.CTkFrame(v_ctrl, fg_color="transparent")
    frame_ops.pack(pady=10)
    ctk.CTkButton(frame_ops, text="➕ Añadir Mando", fg_color="#27AE60").pack(side="left", padx=6)
    ctk.CTkButton(frame_ops, text="✏️ Modificar Tarifas", fg_color="#E67E22").pack(side="left", padx=6)
    ctk.CTkButton(frame_ops, text="🗑️ Eliminar Mando", fg_color="#C0392B").pack(side="left", padx=6)

    ctk.CTkButton(v_ctrl, text="Regresar al Stock", fg_color="#7F8C8D", command=v_ctrl.destroy).pack(pady=10)


# --- PUNTO DE ENTRADA DEL MÓDULO (BOOTSTRAP) ---
if __name__ == "__main__":
    # Inicializa el flujo directamente en la pantalla de control administrativo
    ventana_administrador(sist_admin)
    
    # Bloque de contingencia para pruebas locales del widget de mandos
    ventana_controles = ctk.CTk()
    ventana_controles.title("Controles")
    ventana_controles.geometry("400x350")
    # Limpiar_pantalla(ventana_controles)
    btn_salir = ctk.CTkButton(ventana_controles, text="Salir", command=ventana_stock)
    btn_salir.pack(pady=10)
    ventana_controles.mainloop()
