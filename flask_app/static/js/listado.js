const agrandarFoto = (ruta_de_la_foto) => { 
  const modal = document.getElementById("modal-foto");
  const imagenAmpliada = document.getElementById("imagen-ampliada");
  
  imagenAmpliada.src = ruta_de_la_foto; 
  
  modal.style.display = "flex";
};

const cerrarFoto = () => {
 document.getElementById("modal-foto").style.display = "none";
};




const cargarComentarios = async () => {
    const contenedor_html = document.getElementById("comentarios");

    try{
      const response = await fetch(`/Aviso/${AVISO_ID}/comentarios`);

      if (!response.ok){
        throw new Error("Network response was not ok");
      }
      const lista_comentarios = await response.json();
      
      contenedor_html.innerHTML = "";

      if (lista_comentarios.length == 0){
        contenedor_html.innerHTML = "<p>Aún no hay comentarios</p>";
      } else {
        let comentarios_html = "";

        lista_comentarios.forEach(comentario => {
          comentarios_html += `
          <div class="comentario-item">
            <p class="comentario-meta">
              <strong>${comentario.nombre}</strong> 
              <span class="comentario-fecha">(${comentario.fecha})</span>
            </p>
            <p class="comentario-texto">${comentario.texto}</p>
          </div>
          <hr>
        `;
        });
        contenedor_html.innerHTML = comentarios_html;
      }
      return response;
  }
  catch(error){
    console.error("Error:", error);
  }
};

const agregarComentario = async (event) => {
    event.preventDefault();
    const nombreInput = document.getElementById("comentario-nombre");
    const textoInput = document.getElementById("comentario-texto");
    const boton = document.getElementById("agregar-comentario-btn");

    const nombre = nombreInput.value;
    const texto = textoInput.value;

    if (nombre.length < 3 || texto.length < 5) {
      alert("Nombre (mín 3) y comentario (mín 5) son obligatorios.");
      return;
    }
    boton.disabled = true;

    try {
    const datos = { nombre: nombre, texto: texto };
    const response = await fetch(`/Aviso/${AVISO_ID}/comentarios`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.mensajes.join(", "));
    }
    nombreInput.value = ""; 
    textoInput.value = "";

    await cargarComentarios();
    
  } catch (error) {
    alert("Error al enviar comentario: " + error.message);
  } finally {
    boton.disabled = false;
  }
};

document.addEventListener("DOMContentLoaded", () => {
    cargarComentarios();

  const formComentarios = document.getElementById("form-comentario");
  formComentarios.addEventListener("submit", agregarComentario);
});
