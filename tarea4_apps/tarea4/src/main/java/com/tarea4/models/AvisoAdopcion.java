package com.tarea4.models;

import java.time.LocalDateTime; 
import java.util.List;
import java.util.ArrayList;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.SequenceGenerator; 
import jakarta.persistence.Table;
import jakarta.persistence.Transient;

@Entity
@Table(name = "aviso_adopcion") 
public class AvisoAdopcion {

    @Id
    @SequenceGenerator(
        name = "aviso_sequence",
        sequenceName = "aviso_sequence",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "aviso_sequence"
    )
    private Long id;

    private String sector;
    private String tipo; 
    private Integer cantidad;
    private Integer edad;
    private String unidad_medida_edad; 
    private LocalDateTime fecha_publicacion; 
    private String comuna;
    
    @OneToMany(mappedBy = "aviso", fetch = FetchType.LAZY)
    private List<Nota> notas = new ArrayList<>();

    public Long getId() { return id; }
    public String getComuna() { return comuna; }
    public LocalDateTime getFecha_publicacion() { return fecha_publicacion; }
    
    public String getCantidadTipoEdad() {
        return String.format("%d %s %d %s", 
            this.cantidad, this.tipo, this.edad, this.unidad_medida_edad);
    }

    public String getSector() {
        if (this.comuna != null) {
            return sector; 
        }
        return "-";
    }

    public String getNombreComuna() {
        if (this.comuna != null) {
            return this.comuna;
        }
        return "-";
    }

    public List<Nota> getNotas() { return this.notas;}

    @Transient
    public String getPromedioNotas() {
        if (this.notas == null || this.notas.isEmpty()) {
            return "-"; 
        }
        double sum = 0;
        for (Nota n : this.notas) {
            sum += n.getNota();
        }
        double promedio = sum / this.notas.size();
        return String.format("%.1f", promedio);
    } 

    public void setSector(String sector) { this.sector = sector; }

    public void setTipo(String tipo) { this.tipo = tipo; }

    public void setCantidad(Integer cantidad) { this.cantidad = cantidad; }

    public void setEdad(Integer edad) { this.edad = edad; }

    public void setUnidad_medida_edad(String unidad_medida_edad) { this.unidad_medida_edad = unidad_medida_edad; }

    public void setFecha_publicacion(LocalDateTime fecha_publicacion) { this.fecha_publicacion = fecha_publicacion; }

    public void setComuna(String comuna) { this.comuna = comuna; }
}