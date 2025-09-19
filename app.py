from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos de base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    membresia_activa = db.Column(db.Boolean, default=False)
    fecha_membresia = db.Column(db.DateTime)
    recordatorios = db.relationship('Recordatorio', backref='user', lazy=True)

class Recordatorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_cumpleanos = db.Column(db.DateTime, nullable=False)
    anticipacion_dias = db.Column(db.Integer, default=3)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    tienda = db.Column(db.String(50), nullable=False)
    imagen_url = db.Column(db.String(200))
    url_producto = db.Column(db.String(200))

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/membresias')
def membresias():
    return render_template('membresias.html')

@app.route('/tienda')
def tienda():
    productos = Producto.query.all()
    return render_template('tienda.html', productos=productos)

@app.route('/recordatorios')
def recordatorios():
    return render_template('recordatorios.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Agregar productos de ejemplo si no existen
        if not Producto.query.first():
            productos_ejemplo = [
                Producto(
                    nombre="Tarjeta de Regalo Amazon",
                    descripcion="Tarjeta de regalo electrónica para Amazon",
                    precio=500.00,
                    tienda="Amazon",
                    imagen_url="/static/images/amazon-giftcard.jpg",
                    url_producto="https://www.amazon.com.mx"
                ),
                Producto(
                    nombre="Juego de Vino",
                    descripcion="Elegante juego de vino tinto y blanco",
                    precio=850.00,
                    tienda="Liverpool",
                    imagen_url="/static/images/vino-set.jpg",
                    url_producto="https://www.liverpool.com.mx"
                ),
                Producto(
                    nombre="Globo Personalizado",
                    descripcion="Globo con mensaje personalizado para cumpleaños",
                    precio=250.00,
                    tienda="Mercado Libre",
                    imagen_url="/static/images/globo.jpg",
                    url_producto="https://www.mercadolibre.com.mx"
                )
            ]
            
            for producto in productos_ejemplo:
                db.session.add(producto)
            db.session.commit()
    
    # CAMBIA ESTA LÍNEA:
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)