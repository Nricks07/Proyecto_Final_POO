import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

try:
    supabase = create_client(url, key)
    print("--- Sistema de Gestión de Reparaciones ---")
    print("¡Conexión exitosa al sistema de la tienda!")
except Exception as e:
    print(f"Error al conectar: {e}")

class Persona:
    def __init__(self, name="", mail="", cel=""):
        self.nombre = name
        self.correo = mail
        self.num_cel = cel

    @staticmethod
    def login(correo, contra):
        try:
            sesion = supabase.auth.sign_in_with_password({
                "email": correo,
                "password": contra,
            })
            return sesion
        except Exception as e:
            raise Exception(f"Error al iniciar sesión: {e}")

class Administrador(Persona):
    def __init__(self, nom="", mail="", cel="", id_admin="", contra=""):
        super().__init__(nom, mail, cel)
        self.contraseña = contra
        self.id_admin = id_admin

    def cambiar_estado_soli(self, id_solicitud, new_estado):
        actualizar = supabase.table("Solicitudes").update({"estado": new_estado}).eq("id", id_solicitud).execute()
        return actualizar

    def gest_stock(self):
        stock = Stock()
        return stock.mostrar_stock()

    def contactar_distribuidores(self):
        mostrar = supabase.table("Distribuidor").select("*").execute()
        return mostrar

    def ingresos(self):
        mostrar = supabase.table("Finanzas").select("*").eq("tipo", "Ingreso").execute()
        return mostrar

    def gastos(self):
        mostrar = supabase.table("Finanzas").select("*").eq("tipo", "Gasto").execute()
        return mostrar

    def gest_clientes(self):
        mostrar = supabase.table("Clientes").select("*").execute()
        return mostrar

    def gest_soli(self):
        mostrar = supabase.table("Solicitudes").select("*").execute()
        return mostrar

class Distruidor(Persona):
    def __init__(self, name="", mail="", cel=""):
        super().__init__(name, mail, cel)

class Usuario(Persona):
    def __init__(self, id_cliente="", nom="", mail="", cel="", contra=""):
        super().__init__(nom, mail, cel)
        self.id_cliente = id_cliente 
        self.contraseña = contra


    def crear_usuario(self, nom, mail, cel, contra):
        nuevo_usuario = {
            "Nombre" : nom,
            "Email" : mail,
            "Celular" : cel,
            "Contraseña" : contra,
        }
        insertar = supabase.table("Clientes").insert([nuevo_usuario]).execute()

        if insertar.data:
            self.id_cliente = insertar.data[0]['id'] 
            return insertar

    def crear_soli(self, cat, id_client, tipo):
        solicitud = Solicitudes(cat, id_client, tipo)
        return solicitud

    def eliminar_soli(self, id_sol):
        eliminar = supabase.table("Solicitudes").delete().eq("id", id_sol).execute()
        return eliminar

    def ver_mis_solicitudes(self):
        mostrar = supabase.table("Solicitudes").select("*").eq("id_cliente", self.id_cliente).execute()
        return mostrar

class Aparato:
    def __init__(self, id_prod="", marca="", mod=""):
        self.id_producto = id_prod
        self.marca = marca
        self.modelo = mod

class Celular(Aparato):
    def __init__(self, id_prod="", marca="", mod="", falla_especifica_cel=""):
        super().__init__(id_prod, marca, mod)
        self.falla_especifica = falla_especifica_cel

class Consola(Aparato):
    def __init__(self, id_prod="", marca="", mod="", falla_especifica_consola=""):
        super().__init__(id_prod, marca, mod)
        self.falla_especifica = falla_especifica_consola

class Laptop(Aparato):
    def __init__(self, id_prod="", marca="", mod="", falla_especifica_laptop=""):
        super().__init__(id_prod, marca, mod)
        self.falla_especifica = falla_especifica_laptop

class Solicitudes:
    def __init__(self, cat="", id_client="", tipo=""):
        self.categoria = cat
        self.tipo = tipo
        self.id_cliente = id_client
        
    def agregar_soli(self, descripcion):
        nueva_solicitud = {
            "categoria" : self.categoria,
            "id_cliente" : self.id_cliente,
            "tipo" : self.tipo,
            "estado" : "Pendiente",
            "descripcion" : descripcion,
            "costo": 0.0,
        }

        insertar = supabase.table("Solicitudes").insert([nueva_solicitud]).execute()

        if insertar.data:
            self.id_solicitud = insertar.data[0]['id'] 
            
        return insertar

    def agregar_precio(self, costo_sol):
        actualizar = supabase.table("Solicitudes").update({"costo": costo_sol}).eq("id", self.id_solicitud).execute()
        return actualizar

    def mostrar_solicitudes(self):
        mostrar = supabase.table("Solicitudes").select("*").execute()
        return mostrar

    def mostrar_solicitudes_pendientes(self):
        mostrar = supabase.table("Solicitudes").select("*").eq("estado", "Pendiente").execute()
        return mostrar

    def mostrar_solicitudes_en_proceso(self):
        mostrar = supabase.table("Solicitudes").select("*").eq("estado", "En Proceso").execute()
        return mostrar

    def mostrar_solicitudes_finalizadas(self):
        mostrar = supabase.table("Solicitudes").select("*").eq("estado", "Finalizado").execute()
        if mostrar.data:
            descripcion = mostrar.data[-1].get('descripcion', 'Reparación Finalizada')
            monto = float(mostrar.data[-1].get('costo', 0))
            mostrar2 = supabase.table("Finanzas").insert([{"descripcion": descripcion, "monto" : monto, "tipo" : "Ingreso"}]).execute()
            return mostrar, mostrar2
        return mostrar, None

    def cambiar_estado_soli(self, id_sol, estado):
        actualizar = supabase.table("Solicitudes").update({"estado": estado}).eq("id", id_sol).execute()
        return actualizar

    def eliminar_soli(self, id_sol):
        eliminar = supabase.table("Solicitudes").delete().eq("id", id_sol).execute()
        return eliminar

class Stock:
    def __init__(self):
        pass

    def agregar_nuevo(self, nombre, prec_comp, prec_venta, cant_existente):
        nuevo_producto ={
            "Nombre" : nombre,
            "Precio-Compra" : prec_comp,
            "Precio-Venta" : prec_venta,
            "Cantidad" : cant_existente,
        }

        insertar = supabase.table("Productos").insert([nuevo_producto]).execute()
        return insertar

    def agregar_cant(self, nombre, cantidad):
        agregar = supabase.table("Productos").update({"Cantidad": cantidad}).eq("Nombre", nombre).execute()
        monto_resp = supabase.table("Productos").select("Precio-Compra").eq("Nombre", nombre).execute()
        if monto_resp.data:
            monto = float(monto_resp.data[0]['Precio-Compra'])
            monto_final = monto * cantidad
            gasto = supabase.table("Finanzas").insert([{"descripcion" : "Compra de Repuestos", "monto" : monto_final, "tipo" : "Gasto"}]).execute()
            return agregar, gasto
        return agregar, None

    def mostrar_stock(self):
        mostrar = supabase.table("Productos").select("*").execute()
        return mostrar

    def eliminar_stock(self, id_producto):
        eliminar = supabase.table("Productos").delete().eq("Id", id_producto).execute()
        return eliminar

class Piezas_Consola(Stock):
    def __init__(self, marca="", modelo="", mante_sencillo=0, mante_estandar=0, mante_completo=0, repa_ruido=0, repa_novideo=0, repa_noprende=0):
        super().__init__()
        self.marca = marca
        self.modelo = modelo
        self.mante_sencillo = mante_sencillo
        self.mante_estandar = mante_estandar
        self.mante_completo = mante_completo
        self.repa_ruido = repa_ruido
        self.repa_no_video = repa_novideo
        self.repa_no_enciende = repa_noprende

    def agregar_piezas(self):
        nueva_pieza = {
            "Marca" : self.marca,
            "Modelo" : self.modelo,
            "Mantenimiento Sencillo" : self.mante_sencillo,
            "Mantenimiento Estandar" : self.mante_estandar,
            "Mantenimiento Completo" : self.mante_completo,
            "Reparación Ruido" : self.repa_ruido,
            "Reparación No Da Video" : self.repa_novideo,
            "Reparación No Prende" : self.repa_noprende,
        }
        insertar = supabase.table("Consola").insert([nueva_pieza]).execute()
        return insertar

    def agregar_cantidad(self, id_consola, cantidad):
        actualizar = supabase.table("Consola").update({"Cantidad" : cantidad}).eq("id", id_consola).execute()
        return actualizar
    
    def mostrar_consola(self):
        mostrar = supabase.table("Consola").select("*").execute()
        return mostrar

    def eliminar_consola(self, id_consola):
        eliminar = supabase.table("Consola").delete().eq("Id", id_consola).execute()
        return eliminar

    def actualizar_consola(self, id_consola, mante_sencillo, mante_estandar, mante_completo, repa_ruido, repa_novideo, repa_noprende):
        actualizar = supabase.table("Consola").update({"Mantenimiento Sencillo" : mante_sencillo, "Mantenimiento Estandar" : mante_estandar, "Mantenimiento Completo" : mante_completo, "Reparacion Ruido" : repa_ruido, "Reparacion No DaVideo" : repa_novideo, "Reparacion NoPrende" : repa_noprende}).eq("id", id_consola).execute()
        return actualizar

class Piezas_Celular(Stock):
    def __init__(self, marca="", modelo="", pantalla_venta=0, pantalla_compra=0, bateria_venta=0, bateria_compra=0, centro_carga_venta=0, centro_carga_compra=0,camara_venta=0, camara_compra=0, carcasa_venta=0, carcasa_compra=0, cantidad_pantalla=0, cantidad_bateria=0, cantidad_centro_carga=0, cantidad_camara=0, cantidad_carcasa=0):
        super().__init__()
        self.marca = marca
        self.modelo = modelo
        self.pantalla_venta = pantalla_venta
        self.pantalla_compra = pantalla_compra
        self.bateria_venta = bateria_venta
        self.bateria_compra = bateria_compra
        self.centro_carga_venta = centro_carga_venta
        self.centro_carga_compra = centro_carga_compra
        self.camara_venta = camara_venta
        self.camara_compra = camara_compra
        self.carcasa_venta = carcasa_venta
        self.carcasa_compra = carcasa_compra
        self.cantidad_pantalla = cantidad_pantalla
        self.cantidad_bateria = cantidad_bateria
        self.cantidad_centro_carga = cantidad_centro_carga
        self.cantidad_camara = cantidad_camara
        self.cantidad_carcasa = cantidad_carcasa

    def agregar_piezas(self):
        nueva_pieza = {
            "Marca" : self.marca,
            "Modelo" : self.modelo,
            "Pantalla Venta" : self.pantalla_venta,
            "Pantalla Provedor" : self.pantalla_compra,
            "Bateria Venta" : self.bateria_venta,
            "Bateria Provedor" : self.bateria_compra,
            "C/Carga Venta" : self.centro_carga_venta,
            "C/Carga Provedor" : self.centro_carga_compra,
            "Camara Venta" : self.camara_venta,
            "Camara Provedor" : self.camara_compra,
            "Carcasa Venta" : self.carcasa_venta,
            "Carcasa Provedor" : self.carcasa_compra,
            "Cantidad Pantalla" : self.cantidad_pantalla,
            "Cantidad Bateria" : self.cantidad_bateria,
            "Cantidad C/Carga" : self.cantidad_centro_carga,
            "Cantidad Camara" : self.cantidad_camara,
            "Cantidad Carcasa" : self.cantidad_carcasa,
        }
        insertar = supabase.table("Celular").insert([nueva_pieza]).execute()
        return insertar

    def agregar_cantidad(self, id_celular, cantidad, categoria_pieza, Pieza):
        categoria = ["Pantalla Provedor", "Bateria Provedor", "C/Carga Provedor", "Camara Provedor", "Carcasa Provedor"]
        cantidades = ["Cantidad Pantalla", "Cantidad Bateria", "Cantidad C/Carga", "Cantidad Camara", "Cantidad Carcasa"]
        cate = categoria[categoria_pieza]
        canti = cantidades[Pieza]
        actualizar = supabase.table("Celular").update({canti : cantidad}).eq("id", id_celular).execute()
        monto_resp = supabase.table("Celular").select(cate).eq("id", id_celular).execute()
        if monto_resp.data:
            monto = float(monto_resp.data[0][cate])
            monto_final = monto * cantidad
            gasto = supabase.table("Finanzas").insert([{"descripcion" : "Compra de Repuestos", "monto" : monto_final, "tipo" : "Gasto"}]).execute()
            return actualizar, gasto
        return actualizar, None
    
    def mostrar_celular(self):
        mostrar = supabase.table("Celular").select("*").execute()
        return mostrar

    def eliminar_celular(self, id_celular):
        eliminar = supabase.table("Celular").delete().eq("id", id_celular).execute()
        return eliminar
    
    def actualizar_celular(self, id_celular, pantalla_venta, pantalla_compra, bateria_venta, bateria_compra, centro_carga_venta, centro_carga_compra, carcasa_venta, carcasa_compra, cantidad):
        actualizar = supabase.table("Celular").update({"Pantalla Venta" : pantalla_venta, "Pantalla Provedor" : pantalla_compra, "Bateria Venta" : bateria_venta, "Bateria Provedor" : bateria_compra, "C/Carga Venta" : centro_carga_venta, "C/Carga Provedor" : centro_carga_compra, "Carcasa Venta" : carcasa_venta, "Carcasa Provedor" : carcasa_compra, "Cantidad" : cantidad}).eq("id", id_celular).execute()
        return actualizar

class Piezas_Laptop(Stock):
    def __init__(self, marca="", categoria="", modelo="", proveedor=0, venta=0, cantidad=0): 
        super().__init__()
        self.marca = marca
        self.categoria = categoria
        self.modelo = modelo
        self.venta = venta
        self.proveedor = proveedor
        self.cantidad = cantidad

    def agregar_piezas(self):
        nueva_pieza = {
            "Marca" : self.marca,
            "Categoria" : self.categoria,
            "Modelo" : self.modelo,
            "Proveedor" : self.proveedor,
            "Venta" : self.cantidad,
            "Cantidad" : self.cantidad,
        }
        insertar = supabase.table("Laptop").insert([nueva_pieza]).execute()
        return insertar

    def agregar_cantidad(self, id_pieza, cantidad):
        actualizar = supabase.table("Laptop").update({"Cantidad" : cantidad}).eq("id", id_pieza).execute()
        monto_resp = supabase.table("Laptop").select("Proveedor").eq("id", id_pieza).execute()
        if monto_resp.data:
            monto = float(monto_resp.data[0]['Proveedor'])
            monto_final = monto * cantidad
            gasto = supabase.table("Finanzas").insert([{"descripcion" : "Compra de Repuestos", "monto" : monto_final, "tipo" : "Gasto"}]).execute()
            return actualizar, gasto
        return actualizar, None

    def mostrar_laptop(self):
        mostrar = supabase.table("Laptop").select("*").execute()
        return mostrar

    def eliminar_laptop(self, id_laptop):
        eliminar = supabase.table("Laptop").delete().eq("id", id_laptop).execute()
        return eliminar
    
    def actualizar_laptop(self, id_laptop, venta, cantidad):
        actualizar = supabase.table("Laptop").update({"Venta" : venta}).eq("id", id_laptop).execute()
        return actualizar

class controles(Stock):
    def __init__(self, marca="", modelo="", mante_sencillo=0, mante_estandar=0, mante_completo=0, repa_joystick=0, repa_botones=0, repa_noprende=0):
        super().__init__()
        self.marca = marca
        self.modelo = modelo
        self.mante_sencillo = mante_sencillo
        self.mante_estandar = mante_estandar
        self.mante_completo = mante_completo
        self.repa_joystick = repa_joystick
        self.repa_botones = repa_botones
        self.repa_noprende = repa_noprende

    def agregar_piezas(self):
        nueva_pieza = {
            "Marca" : self.marca,
            "Modelo" : self.modelo,
            "Mantenimiento Sencillo" : self.mante_sencillo,
            "Mantenimiento Estandar" : self.mante_estandar,
            "Mantenimiento Completo" : self.mante_completo,
            "Reparacion Joystick" : self.repa_joystick,
            "Reparacion Botones" : self.repa_botones,
            "Reparacion No Prende" : self.repa_noprende,
        }
        insertar = supabase.table("Controles").insert([nueva_pieza]).execute()
        return insertar

    def mostrar_controles(self):
        mostrar = supabase.table("Controles").select("*").execute()
        return mostrar

    def eliminar_controles(self, id_control):
        eliminar = supabase.table("Controles").delete().eq("id", id_control).execute()
        return eliminar
    
    def actualizar_controles(self, id_control, mante_sencillo, mante_estandar, mante_completo, repa_joystick, repa_botones, repa_noprende):
        actualizar = supabase.table("Controles").update({"Mantenimiento Sencillo" : mante_sencillo, "Mantenimiento Estandar" : mante_estandar, "Mantenimiento Completo" : mante_completo, "Reparacion Joystick" : repa_joystick, "Reparacion Botones" : repa_botones, "Reparacion No Prende" : repa_noprende}).eq("id", id_control).execute()
        return actualizar