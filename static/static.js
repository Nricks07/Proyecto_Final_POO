// 1. Nuestra base de datos de modelos (Diccionario)
const modelosPorMarca = {
    'Apple': ['iPhone 13', 'iPhone 14', 'iPhone 15 Pro Max'],
    'Samsung': ['Galaxy S23', 'Galaxy S24 Ultra', 'Galaxy A54'],
    'Xiaomi': ['Poco X5', 'Redmi Note 13', 'Xiaomi 14']
};

// 2. Seleccionamos las cajas de HTML
const selectMarca = document.getElementById('marca');
const selectModelo = document.getElementById('modelo');

// 3. El "Escuchador"
selectMarca.addEventListener('change', function () {
    // Obtenemos la marca que el usuario acaba de elegir (ej. "Apple")
    let marcaElegida = selectMarca.value;

    // Limpiamos el menú de modelos para que no se amontonen
    selectModelo.innerHTML = '<option value="" disabled selected>Elige el modelo...</option>';

    // Si la marca existe en nuestro diccionario
    if (modelosPorMarca[marcaElegida]) {
        // Obtenemos la lista de modelos de esa marca
        let modelos = modelosPorMarca[marcaElegida];

        // Hacemos un ciclo (For loop) para crear una <option> por cada modelo
        modelos.forEach(function (modelo) {
            let nuevaOpcion = document.createElement('option');
            nuevaOpcion.value = modelo;
            nuevaOpcion.text = modelo;
            selectModelo.appendChild(nuevaOpcion); // Lo inyectamos al HTML
        });
    }
});