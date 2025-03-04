from flask_sqlalchemy import SQLAlchemy

# Inicializamos SQLAlchemy
db = SQLAlchemy()

# Definir la tabla `Category`
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    # Relación con la tabla `Post` (uno a muchos)
    posts = db.relationship('Post', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

# Definir la tabla `Post`
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    
    def __repr__(self):
        return f'<Post {self.title}>'
