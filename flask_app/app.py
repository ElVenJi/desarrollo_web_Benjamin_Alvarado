from flask import Flask, request, render_template, redirect, url_for, session
from database import db
from datetime import datetime
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)

app.secret_key = "s3cr3t_k3y"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "webp"}

db.reset_database()

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
        session = db.SessionLocal()
        datos = {
            "comuna_id": int(request.form["seleccionar-comuna"]),
            "sector": request.form["sector"],
            "nombre": request.form["Nombre"],
            "email": request.form["email"],
            "celular": request.form["telefono"],
            "tipo": request.form["seleccionar-tipo"],
            "cantidad": int(request.form["cantidad"]),
            "edad": int(request.form["edad"]),
            "unidad_medida": request.form["seleccionar-unidad-tiempo"],
            "fecha_entrega": datetime.fromisoformat(request.form["fecha-disponible"]),
            "descripcion": request.form["descripción"],
        }
        aviso = db.AvisoAdopcion(**datos)
        session.add(aviso)

        fotos_guardadas = []
        fotos = request.files.getlist("fotos[]")
        for f in fotos:
            if f.filename:
                filename = secure_filename(f.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                f.save(path)
                fotos_guardadas.append(db.Foto(ruta_archivo=path, nombre_archivo=filename))
        if fotos_guardadas:
            aviso_db = session.query(db.AvisoAdopcion).get(aviso.id)
            aviso_db.fotos.extend(fotos_guardadas)


        tipocontacto = request.form.get("seleccionar-medio")
        contactofinal = request.form.get("contacto-final")
        if tipocontacto and contactofinal:
            contacto = db.ContactarPor(nombre=tipocontacto, identificador=contactofinal)
            aviso_db.contactar_por.append(contacto)
        
        session.commit()
        session.close()
        return redirect(url_for("listado"))
    return render_template("Aviso.html")

@app.route("/Listado")
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
            db.joinedload(db.AvisoAdopcion.comuna).joinedload(db.Comuna.region)
        )
        .order_by(db.AvisoAdopcion.fecha_ingreso.desc())
        .limit(per_page)
        .offset(offset)
        .all()
    )
    total_pages = (total_avisos + per_page - 1) // per_page
    session.close()
    return render_template("Listado.html", avisos=avisos, page=page, total_pages=total_pages)


Aux = ["a","Estadisticas", "Aviso", "Listado"]

@app.route("/<content>")
def aux(content):
    for i in Aux:
        if content == i:
            return  redirect(url_for((f"{content}")))
    return  redirect(url_for(("index")))


@app.route("/Aviso/<int:aviso_id>")
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
    return render_template("Detalle.html", aviso=aviso)

if __name__ == "__main__":  
    app.run()
