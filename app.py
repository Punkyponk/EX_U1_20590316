from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://samvela_9quo_user:CeSAu0fQvU4hhgEGvM8FF29KfH0CMg2f@dpg-cv33matsvqrc739abqc0-a.oregon-postgres.render.com/samvela_9quo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definición del modelo de la tabla 'categories'
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"

# Definición del modelo de la tabla 'posts'
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref='posts')

    def __repr__(self):
        return f"<Post {self.title}>"

# Función para crear datos de prueba
def create_data():
    # Verificar si la categoría con ID 2 existe, si no existe, crearla
    category = Category.query.get(2)
    if category is None:
        print("La categoría con ID 2 no existe. Creándola...")
        category = Category(id=2, name="Cryptocurrency")
        db.session.add(category)
        db.session.commit()
    
    # Ahora insertar el post con category_id=2
    post = Post(
        title="Bitcoin alcanza su máximo histórico en 2023",
        content="El Bitcoin ha superado nuevamente las expectativas al alcanzar un nuevo máximo histórico de $45,000 este mes, impulsado por la adopción masiva de criptomonedas...",
        category_id=2
    )
    db.session.add(post)
    db.session.commit()
    print("Post creado exitosamente.")

# Ruta para retornar "Hola Mundo"
@app.route('/')
def hola_mundo():
    return "Hola Mundo"

# Ejecutar la función cuando se corra el script
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear todas las tablas si no existen
        create_data()  # Crear los datos de prueba
    app.run(debug=True)
