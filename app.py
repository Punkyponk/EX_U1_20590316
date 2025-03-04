from flask import Flask, render_template, request, redirect, url_for
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

# Ruta para mostrar todos los posts
@app.route('/')
def index():
    posts = Post.query.all()  # Obtener todos los posts de la base de datos
    return render_template('index.html', posts=posts)

# Ruta para mostrar el formulario de creación de un post
@app.route('/add', methods=['GET'])
def add_post():
    categories = Category.query.all()  # Obtener todas las categorías
    return render_template('create_post.html', categories=categories)

# Ruta para manejar el formulario de creación de un post
@app.route('/add', methods=['POST'])
def add_post_submit():
    title = request.form['title']
    content = request.form['content']
    category_id = request.form['category_id']
    
    # Crear un nuevo post con los datos del formulario
    post = Post(title=title, content=content, category_id=category_id)
    db.session.add(post)
    db.session.commit()
    
    return redirect(url_for('index'))  # Redirigir al index después de crear el post

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

# Ejecutar la función cuando se corra el script
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear todas las tablas si no existen
        create_data()  # Crear los datos de prueba
    app.run(debug=True)
