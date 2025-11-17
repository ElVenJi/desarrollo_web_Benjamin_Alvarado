package com.tarea4.controllers; 

import com.tarea4.services.NotaService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class ApiController {

    private final NotaService notaService;

    public ApiController(NotaService notaService) {
        this.notaService = notaService;
    }

    @PostMapping("/api/avisos/{avisoId}/evaluar")
    public ResponseEntity<?> evaluarAviso(
            @PathVariable("avisoId") Long avisoId,
            @RequestParam("nota") Integer nota) {
        
        try {
            String nuevoPromedio = notaService.agregarNota(avisoId, nota);

            return ResponseEntity.ok(Map.of("nuevoPromedio", nuevoPromedio));

        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
}