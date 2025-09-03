const data = region_comuna.regiones; 

const poblarRegiones = () => {
  let regionSelect = document.getElementById("seleccionar-región");
  data.forEach(region => {
      let option = document.createElement("option");
      option.value = region.numero;
      option.text = region.nombre
      regionSelect.appendChild(option);
  })
};

const poblarComunas = () => {
  let regionSelect = document.getElementById("seleccionar-región");
  let comunaSelect = document.getElementById("seleccionar-comuna");
  let selectedRegion = regionSelect.value;
  
  comunaSelect.innerHTML = '<option value="">Seleccione una Comuna</option>';
  
  let region = data.find(r => r.numero == selectedRegion);

  if (region) {
      region.comunas.forEach(comuna => {
          let option = document.createElement("option");
          option.value = comuna.id;
          option.text = comuna.nombre;
          comunaSelect.appendChild(option);
      });
  }
};



const contactosData = {
  "medio" : ["Correo", "WhatsApp", "Telegram","X","Instagram","TikTok", "otra"]
}

const poblarContactos = () => {
  let contactoSelect = document.getElementById("seleccionar-medio");

  contactoSelect.innerHTML = '<option value="">Seleccione un medio</option>';

  contactosData.medio.forEach(medio1 => {
      let option = document.createElement("option");
      option.value = medio1;
      option.text = medio1;
      contactoSelect.appendChild(option);
  });
};

const tipoData = {
  "tipo" : ["Gato", "Perro"]
}

const poblarTipo = () => {
  let tipoSelect = document.getElementById("seleccionar-tipo");

  tipoSelect.innerHTML = '<option value="">Seleccione un tipo</option>';

  tipoData.tipo.forEach(tipo1 => {
      let option = document.createElement("option");
      option.value = tipo1;
      option.text = tipo1;
      tipoSelect.appendChild(option);
  });
};

const tiempoData={
  "unidades" : ["Días", "Semanas", "Meses", "Años"]
}

const poblarTiempo = () => {
  let tiempoSelect = document.getElementById("seleccionar-unidad-tiempo");

  tiempoSelect.innerHTML = '<option value="">Seleccione una unidad de Tiempo</option>';

  tiempoData.unidades.forEach(unidad => {
    let option = document.createElement("option");
    option.value = unidad;
    option.text = unidad;
    tiempoSelect.appendChild(option);
  });
};

const poblarFecha = () => {
  let fechaInput = document.getElementById("fecha-disponible");
  let fechaActual = new Date();
  fechaActual.setHours(fechaActual.getHours() -1);// Al parecer así es un +3
  fechaInput.value = fechaActual.toISOString().slice(0, 16);
  
};


const createContacto = () => {
  const contactoSelect = document.getElementById("seleccionar-medio");
  const contactoLabel = document.getElementById("contactoLabel");
  const contactoTextarea = document.getElementById("contactoTextarea");
  
  if (contactoSelect.value !== "") {
      contactoLabel.style.display = "block";
      contactoTextarea.style.display = "block";
  } else {
      contactoLabel.style.display = "none";
      contactoTextarea.style.display = "none";
  };
};


const addFotos = () => {
  let fotosContainer = document.getElementById("fotosContainer");
  let addFotoBtn = document.getElementById("addFotoBtn");
  let fotosInput = fotosContainer.querySelectorAll(".fotoInput");
  if (fotosInput.length < 5) {
    let newInput = document.createElement("input");
    newInput.type = "file";
    newInput.classList.add("fotoInput");
    newInput.accept = "image/*";
    fotosContainer.insertBefore(newInput, addFotoBtn);
    if (fotosInput.length == 4){
     addFotoBtn.style = "display:none"
    };
  };
};

document.getElementById("addFotoBtn").addEventListener("click", addFotos);
document.getElementById("seleccionar-medio").addEventListener("change", createContacto);
document.getElementById("seleccionar-región").addEventListener("change", poblarComunas);




window.onload = () => {
  poblarRegiones();
  poblarContactos();
  poblarTipo();
  poblarTiempo();
  poblarFecha();
};