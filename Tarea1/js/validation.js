  // validacion formulario
  const validarForm = () => {
    // funciones auxiliares
    const validadorMail = (mail) => mail && mail.includes("@");
    const validadorNombre = (nombre) => nombre && nombre.length > 3 && nombre.length < 200;
    const tieneNumeros = (str) => /\d/.test(str);
    const validadorSector = (sector) => !sector || (sector.length >= 1 && sector.length <= 100); //No sé si es necesario la verdad
    const validadorTelefono = (telefono) => {
    if (!telefono) return false;
    let lengthValid = telefono.length >= 8;

    let re =  /^\+?[0-9]+$/;
    let formatValid = re.test(telefono);

    return lengthValid && formatValid;
      };
    const validadorFotos = (files) => files.length > 0 && files.length <= 5;
    const validadorFecha = (fecha) => {
        let fechaActual = new Date();
        let fechaIn = new Date(fecha);
        fechaActual.setHours(fechaActual.getHours() -1);
        return fechaIn > fechaActual;
    };

    //Inputs
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
    


    let allFiles = [];
    fotosInputs.forEach(input => {
      for (let f of input.files) allFiles.push(f);
    });

    let isValid = true;
    let msg = "";

    if (!validadorMail(emailInput.value)) {
      msg += "Mail inválido!\n";
      emailInput.style.borderColor = "red"; // cambiar estilo con JS!!
      isValid = false;
    } else {
      emailInput.style.borderColor = "";
    }

    if (!validadorNombre(nameInput.value)) { 
      msg += "Nombre inválido!\n";
      nameInput.style.borderColor = "red";
      isValid = false;
    } else {
      nameInput.style.borderColor = "";
    }

    if (!validadorSector(sectorInput.value)) {
      msg += "Sector inválido!\n";
      sectorInput.style.borderColor = "red";
      isValid = false;
    } else {
      sectorInput.style.borderColor = "";
    }
    
    if (!validadorTelefono(telefonoInput.value)) {
      msg += "Teléfono inválido!\n";
      telefonoInput.style.borderColor = "red";
      isValid = false;
    } else {
      telefonoInput.style.borderColor = "";
    }
    
    if (!regionSelect.value) {
      msg += "Debe seleccionar una región\n";
      regionSelect.style.borderColor = "red";
      isValid = false;
    } else regionSelect.style.borderColor = "";
    
    if (!comunaSelect.value) {
      msg += "Debe seleccionar una comuna\n";
      comunaSelect.style.borderColor = "red";
      isValid = false;
    } else comunaSelect.style.borderColor = "";
    
    if (!tipoSelect.value) {
      msg += "Debe seleccionar un tipo\n";
      tipoSelect.style.borderColor = "red";
      isValid = false;
    } else tipoSelect.style.borderColor = "";

    if (!cantidadInput.value || cantidadInput.value < 1) {
      msg += "Cantidad inválida\n";
      cantidadInput.style.borderColor = "red";
      isValid = false;
    } else cantidadInput.style.borderColor = "";

    if (!edadInput.value || edadInput.value < 1) {
      msg += "Edad inválida\n";
      edadInput.style.borderColor = "red";
      isValid = false;
    } else edadInput.style.borderColor = "";

    if (!unidadTiempoSelect.value) {
      msg += "Debe seleccionar una unidad de tiempo\n";
      unidadTiempoSelect.style.borderColor = "red";
      isValid = false;
    } else unidadTiempoSelect.style.borderColor = "";

    if (!fechaInput.value) {
      msg += "Debe ingresar fecha disponible\n";
      fechaInput.style.borderColor = "red";
      isValid = false;
    } else fechaInput.style.borderColor = "";

    if (!validadorFecha(fechaInput.value)) {
      msg += "Fecha inválida!\n";
      fechaInput.style.borderColor = "red";
      isValid = false;
    } else {
      fechaInput.style.borderColor = "";
    };

    if (!validadorFotos(allFiles)) {
      msg += "Debe subir entre 1 y 5 fotos\n";
      isValid = false;
    };

    if (isValid) {
      let confirmBox = document.getElementById("confirm-box");
      let successBox = document.getElementById("success-box");
      msg = "Felicidades tu aviso se subió correctamente";
      isValid = true;
      document.getElementById("main-container").style.display = "none";
      confirmBox.style.display = "block";
      document.getElementById("confirm-yes").onclick = () => {
          confirmBox.style.display = "none";
          successBox.style.display = "block";
      };
      document.getElementById("confirm-no").onclick = () => {
        confirmBox.style.display = "none";
        document.getElementById("main-container").style.display = "block";
      };
      return;
    };  
    alert(msg); // alertas JS
  };
  // recuperamos el boton que envia el form
  let submitBtn = document.getElementById("envio");
  submitBtn.addEventListener("click", validarForm);
