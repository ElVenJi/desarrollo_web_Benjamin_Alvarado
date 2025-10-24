from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from sqlalchemy import func, extract
from database import db
from datetime import datetime, timedelta 
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)

app.secret_key = "s3cr3t_k3y"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "webp"}

db.reset_database()


def allowed_file(filename):
    """Verifica si la extensión del archivo está permitida."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@app.route("/", methods=["GET"])
def index():
    avisos = db.obtener_avisoscL(5)
    return render_template("Portada.html", avisos = avisos)

@app.route("/Estadisticas", methods=["GET"])
def estadisticas():
    return render_template("Estadisticas.html")


@app.route("/Aviso", methods=["GET", "POST"])
def aviso():
    if request.method == "POST":
        
        datos = request.form
        archivos = request.files
        
        try:            
            fotos = archivos.getlist("fotos[]")
            archivos_validos = [f for f in fotos if f.filename and allowed_file(f.filename)]

            if not (1 <= len(archivos_validos) <= 5):
                 raise ValueError("Cantidad de fotos no válida (Server-Side)")
                 
            comuna_id = int(datos.get("seleccionar-comuna"))
            cantidad = int(datos.get("cantidad"))
            edad = int(datos.get("edad"))
            fecha_entrega = datetime.fromisoformat(datos.get("fecha-disponible"))
            
            datos_aviso = {
                "comuna_id": comuna_id,
                "sector": datos.get("sector"),
                "nombre": datos.get("Nombre"),
                "email": datos.get("email"),
                "celular": datos.get("telefono"),
                "tipo": datos.get("seleccionar-tipo").lower(), 
                "cantidad": cantidad,
                "edad": edad,
                "unidad_medida": datos.get("seleccionar-unidad-tiempo"), 
                "fecha_ingreso": datetime.now(), 
                "fecha_entrega": fecha_entrega,
                "descripcion": datos.get("descripción"),
            }

        except Exception as e:
            flash("Error de datos. Revisar el formulario.", "error")
            return render_template("Aviso.html")
            
        
        session = db.SessionLocal()
        
        try:
            nuevo_aviso = db.AvisoAdopcion(**datos_aviso)
            session.add(nuevo_aviso)
            session.flush()

            for f in archivos_validos:
                filename = secure_filename(f.filename)
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{filename}" 
                path_completo = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                ruta_relativa_static = os.path.join('uploads', unique_filename)
                
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                        
                f.save(path_completo) 
                
                nueva_foto = db.Foto(
                    ruta_archivo=ruta_relativa_static,
                    nombre_archivo=unique_filename,
                    actividad_id=nuevo_aviso.id 
                )
                session.add(nueva_foto)
                
            tipocontacto = datos.get("seleccionar-medio")
            contactofinal = datos.get("contacto-final")

            if tipocontacto and contactofinal:
                nuevo_contacto = db.ContactarPor(
                    nombre=tipocontacto,
                    identificador=contactofinal,
                    actividad_id=nuevo_aviso.id 
                )
                session.add(nuevo_contacto)

            session.commit() 
            session.close()
            
            flash("Hemos recibido la información de adopción, muchas gracias y suerte!", "success")
            return redirect(url_for("index"))

        except Exception as e:
            session.rollback()
            session.close()
            flash("Error al guardar en la base de datos. Por favor, inténtelo de nuevo.", "error")
            return render_template("Aviso.html")


    return render_template("Aviso.html")


@app.route("/Listado", methods =["GET"])
def listado():
    page = request.args.get("page", 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    session = db.SessionLocal()
    total_avisos = session.query(db.AvisoAdopcion).count()
    avisos = (
        session.query(db.AvisoAdopcion)
        .options(
            db.joinedload(db.AvisoAdopcion.fotos),
            db.joinedload(db.AvisoAdopcion.comuna).joinedload(db.Comuna.region),
            db.joinedload(db.AvisoAdopcion.contactar_por) 
        )
        .order_by(db.AvisoAdopcion.fecha_ingreso.desc())
        .limit(per_page)
        .offset(offset)
        .all()
    )
    total_pages = (total_avisos + per_page - 1) // per_page
    session.close()
    return render_template("Listado.html", avisos=avisos, page=page, total_pages=total_pages)


@app.route("/<content>")
def aux(content):
    if content.lower() in ["estadisticas", "aviso", "listado"]:
        return redirect(url_for(content.lower()))
    return redirect(url_for("index"))

@app.route("/Aviso/<int:aviso_id>", methods =["GET"])
def detalle_aviso(aviso_id):
    session = db.SessionLocal()
    aviso = (
        session.query(db.AvisoAdopcion)
        .options(
            db.joinedload(db.AvisoAdopcion.fotos),
            db.joinedload(db.AvisoAdopcion.comuna).joinedload(db.Comuna.region),
            db.joinedload(db.AvisoAdopcion.contactar_por)
        )
        .get(aviso_id)
    )
    session.close()
    
    if aviso is None:
        flash("Aviso no encontrado.", "error")
        return redirect(url_for("listado"))
        
    return render_template("Detalle.html", aviso=aviso)

@app.route("/Aviso/<int:aviso_id>/comentarios", methods=["GET", "POST"])
def comentarios(aviso_id):
    try:
        session = db.SessionLocal()
        if request.method == "GET":
            comentarios_db = (
                session.query(db.Comentario)
                .filter(db.Comentario.aviso_id == aviso_id)
                .order_by(db.Comentario.fecha.asc())
                .all()
            )
            comentarios = []
            for comentario in comentarios_db:
                comentarios.append({
                    "id": comentario.id,
                    "nombre": comentario.nombre,
                    "texto": comentario.texto,
                    "fecha": comentario.fecha.strftime('%d-%m-%Y %H:%M')
                })
            session.close()
            return jsonify(comentarios)
        
        elif request.method == "POST": 
            datos = request.json
            nombre = datos.get("nombre")
            texto = datos.get("texto")

            errores = []
            if not nombre or len(nombre) < 3 or len(nombre) >80:
                errores.append("Nombre inválido (3-80 carácteres)")
            if not texto or len(texto) < 5 or len(texto) > 300:
                errores.append("Texto inválido (5-300 caráctares)")
            if errores:
                return jsonify({"errores": errores})
            
            aviso = session.query(db.AvisoAdopcion).get(aviso_id)
            if not aviso:
                return jsonify({"error": "No hay aviso"})
            
            comentario = db.Comentario(nombre = nombre, texto = texto, aviso_id = aviso_id)

            session.add(comentario)
            session.commit()
            session.refresh(comentario)
            comentario_final = ({
                    "id": comentario.id,
                    "nombre": comentario.nombre,
                    "texto": comentario.texto,
                    "fecha": comentario.fecha.strftime('%d-%m-%Y %H:%M')
                })
            session.close()
            return jsonify(comentario_final)       
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        session.close()
        return jsonify({"error": "Error interno del servidor"})
    

@app.route("/Estadisticas/grafico1")
def grafico1():
    session = db.SessionLocal()
    try:
        datos = (
            session.query(
                func.date(db.AvisoAdopcion.fecha_ingreso).label('fecha'), #
                func.count(db.AvisoAdopcion.id).label('cantidad')
            )
            .group_by(func.date(db.AvisoAdopcion.fecha_ingreso))
            .order_by(func.date(db.AvisoAdopcion.fecha_ingreso))
            .all()
        )
        categorias = [d.fecha.strftime('%d-%m-%Y') for d in datos]
        cantidades = [d.cantidad for d in datos]

        return jsonify({
            "categorias": categorias,
            "cantidades": cantidades
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error interno del servidor"})
    finally:
        session.close()

@app.route("/Estadisticas/grafico2")
def grafico2():
    session = db.SessionLocal()
    try:
        datos = (
            session.query(
                db.AvisoAdopcion.tipo, 
                func.count(db.AvisoAdopcion.id).label('total')
            )
            .group_by(db.AvisoAdopcion.tipo)
            .all()
        )
        datos_formateados = []
        for d in datos:
            datos_formateados.append({
                "name": d.tipo.capitalize(),
                "y": d.total
            })
        return jsonify(datos_formateados)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error interno del servidor"})
    finally:
        session.close()



@app.route("/Estadisticas/grafico3")
def grafico3():
    session = db.SessionLocal()
    try:
        datos = (
            session.query(
                extract('month', db.AvisoAdopcion.fecha_ingreso).label('mes_numero'),
                db.AvisoAdopcion.tipo,
                func.count(db.AvisoAdopcion.id).label('cantidad')
            )
            .group_by(extract('month', db.AvisoAdopcion.fecha_ingreso), db.AvisoAdopcion.tipo)
            .order_by(extract('month', db.AvisoAdopcion.fecha_ingreso))
            .all()
        )
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        gatos = [0]*12
        perros = [0]*12
        for d in datos:            
            if d.tipo == 'gato':
                gatos[int(d.mes_numero) - 1] = d.cantidad
            elif d.tipo == 'perro':
                perros[int(d.mes_numero) - 1] = d.cantidad
        return jsonify({
            "categorias": meses,
            "gatos": gatos,
            "perros": perros
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error interno del servidor"})
    finally:
        session.close()

if __name__ == "__main__":  
    app.run(debug=True)