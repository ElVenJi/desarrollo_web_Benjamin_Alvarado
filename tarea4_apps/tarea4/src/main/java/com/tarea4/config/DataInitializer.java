package com.tarea4.config;

import com.tarea4.models.AvisoAdopcion;
import com.tarea4.models.AvisoAdopcionRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import java.time.LocalDateTime;

@Component // ¡Importante! Para que Spring lo detecte
public class DataInitializer implements CommandLineRunner {

    private final AvisoAdopcionRepository avisoRepository;

    public DataInitializer(AvisoAdopcionRepository avisoRepository) {
        this.avisoRepository = avisoRepository;
    }
    
    @Override
    public void run(String... args) throws Exception {
        
        if (avisoRepository.count() == 0) {
            AvisoAdopcion aviso1 = new AvisoAdopcion();
            aviso1.setFecha_publicacion(LocalDateTime.of(2025, 6, 2, 12, 0));
            aviso1.setSector("Beauchef 859, terraza");
            aviso1.setTipo("gato");
            aviso1.setCantidad(1);
            aviso1.setEdad(2);
            aviso1.setUnidad_medida_edad("meses");
            aviso1.setComuna("Santiago");

            AvisoAdopcion aviso2 = new AvisoAdopcion();
            aviso2.setFecha_publicacion(LocalDateTime.of(2025, 5, 28, 10, 0));
            aviso2.setSector("Plaza Maipú");
            aviso2.setTipo("perro");
            aviso2.setCantidad(3);
            aviso2.setEdad(2);
            aviso2.setUnidad_medida_edad("meses");
            aviso2.setComuna("Santiago");
            
            AvisoAdopcion aviso3 = new AvisoAdopcion();
            aviso3.setFecha_publicacion(LocalDateTime.of(2025, 5, 20, 15, 0));
            aviso3.setSector("Lagunas");
            aviso3.setTipo("perro");
            aviso3.setCantidad(2);
            aviso3.setEdad(1);
            aviso3.setUnidad_medida_edad("años");
            aviso3.setComuna("Los Lagos");

            AvisoAdopcion aviso4 = new AvisoAdopcion();
            aviso4.setFecha_publicacion(LocalDateTime.of(2025, 6, 1, 8, 0));
            aviso4.setSector("Un árbol");
            aviso4.setTipo("gato");
            aviso4.setCantidad(4);
            aviso4.setEdad(3);
            aviso4.setUnidad_medida_edad("meses");
            aviso4.setComuna("Araucanía");

            AvisoAdopcion aviso5 = new AvisoAdopcion();
            aviso5.setFecha_publicacion(LocalDateTime.of(2025, 4, 15, 18, 0));
            aviso5.setSector("Cerro San Cristóbal");
            aviso5.setTipo("perro");
            aviso5.setCantidad(1);
            aviso5.setEdad(5);
            aviso5.setUnidad_medida_edad("años");
            aviso5.setComuna("Santiago");

            avisoRepository.save(aviso1);
            avisoRepository.save(aviso2);
            avisoRepository.save(aviso3);
            avisoRepository.save(aviso4);
            avisoRepository.save(aviso5);

        }
    }
}