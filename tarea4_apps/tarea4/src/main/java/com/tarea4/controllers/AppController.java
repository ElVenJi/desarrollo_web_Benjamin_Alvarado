package com.tarea4.controllers;

import com.tarea4.models.AvisoAdopcion;
import com.tarea4.models.AvisoAdopcionRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import java.util.List;

@Controller
public class AppController {

    private final AvisoAdopcionRepository avisoRepository;

   
    public AppController(AvisoAdopcionRepository avisoRepository) {
        this.avisoRepository = avisoRepository;
    }

    @GetMapping("/")
    public String paginaListado(Model model) {
        
        List<AvisoAdopcion> avisos = avisoRepository.findAll();

        model.addAttribute("data", avisos); 
        
        return "listado"; 
    }
}