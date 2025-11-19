const validarForm = () => {
    const validadorMail = (mail) => mail && mail.includes("@") && mail.length <= 100;
    const validadorNombre = (nombre) => nombre && nombre.length >= 3 && nombre.length <= 200;
    const validadorSector = (sector) => !sector || (sector.length >= 1 && sector.length <= 100);
    const validadorTelefono = (telefono) => {
      if (!telefono) return true;
      let re =  /^\+\d{11}$/;
      return re.test(telefono);
    };
    const validadorContactoFinal = (identificador, medio) => {
        if (!medio || medio === "") return true; 
        return identificador && identificador.length >= 4 && identificador.length <= 50;
    };
    const validadorFotos = (files) => files.length >= 1 && files.length <= 5;
    const validadorFecha = (fecha) => {
        if (!fecha) return false;
        let fechaIn = new Date(fecha);
        let fechaActual = new Date();
        let fechaMinima = new Date(fechaActual.getTime() + (3 * 60 * 6 * 1000));
        return fechaIn >= fechaMinima;
    };


    let emailInput = document.getElementById("email");
    let nameInput = document.getElementById("nombre");
    let sectorInput = document.getElementById("sector");
    let telefonoInput = document.getElementById("telefono");
    let regionSelect = document.getElementById("seleccionar-región");
    let comunaSelect = document.getElementById("seleccionar-comuna");
    let tipoSelect = document.getElementById("seleccionar-tipo");
    let cantidadInput = document.getElementById("cantidad");
    let edadInput = document.getElementById("edad");
    let unidadTiempoSelect = document.getElementById("seleccionar-unidad-tiempo");
    let fechaInput = document.getElementById("fecha-disponible");
    let fotosInputs = document.querySelectorAll(".fotoInput");
    let contactoFinalInput = document.getElementById("contactoTextarea");
    let medioSelect = document.getElementById("seleccionar-medio");
    
    let allFiles = [];
    fotosInputs.forEach(input => {
      for (let f of input.files) {
        if (f.name) allFiles.push(f);
      }
    });

    let isValid = true;
    let msg = "Errores encontrados:\n";

    if (!regionSelect.value) { msg += "- Debe seleccionar una región.\n"; isValid = false; }
    if (!comunaSelect.value) { msg += "- Debe seleccionar una comuna.\n"; isValid = false; }
    if (!validadorSector(sectorInput.value)) { msg += "- Sector inválido (máx. 100 caracteres).\n"; isValid = false; }
    
    if (!validadorNombre(nameInput.value)) { msg += "- Nombre inválido (mín. 3, máx. 200 caracteres).\n"; isValid = false; }
    if (!validadorMail(emailInput.value)) { msg += "- Email inválido (debe incluir @ y .).\n"; isValid = false; }
    if (!validadorTelefono(telefonoInput.value)) { msg += "- Formato de Teléfono móvil inválido (ej: +56999999999).\n"; isValid = false; }
    if (!validadorContactoFinal(contactoFinalInput.value, medioSelect.value)) { msg += "- Identificador de contacto obligatorio (4-50 caracteres) si se selecciona un medio.\n"; isValid = false; }


    if (!tipoSelect.value) { msg += "- Debe seleccionar un tipo de mascota.\n"; isValid = false; }
    if (!cantidadInput.value || parseInt(cantidadInput.value) < 1) { msg += "- Cantidad inválida (mín. 1).\n"; isValid = false; }
    if (!edadInput.value || parseInt(edadInput.value) < 1) { msg += "- Edad inválida (mín. 1).\n"; isValid = false; }
    if (!unidadTiempoSelect.value) { msg += "- Debe seleccionar una unidad de tiempo.\n"; isValid = false; }
    if (!fechaInput.value) { msg += "- Debe ingresar fecha disponible.\n"; isValid = false; }
    if (!validadorFecha(fechaInput.value)) { msg += "- Fecha inválida (debe ser mayor o igual a la fecha/hora actual + 3 horas).\n"; isValid = false; }
    if (!validadorFotos(allFiles)) { msg += "- Debe subir entre 1 y 5 fotos.\n"; isValid = false; }


    if (isValid) {
      let confirmBox = document.getElementById("confirm-box");
      document.getElementById("main-container").style.display = "block";
      confirmBox.style.display = "block";
      
      document.getElementById("confirm-yes").onclick = () => {
          confirmBox.style.display = "none";
          document.getElementById("AvisoForm").submit(); 
      };
      
      document.getElementById("confirm-no").onclick = () => {
        confirmBox.style.display = "none";
        document.getElementById("main-container").style.display = "block";
      };
      return;
    };  
    
    alert(msg);
  };
  
  let submitBtn = document.getElementById("boton-confirmar-js");
  submitBtn.addEventListener("click", validarForm);