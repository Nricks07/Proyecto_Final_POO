from flask import Flask, render_template, request, redirect, url_for, session
from Backend import * # Importar Backend.py que ya inicializa supabase

app = Flask(__name__)
app.secret_key = 'techfix_secreto_123'
# RUTAS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correoI=request.form.get('correo')
        passwordI=request.form.get('password')
        
        respuesta = supabase.table("Clientes").select("*").eq("Email", correoI).execute()
        
        if respuesta.data and respuesta.data[0].get("Contraseña") == passwordI:
            usuarioValidar = respuesta.data[0]
            session['id'] = usuarioValidar['id']
            session['correo'] = correoI
            session['nombre'] = usuarioValidar['Nombre']
            session['rol'] = "Cliente"

            print(f"¡{usuarioValidar['Nombre']} ha iniciado sesión!")
            return redirect(url_for('index'))
        else:
            return redirect(url_for('crearCuenta', alerta="credencialesMalas"))
    return render_template('inicioSesion.html')

@app.route('/crearCuenta', methods=['GET', 'POST'])
def crearCuenta():
    if request.method=='POST':
        correo=request.form.get('correo')
        password=request.form.get('password')
        nombre=request.form.get('nombre')
        apellido=request.form.get('apellido')
        telefono=request.form.get('telefono')
        nombre_completo = f"{nombre} {apellido}"

        respuesta = supabase.table("Clientes").select("*").eq("Email", correo).execute()
        if respuesta.data:
            return redirect(url_for('crearCuenta', alerta="correo_existente "))
            
        usr = Usuario()
        res = usr.crear_usuario(nombre_completo, correo, telefono, password)

        if res.data:
            #Autoinicio de sesion
            session['id'] = res.data[0]['id']
            session['correo']=correo
            session['nombre']=nombre
            session['rol']="Cliente"
            return redirect(url_for('index'))
        else:
            return redirect(url_for('crearCuenta', alerta="error_creacion"))
    return render_template('crearCuenta.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/cellphone', methods=['GET', 'POST'])
def cellphone():
    if not session.get('nombre'):
        return redirect(url_for('login', alerta="necesita_registro"))
    if request.method == 'POST':
        marca = request.form.get('marca')
        detalles = request.form.get('detalles')
        reparaciones = request.form.getlist('reparacion')
        modelo=request.form.get('modelo')
        correo=session.get('correo')

        #ticket
        reparaciones_str = ', '.join(reparaciones) if reparaciones else "Ninguno"
        descripcion = f"Marca: {marca}, Modelo: {modelo}, Detalles: {detalles}, Problemas: {reparaciones_str}"
        
        sol = Solicitudes(cat="Celular", id_client=session.get('id'), tipo="Reparación")
        sol.agregar_soli(descripcion)

        return redirect(url_for('Tickets'))

    return render_template('celulares.html')

@app.route('/laptops_PC', methods=['GET','POST'])
def laptops_PC():
    if not session.get('nombre'):
        return redirect(url_for('login', alerta="necesita_registro"))
    if request.method=='POST':
        mantenimiento=request.form.get('mantenimiento')
        programas=request.form.getlist('programas')
        actualizacion=request.form.get('update')
        detalles=request.form.get('detalles')
        tipo=request.form.get('tipo_equipo')
        piezas=request.form.getlist('piezas')
        marca=request.form.get('marca_laptop')
        modelo=request.form.get('modelo_laptop')
        correo=session.get('correo')

        if tipo=='Laptop':
            categoria="Laptop"
            marcaF=marca if marca else "No especificada"
        else:
            categoria="PC de escritorio"
            marcaF="PC armada"

        problemas=programas+piezas
        if mantenimiento:
            problemas.append(mantenimiento)
        
        #Generacion de ticket
        problemas_str = ', '.join(problemas) if problemas else "Ninguno"
        descripcion = f"Marca: {marcaF}, Modelo: {modelo}, Detalles: {detalles}, Problemas: {problemas_str}"
        
        sol = Solicitudes(cat=categoria, id_client=session.get('id'), tipo="Reparación")
        sol.agregar_soli(descripcion)

        return redirect(url_for('Tickets'))

    return render_template('laptopsPC.html')

@app.route('/consolas', methods=['GET', 'POST'])
def consolas():
    if not session.get('correo'):
        return redirect(url_for('login', alerta="necesita_registro"))
    
    if request.method == 'POST':
        marca=request.form.get('marca')
        modelo=request.form.get('modelo')
        problemas=request.form.get('reparacion_control')
        detalles=request.form.get('detalles')
        correo=session.get('correo')

        descripcion = f"Marca: {marca}, Modelo: {modelo}, Detalles: {detalles}, Problemas: {problemas}"
        sol = Solicitudes(cat="Consola", id_client=session.get('id'), tipo="Reparación")
        sol.agregar_soli(descripcion)

        return redirect(url_for('Tickets'))

    return render_template('consolas.html')

@app.route('/otros', methods=['GET', 'POST'])
def otros():
    if not session.get('correo'):
        return redirect(url_for('login', alerta="necesita_registro"))
    
    if request.method=='POST':
        tipoAparato=request.form.get('tipoAparato')
        marca=request.form.get("marca")
        modelo=request.form.get('modelo')
        detalles=request.form.get('detalles')
        problemas=request.form.get('problemas')
        correo=session.get('correo')

        #ticket otros
        descripcion = f"Aparato: {tipoAparato}, Marca: {marca}, Modelo: {modelo}, Detalles: {detalles}, Problemas: {problemas}"
        sol = Solicitudes(cat="Otros", id_client=session.get('id'), tipo="Reparación")
        sol.agregar_soli(descripcion)

        return redirect(url_for('Tickets'))
    return render_template('otros.html')

@app.route('/Tickets')
def Tickets():
    if not session.get('correo'):
        return redirect(url_for('login', alerta="necesita_registro"))
    
    id_cliente = session.get('id')
    filtro = request.args.get('filtro', 'General')
    
    usr = Usuario(id_cliente=id_cliente)
    respuesta = usr.ver_mis_solicitudes()
    mis_tickets_reales = respuesta.data if hasattr(respuesta, 'data') and respuesta.data else []

    totAct=0
    totRep=0
    for t in mis_tickets_reales:
        estado = t.get('estado', '')
        if estado == "Pendiente" or estado == "En proceso" or estado == "En Proceso":
            totAct+=1
        elif estado == "Finalizado":
            totRep+=1

    tickets_filtrados = []
    if filtro == 'General':
        tickets_filtrados = mis_tickets_reales
    else:
        for t in mis_tickets_reales:
            if t.get('estado') == filtro:
                tickets_filtrados.append(t)
                
    # Formatear datos para la plantilla Jinja2
    for t in tickets_filtrados:
        t['id_solicitud'] = t.get('id')
        t['fecha'] = t.get('fecha_recibo', 'Sin fecha')
        t['marca'] = "Detalle"
        t['modelo'] = "Solicitud"
        t['problemas'] = [t.get('descripcion', 'Sin descripción')]
        t['detalles'] = "Tipo: " + t.get('tipo', '')

    return render_template('ticketsUsuarios.html', ticketFiltrado=tickets_filtrados, filtroActual=filtro, activos=totAct, reparados=totRep)

@app.route('/cancelarT/<int:id_ticket>')
def cancelar_ticket(id_ticket):
    sol = Solicitudes()
    sol.cambiar_estado_soli(id_ticket, "Cancelado")
    return redirect(url_for('Tickets'))
    
if __name__ == '__main__':
    app.run(debug=True)