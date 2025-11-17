package com.tarea4.models; 
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

@Entity
@Table(name = "nota") 
public class Nota {

    @Id
    @SequenceGenerator(
        name = "nota_sequence",
        sequenceName = "nota_sequence",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "nota_sequence"
    )
    private Long id;

    @NotNull
    @Min(1) 
    @Max(7)
    private Integer nota;


    @NotNull
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "aviso_id") 
    private AvisoAdopcion aviso;


    public Nota() {
    }

    public Nota(Integer nota, AvisoAdopcion aviso) {
        this.nota = nota;
        this.aviso = aviso;
    }

    public Long getId() { return id; }

    public void setId(Long id) { this.id = id; }

    public Integer getNota() { return nota; }

    public void setNota(Integer nota) { this.nota = nota; }

    public AvisoAdopcion getAviso() { return aviso; }

    public void setAviso(AvisoAdopcion aviso) { this.aviso = aviso; }
}