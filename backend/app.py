from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql

# Initialize Flask app and SQLAlchemy
app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_sharing_vision_amirul'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model for Article
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)  # Default to current time
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Updated on modification

# Validate article
def validate_article(data):
    if len(data.get('title', '')) < 20:
        print(f"Validation failed: Title is too short. Title length: {len(data.get('title', ''))}")
        return False
    if len(data.get('content', '')) < 200:
        print(f"Validation failed: Content is too short. Content length: {len(data.get('content', ''))}")
        return False
    if len(data.get('category', '')) < 3:
        print(f"Validation failed: Category is too short. Category length: {len(data.get('category', ''))}")
        return False
    if data.get('status') not in ["publish", "draft", "trash"]:
        print(f"Validation failed: Invalid status. Status: {data.get('status')}")
        return False
    return True

# Route to create an article
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

# Route to get a paginated list of articles
@app.route('/article/', methods=['GET'])
def get_articles():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    articles = Article.query.limit(limit).offset(offset).all()
    return jsonify([{
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "category": article.category,
        "status": article.status,
        "created_date": article.created_date,
        "updated_date": article.updated_date
    } for article in articles]), 200

# Route to get an article by ID
@app.route('/article/<int:id>', methods=['GET'])
def get_article(id):
    article = Article.query.get_or_404(id)
    return jsonify({
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "category": article.category,
        "status": article.status,
        "created_date": article.created_date,
        "updated_date": article.updated_date
    }), 200

# Route to update an article by ID
@app.route('/article/<int:id>', methods=['PUT'])
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

# Route to delete an article by ID
@app.route('/article/<int:id>', methods=['DELETE'])
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({"message": "Article deleted successfully"}), 200

# Route to serve dashboard.html
@app.route('/dashboard')
def serve_dashboard():
    return send_from_directory('../frontend', 'dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
