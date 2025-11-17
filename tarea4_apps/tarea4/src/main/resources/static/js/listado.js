function mostrarFormulario(avisoId) {
    const celdaAccion = document.getElementById('accion-' + avisoId);

    const inputNota = document.createElement('input');
    inputNota.type = 'number';
    inputNota.id = 'input-nota-' + avisoId; 
    inputNota.min = 1;
    inputNota.max = 7;
    inputNota.placeholder = 'Nota (1-7)';
    inputNota.style.width = '100px'; 

    const botonGuardar = document.createElement('button');
    botonGuardar.textContent = 'Guardar';
    botonGuardar.onclick = () => enviarNota(avisoId); 

    celdaAccion.innerHTML = ''; 
    
    celdaAccion.appendChild(inputNota);
    celdaAccion.appendChild(botonGuardar);
}

async function enviarNota(avisoId) {
    const inputNota = document.getElementById('input-nota-' + avisoId);
    const notaString = inputNota.value;
    const nota = parseInt(notaString, 10);

    if (isNaN(nota) || nota < 1 || nota > 7 || notaString !== nota.toString()) {
        alert("Error: Debe ingresar un número entero entre 1 y 7.");
        return; 
    }

    console.log(`Nota válida: ${nota}. Enviando al servidor...`);

    try {
        const url = `/api/avisos/${avisoId}/evaluar?nota=${nota}`;

        const respuesta = await fetch(url, {
            method: 'POST',
            headers: { 'Accept': 'application/json' }
        });

        if (!respuesta.ok) {
            const errorData = await respuesta.json();
            throw new Error(errorData.error || 'Error al guardar la nota.');
        }

        const data = await respuesta.json(); 
        const nuevoPromedio = data.nuevoPromedio;

        const celdaNota = document.getElementById('nota-' + avisoId);
        celdaNota.textContent = nuevoPromedio;

        const celdaAccion = document.getElementById('accion-' + avisoId);
        
        celdaAccion.innerHTML = `<button type="button" onclick="mostrarFormulario(${avisoId})">evaluar</button>`;

    } catch (error) {
        console.error("Error en la llamada fetch:", error);
        alert("Hubo un error al guardar tu nota: " + error.message);
    }
}