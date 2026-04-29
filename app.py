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

from views.routes.auth import auth_bp
from views.routes.spaces import spaces_bp
from views.routes.reservations import reservations_bp
from views.routes.notifications import notifications_bp
from views.routes.admin import admin_bp


def create_app():
    """Factory function para criar a aplicação Flask."""
    app = Flask(__name__, template_folder='views/templates', static_folder='views/static')
    app.config.from_object(Config)

    os.makedirs(os.path.join(app.root_path, 'data'), exist_ok=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(spaces_bp)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    with app.app_context():
        db.create_all()
        _seed_initial_data()

    from services.scheduler_service import init_scheduler
    init_scheduler(app)

    return app


def _seed_initial_data():
    """Insere dados iniciais no banco e sincroniza catálogo padrão."""
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@studyspace.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)

    spaces_catalog = _build_spaces_catalog()
    existing_by_name = {space.name: space for space in Space.query.all()}
    catalog_names = {item['name'] for item in spaces_catalog}

    for item in spaces_catalog:
        existing = existing_by_name.get(item['name'])
        if existing:
            existing.description = item['description']
            existing.capacity = item['capacity']
            existing.location = item['location']
            existing.status = 'available'
        else:
            db.session.add(Space(**item, status='available'))

    for old_space in Space.query.all():
        if old_space.name in catalog_names:
            continue
        if old_space.reservations.count() == 0:
            db.session.delete(old_space)
        else:
            old_space.status = 'maintenance'

    db.session.commit()


def _build_spaces_catalog():
    """Gera o catálogo oficial de laboratórios da Unidade 2."""
    catalog = []
    capacities_by_floor = {2: 30, 3: 32, 5: 26, 6: 40, 7: 28, 8: 28, 9: 36}

    for floor in [2, 3, 7, 8, 9]:
        for room in range(1, 5):
            number = f'{floor}0{room}'
            catalog.append({
                'name': f'Laboratório {number}',
                'description': (
                    'Laboratório de computação da Unidade 2 com perfil versátil para '
                    'programação, web, bancos de dados e atividades acadêmicas.'
                ),
                'capacity': capacities_by_floor[floor],
                'location': f'{floor}º Andar, Unidade 2',
            })

    catalog.extend([
        {
            'name': 'Laboratório 502 (Lab Gamer)',
            'description': (
                'Lab gamer com GPU dedicada para IA, machine learning, computação '
                'gráfica, renderização e jogos.'
            ),
            'capacity': capacities_by_floor[5],
            'location': '5º Andar, Unidade 2',
        },
        {
            'name': 'Laboratório 503 (Lab de MacBooks)',
            'description': (
                'Laboratório com equipamentos Apple para desenvolvimento iOS e mobile, '
                'além de uso geral de desenvolvimento.'
            ),
            'capacity': capacities_by_floor[5],
            'location': '5º Andar, Unidade 2',
        },
        {
            'name': 'Laboratório 603',
            'description': (
                'Laboratório amplo para turmas grandes, práticas em grupo, redes, '
                'infraestrutura e projetos de IoT.'
            ),
            'capacity': capacities_by_floor[6],
            'location': '6º Andar, Unidade 2',
        },
    ])

    return catalog


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
