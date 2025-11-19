from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
from datetime import datetime

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Region(Base):
    __tablename__ = "region"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)

    comunas = relationship("Comuna", back_populates="region", cascade="all, delete-orphan")

class Comuna(Base):
    __tablename__ = "comuna"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    region = relationship("Region", back_populates="comunas")
    avisos = relationship("AvisoAdopcion", back_populates="comuna", cascade="all, delete-orphan")

class AvisoAdopcion(Base):
    __tablename__ = "aviso_adopcion"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(DateTime, nullable=False)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100), nullable=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=True)
    tipo = Column(String(5), nullable=False)
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_medida = Column(String(8), nullable=False)
    fecha_entrega = Column(DateTime, nullable=False)
    descripcion = Column(String(500), nullable=True)

    fotos = relationship("Foto", back_populates="aviso", cascade="all, delete-orphan")
    comuna = relationship("Comuna", back_populates="avisos")
    contactar_por = relationship("ContactarPor", back_populates="aviso", cascade="all, delete-orphan")
    comentario = relationship("Comentario", back_populates="aviso", cascade="all, delete-orphan")

class Foto(Base):
    __tablename__ = "foto"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(BigInteger, ForeignKey('aviso_adopcion.id'))

    aviso = relationship("AvisoAdopcion", back_populates="fotos")

class ContactarPor(Base):
    __tablename__ = "contactar_por"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(10), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(BigInteger, ForeignKey('aviso_adopcion.id'))

    aviso = relationship("AvisoAdopcion", back_populates="contactar_por")

class Comentario(Base):
    __tablename__ = "comentario"
    id = Column(Integer, primary_key = True, autoincrement= True)
    nombre = Column(String(80), nullable=False)
    texto = Column(String(300), nullable= False)
    fecha = Column(DateTime, nullable=False, default = datetime.now)
    aviso_id = Column(BigInteger, ForeignKey('aviso_adopcion.id'))

    aviso = relationship("AvisoAdopcion", back_populates="comentario")


def crear_tablas():
    Base.metadata.create_all(engine)

def crear_aviso(datos):
    session = SessionLocal()
    nuevo_aviso = AvisoAdopcion(
        comuna_id=datos["comuna_id"],
        sector=datos["sector"],
        nombre=datos["nombre"],
        email=datos["email"],
        celular=datos["celular"],
        tipo=datos["tipo"],
        cantidad=datos["cantidad"],
        edad=datos["edad"],
        unidad_medida=datos["unidad_medida"],
        fecha_entrega=datos["fecha_entrega"],
        descripcion=datos["descripcion"],
        fecha_ingreso=datetime.now()
    )
    nuevo_aviso.fotos = datos["fotos"]
    session.add(nuevo_aviso)
    session.commit()
    session.close()

#Arreglado por internet
def obtener_avisoscL(limite):
    session = SessionLocal()
    avisos = (
        session.query(AvisoAdopcion)
        .options(
            joinedload(AvisoAdopcion.fotos),
            joinedload(AvisoAdopcion.comuna).joinedload(Comuna.region) 
        )
        .order_by(AvisoAdopcion.fecha_ingreso.desc())
        .limit(limite)
        .all()
    )
    session.close()
    return avisos


def obtener_avisos():
    session = SessionLocal()
    avisos = (
        session.query(AvisoAdopcion)
        .options(
            joinedload(AvisoAdopcion.fotos),
            joinedload(AvisoAdopcion.comuna).joinedload(Comuna.region)
        )
        .order_by(AvisoAdopcion.fecha_ingreso.desc())
        .all()
    )
    session.close()
    return avisos


def crear_avisos_prueba():
    session = SessionLocal()
    comunas = session.query(Comuna).all()
    comuna1 = comunas[56]

    aviso1 = AvisoAdopcion(
        comuna_id=comuna1.id,
        sector="MI casa",
        nombre="Pedro",
        email="pedro@gmail.com",
        celular="56999999999",
        tipo="gato",
        cantidad=2,
        edad=10,
        unidad_medida="años",
        fecha_entrega=datetime.fromisoformat("2025-10-11"),
        descripcion=None,
        fecha_ingreso=datetime.fromisoformat("2025-10-10"),
    )
    aviso1.fotos = [Foto(ruta_archivo="static/uploads/gatinhos.jpg", nombre_archivo="gatinhos.jpg")]
    aviso1.contactar_por = [ContactarPor(nombre = "WhatsApp", identificador = "56999999999")]
    session.add(aviso1)

    comuna2 = comunas[11]

    aviso2 = AvisoAdopcion(
        comuna_id=comuna2.id,
        sector="Cancha de futbol",
        nombre="Alexis",
        email="Sanchez@gmail.com",
        celular="56939999999",
        tipo="perro",
        cantidad=10,
        edad=10,
        unidad_medida="dias",
        fecha_entrega=datetime.fromisoformat("2025-10-09"),
        descripcion=None,
        fecha_ingreso=datetime.fromisoformat("2025-10-04"),
    )
    aviso2.fotos = [Foto(ruta_archivo="static/uploads/dogs.jpg", nombre_archivo="dogs.jpg")]
    aviso2.contactar_por = [ContactarPor(nombre = "Instagram", identificador = "@alexissanchez7")]
    session.add(aviso2)

    comuna3 = comunas[83]

    aviso3 = AvisoAdopcion(
        comuna_id=comuna3.id,
        nombre="Rigby",
        email="rigby@gmail.com",
        celular="56900001394",
        tipo="perro",
        cantidad=1,
        edad=5,
        unidad_medida="años",
        fecha_entrega=datetime.fromisoformat("2025-10-15"),
        descripcion=None,
        fecha_ingreso=datetime.fromisoformat("2025-10-09"),
    )
    aviso3.fotos = [Foto(ruta_archivo="static/uploads/rigby.jpg", nombre_archivo="rigby.jpg"), Foto(ruta_archivo="static/uploads/rigby2.jpg", nombre_archivo="rigby2.jpg")]
    aviso3.contactar_por = [ContactarPor(nombre = "Instagram", identificador = "@rigbythecat")]
    session.add(aviso3)

    comuna4 = comunas[45]

    aviso4 = AvisoAdopcion(
        comuna_id=comuna4.id,
        nombre="Maria",
        email="maria@gmail.com",
        celular="569876578648",
        tipo="perro",
        cantidad=1,
        edad=5,
        unidad_medida="años",
        fecha_entrega=datetime.fromisoformat("2025-09-25"),
        descripcion=None,
        fecha_ingreso=datetime.fromisoformat("2025-08-09"),
    )
    aviso4.fotos = [Foto(ruta_archivo="static/uploads/dog.jpg", nombre_archivo="dog.jpg")]
    aviso4.contactar_por = [ContactarPor(nombre = "Correo", identificador = "maria@gmail.com")]
    session.add(aviso4)

    comuna5 = comunas[85]

    aviso5 = AvisoAdopcion(
        comuna_id=comuna5.id,
        nombre="Yeyo",
        email="yeyo@gmail.com",
        celular="56902001594",
        tipo="gato",
        cantidad=5,
        edad=3,
        unidad_medida="meses",
        fecha_entrega=datetime.fromisoformat("2025-08-05"),
        descripcion=None,
        fecha_ingreso=datetime.fromisoformat("2025-04-16"),
    )
    aviso5.fotos = [Foto(ruta_archivo="static/uploads/5cats.jpg", nombre_archivo="5cats.jpg")]
    aviso5.contactar_por = [ContactarPor(nombre = "Correo", identificador = "yeyo@gmail.com")]    
    session.add(aviso5)

    session.commit()
    session.close()

def cargar_region_comuna(sql_file="database/region-comuna.sql"):
    """Carga las regiones y comunas desde un archivo SQL."""
    conn = engine.raw_connection()  # no usar 'with'
    cursor = conn.cursor()
    try:
        with open(sql_file, "r", encoding="utf-8") as f:
            sql = f.read()
            for statement in sql.split(";"):
                if statement.strip():
                    cursor.execute(statement)
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def reset_database():
    print("En proceso")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    cargar_region_comuna()
    crear_avisos_prueba()
