from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql

# Inisialisasi Flask app dan SQLAlchemy
app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_sharing_vision_amirul'  # Ganti dengan URI database Anda
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model untuk Artikel
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(10), nullable=False)

# Validasi artikel
def validate_article(data):
    if len(data['title']) < 20:
        return False
    if len(data['content']) < 200:
        return False
    if len(data['category']) < 3:
        return False
    if data['status'] not in ["publish", "draft", "thrash"]:
        return False
    return True

# Route untuk membuat artikel
@app.route('/article/', methods=['POST'])
def create_article():
    data = request.json
    if validate_article(data):
        new_article = Article(
            title=data['title'],
            content=data['content'],
            category=data['category'],
            status=data['status']
        )
        db.session.add(new_article)
        db.session.commit()
        return jsonify({"message": "Article created successfully"}), 201
    return jsonify({"error": "Validation failed"}), 400

# Route untuk mengambil beberapa artikel dengan limit dan offset
@app.route('/article/<int:limit>/<int:offset>', methods=['GET'])
def get_articles(limit, offset):
    articles = Article.query.limit(limit).offset(offset).all()
    return jsonify([{
        "title": article.title,
        "content": article.content,
        "category": article.category,
        "status": article.status
    } for article in articles]), 200

# Route untuk mengambil artikel berdasarkan ID
@app.route('/article/<int:id>', methods=['GET'])
def get_article(id):
    article = Article.query.get_or_404(id)
    return jsonify({
        "title": article.title,
        "content": article.content,
        "category": article.category,
        "status": article.status
    }), 200

# Route untuk memperbarui artikel berdasarkan ID
@app.route('/article/<int:id>', methods=['POST', 'PUT', 'PATCH'])
def update_article(id):
    article = Article.query.get_or_404(id)
    data = request.json
    if validate_article(data):
        article.title = data['title']
        article.content = data['content']
        article.category = data['category']
        article.status = data['status']
        db.session.commit()
        return jsonify({"message": "Article updated successfully"}), 200
    return jsonify({"error": "Validation failed"}), 400

# Route untuk menghapus artikel berdasarkan ID
@app.route('/article/<int:id>', methods=['POST', 'DELETE'])
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({"message": "Article deleted successfully"}), 200

# Route untuk menyajikan dashboard.html
@app.route('/dashboard')
def serve_dashboard():
    return send_from_directory('../frontend', 'dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
