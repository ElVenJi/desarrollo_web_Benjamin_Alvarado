package com.tarea4.services; 

import com.tarea4.models.AvisoAdopcion;
import com.tarea4.models.AvisoAdopcionRepository; 
import com.tarea4.models.Nota;
import com.tarea4.models.NotaRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;


@Service
public class NotaService {

    private final NotaRepository notaRepository;
    private final AvisoAdopcionRepository avisoRepository; 

    public NotaService(NotaRepository notaRepository, AvisoAdopcionRepository avisoRepository) {
        this.notaRepository = notaRepository;
        this.avisoRepository = avisoRepository;
    }

    @Transactional 
    public String agregarNota(Long avisoId, Integer valorNota) {
        
        if (avisoId == null || valorNota == null || valorNota < 1 || valorNota > 7) {
            throw new IllegalArgumentException("La nota debe estar entre 1 y 7.");
        }

        AvisoAdopcion aviso = avisoRepository.findById(avisoId).orElseThrow(() -> new RuntimeException("Aviso no encontrado con id: " + avisoId));

        Nota nuevaNota = new Nota(valorNota, aviso);
      
        aviso.getNotas().add(nuevaNota);
        
        notaRepository.save(nuevaNota);

        return aviso.getPromedioNotas();
    }
}