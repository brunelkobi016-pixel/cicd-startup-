from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://startup:startup123@db:5432/startupdb'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Startup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    secteur = db.Column(db.String(100), nullable=False)
    ville = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenue sur la plateforme StartupCI",
        "status": "running",
        "version": "2.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/init-db')
def init_db():
    db.create_all()
    if Startup.query.count() == 0:
        startups = [
            Startup(nom="WaxTech", secteur="Fintech", ville="Dakar"),
            Startup(nom="AgriSen", secteur="AgriTech", ville="Thiès"),
            Startup(nom="SantéPlus", secteur="HealthTech", ville="Saint-Louis"),
        ]
        db.session.add_all(startups)
        db.session.commit()
    return jsonify({"message": "Base de données initialisée !"})

@app.route('/startups')
def get_startups():
    startups = Startup.query.all()
    return jsonify([{
        "id": s.id,
        "nom": s.nom,
        "secteur": s.secteur,
        "ville": s.ville
    } for s in startups])

@app.route('/dashboard')
def dashboard():
    startups = Startup.query.all()
    return render_template('index.html', startups=startups)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)