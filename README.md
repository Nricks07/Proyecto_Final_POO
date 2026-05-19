# Sistema para Tienda de Reparación de Aparatos Electrónicos 

Este sistema se realizó para que las tiendas, en específico de reparaciones de electrónicos, lleven un mejor control sobre trabajos, inventarios, ingresos y/o gastos. 

Asimismo, se buscó crear una página web en la cual el cliente pueda generar una solicitud sobre algún servicio que ofrezca el negocio, así como verificar el estado de sus solicitudes en tiempo real.

---

## Tecnologías Utilizadas

* **Lenguajes:** Python, JavaScript, CSS y HTML
* **Interfaz Gráfica:** CustomTkinter / Tkinter
* **Base de Datos:** Supabase
* **Control de Versiones:** Git y GitHub

---

## Características Principales

*  **Autenticación:** Inicio de sesión seguro tanto para usuarios (clientes) como para el administrador.
* **Gestión de Inventario, Solicitudes, Distribuidores y Finanzas:** El administrador puede verificar el estado de todas las solicitudes que los clientes hayan realizado, checar la cantidad con la que cuenta sobre piezas y poder contactar a distribuidores cuando quede poco stock. Por último, permite ver cuáles han sido los gastos o ingresos del negocio.

---

##  Instalación y Ejecución

Para poder ejecutar este proyecto de forma local, sigue estos pasos:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/Nricks07/Proyecto_Final_POO.git](https://github.com/Nricks07/Proyecto_Final_POO.git)
cd Proyecto_Final_POO
```
 ### 2. Instalar dependencias
pip install customtkinter 
pip install supabase
pip install customtkinter supabase python-dotenv

### 3. Configuracion Variable de Entorno
El proyecto requiere de credenciales para conectarse a la base de datos de Supabase. 

1. Crea un archivo llamado `.env` en la raíz del proyecto.
2. Copia y pega las siguientes variables y asigna tus credenciales correspondientes:

```env
SUPABASE_URL=tu_url_de_supabase_aqui
SUPABASE_KEY=tu_clave_anon_de_supabase_aqui
```

### 4. Ejecutar la pagina web
python app.py

### 5. Ejecutar Interfaz de Administrador
python frontend.py
nota: debe ejecutarse antes Backend 
