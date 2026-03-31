"""
Sistema de Reserva de Espaços de Estudo
========================================
Ponto de entrada da aplicação Flask.
Inicializa o banco de dados, registra blueprints e configura serviços.

Uso:
    python app.py

Acesso padrão:
    - Admin: admin / admin123
    - URL: http://localhost:5000
"""

import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager

from config import Config
from models import db
from models.user import User
from models.space import Space
from models.reservation import Reservation
from models.notification import Notification

# Importa blueprints
from routes.auth import auth_bp
from routes.spaces import spaces_bp
from routes.reservations import reservations_bp
from routes.notifications import notifications_bp
from routes.admin import admin_bp


def create_app():
    """
    Factory function para criar a aplicação Flask.

    Returns:
        Instância configurada do Flask.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Garante que o diretório instance existe
    os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

    # ---- Inicializa extensões ----
    db.init_app(app)

    # Flask-Login (RNF03)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ---- Registra Blueprints ----
    app.register_blueprint(auth_bp)
    app.register_blueprint(spaces_bp)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(admin_bp)

    # ---- Rota raiz ----
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # ---- Cria tabelas e dados iniciais ----
    with app.app_context():
        db.create_all()
        _seed_initial_data()

    # ---- Inicializa scheduler (RF10) ----
    from services.scheduler_service import init_scheduler
    init_scheduler(app)

    return app


def _seed_initial_data():
    """
    Insere dados iniciais no banco se ele estiver vazio.
    Cria um admin padrão e alguns espaços de exemplo.
    """
    # Cria admin padrão se não existir
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@studyspace.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)

    # Cria espaços de exemplo se não existirem
    if Space.query.count() == 0:
        spaces = [
            Space(
                name='Sala 301',
                description='Sala de estudo com quadro branco e ar-condicionado',
                capacity=6,
                location='3º Andar, Unidade 2',
                status='available'
            ),
            Space(
                name='Sala 302',
                description='Sala silenciosa para estudo individual',
                capacity=2,
                location='3º Andar, Unidade 2',
                status='available'
            ),
            Space(
                name='Sala 303',
                description='Sala de estudos em grupo com projetor',
                capacity=10,
                location='3º Andar, Unidade 2',
                status='available'
            ),
            Space(
                name='Laboratório 701',
                description='Laboratório de informática com 20 computadores',
                capacity=20,
                location='7º Andar, Unidade 1',
                status='available'
            ),
            Space(
                name='Sala Bosch',
                description='Sala de inovação patrocinada pela Bosch com recursos multimídia',
                capacity=15,
                location='Térreo, Unidade 1',
                status='available'
            ),
            Space(
                name='Auditório Teatro',
                description='Auditório para apresentações e seminários',
                capacity=50,
                location='8º Andar, Unidade 1',
                status='available'
            ),
        ]
        db.session.add_all(spaces)

    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    # Roda em modo debug para desenvolvimento
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
