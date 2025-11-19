
const agregarGrafico1 = async () => {
  try {
        const response = await fetch("/Estadisticas/grafico1");
        
        if (!response.ok) {
            throw new Error("Error del servidor al obtener datos");
        }
        const datos = await response.json();
        Highcharts.chart("container", {
    chart: {
        type: "line"
    },
    title: {
        text: "Cantidad de Avisos de Adopción por Día"
    },
    xAxis: {
        categories: datos.categorias
    },
    yAxis: {
        title: {
            text: "Cantidad de Avisos"
        }
    },
    series: [{
        name: "Avisos de Adopción",
        data: datos.cantidades
    }]
});
  }catch (error){
    console.error("Error al crear el gráfico de líneas:", error);
  }
};

const agregarGrafico2 = async () => {
    try { 
        const response = await fetch("/Estadisticas/grafico2");
        if(!response.ok){
            throw new Error("Error del servidor al obtener datos");
        };
        const datos = await response.json();
        Highcharts.chart("container-torta", {
    chart: {
        type: "pie"
    },
    title: {
        text: "Total de Avisos de Adopción por Tipo de Mascota"
    },
    series: [{
        name: "Mascotas",
        colorByPoint: true,
        data: datos
    }]
});
    }catch (error){
        console.error("Error al crear el gráfico de torta", error);
    }
};



const agregarGrafico3 = async () => {
    try {
        const response = await fetch("/Estadisticas/grafico3");
        if (!response.ok){
            throw new Error("Error del servidor al obtener datos");
        };
        const datos = await response.json();

        Highcharts.chart("container-barra", {
    chart: {
        type: "column"
    },
    title: {
        text: "Avisos de Adopción por Mes"
    },
    xAxis: {
        categories: datos.categorias
    },
    yAxis: {
        title: {
            text: "Cantidad de Avisos"
        }
    },
    series: [{
        name: "Gatos",
        data: datos.gatos
    }, {
        name: "Perros",
        data: datos.perros
    }]
});

    }catch (error){
        console.error("Error al crear el gráfico de barras", error)
    }
};


document.addEventListener("DOMContentLoaded", () => {
    agregarGrafico1();
    agregarGrafico2();
    agregarGrafico3();
});
