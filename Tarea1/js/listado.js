const onClick1 = () =>{
    document.getElementById("datosD").style.display="table-row";
    document.getElementById("avisoD1").style.display="table-row";
    document.getElementById("boton-volver").style.display="block";
    document.getElementById("tabla-general").style.display= "none";
    
};
const onClick2 = () =>{
    document.getElementById("datosD").style.display="table-row";
    document.getElementById("avisoD2").style.display="table-row";
    document.getElementById("boton-volver").style.display="block";
    document.getElementById("tabla-general").style.display= "none";
    
};

const onClick3 = () =>{
    document.getElementById("datosD").style.display="table-row";
    document.getElementById("avisoD3").style.display="table-row";
    document.getElementById("boton-volver").style.display="block";
    document.getElementById("tabla-general").style.display= "none";
    
};
const onClick4 = () =>{
    document.getElementById("datosD").style.display="table-row";
    document.getElementById("avisoD4").style.display="table-row";
    document.getElementById("boton-volver").style.display="block";
    document.getElementById("tabla-general").style.display= "none";
    
};

const onClick5 = () =>{
    document.getElementById("datosD").style.display="table-row";
    document.getElementById("avisoD5").style.display="table-row";
    document.getElementById("boton-volver").style.display="block";
    document.getElementById("tabla-general").style.display= "none";

};
//Sacado de internet
const agrandarFoto = (foto) => {
  const modal = document.getElementById("modal-foto");
  const imagenAmpliada = document.getElementById("imagen-ampliada");
  imagenAmpliada.src = foto.src;
  modal.style.display = "flex";
};

const cerrarFoto = () => {
  document.getElementById("modal-foto").style.display = "none";
};


document.getElementById("aviso1").addEventListener("click", onClick1);
document.getElementById("aviso2").addEventListener("click", onClick2);
document.getElementById("aviso3").addEventListener("click", onClick3)
document.getElementById("aviso4").addEventListener("click", onClick4);
document.getElementById("aviso5").addEventListener("click", onClick5);