function load() {
    try {
        for (let i = 0; i < document.getElementsByName("div-agregado").length; i++) {
            const element = document.getElementsByName("div-agregado")[i];
            element.classList.remove("claseParaProbar");
        }
        //document.getElementsByName("div-agregado").classList.remove("claseParaProbar");
    
        document.getElementById("estilo2").classList.add("estilo");
        document.getElementById("estilo1").classList.remove("estilo");
        document.getElementById("estilo3").classList.remove("estilo");
    
    } catch (error) {
        
    }
    ocultarBusqueda()
}

function agregarDiv(element) {
    console.log(element);
    element.children[1].classList.toggle("claseParaProbar");
}


function publicacion(){
    document.getElementById("estilo2").classList.add("estilo");
    document.getElementById("estilo1").classList.remove("estilo");
    document.getElementById("estilo3").classList.remove("estilo");
    document.getElementById("icono-subir-foto").classList.remove("estilo");

    ocultarBusqueda();

}

function mensaje(){
    document.getElementById("estilo2").classList.remove("estilo");
    document.getElementById("estilo1").classList.remove("estilo");
    document.getElementById("estilo3").classList.add("estilo");
    document.getElementById("icono-subir-foto").classList.remove("estilo");

    ocultarBusqueda();

}

function buscar(){
    document.getElementById("estilo2").classList.remove("estilo");
    document.getElementById("estilo1").classList.add("estilo");
    document.getElementById("estilo3").classList.remove("estilo");
    document.getElementById("icono-subir-foto").classList.remove("estilo");

    mostrarBusqueda();
}

function lineaFoto(){
    document.getElementById("icono-subir-foto").classList.add("estilo");
    document.getElementById("estilo2").classList.remove("estilo");
    document.getElementById("estilo1").classList.remove("estilo");
    document.getElementById("estilo3").classList.remove("estilo");

    ocultarMains();
    ocultarNavegador();
    ocultarBusqueda();
}

function mostrarSubirPublicacion() {
    none
}

function ocultarMains() {
    for (let i = 0; i < document.getElementsByClassName("contenedor-main").length; i++) {
        const element = document.getElementsByClassName("contenedor-main")[i];
        element.style.display = 'none';
    }
}

function ocultarBusqueda(){
    const element = document.getElementsByClassName("nav-bar");
    element[0].style.display = 'none';
}

function mostrarBusqueda(){
    const element = document.getElementsByClassName("nav-bar")[0];
    element.style.display = 'block';
}

function ocultarNavegador() {
    const navegador = document.getElementsByClassName("header");
    navegador[0].style.display = 'none';

    const invisible = document.getElementsByClassName("invisible");
    invisible[0].style.display = 'none';
    
}

function mostrarMains() {
    for (let i = 0; i < document.getElementsByClassName("contenedor-main").length; i++) {
        const element = document.getElementsByClassName("contenedor-main")[i];
        element.style.display = 'block';
    }
}

function favorito(element){
    //document.getElementById("favorito").classList.add("borde");
    element.children[0].classList.toggle("borde");
}



