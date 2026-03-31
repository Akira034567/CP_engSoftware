"""
Modelo de Usuário.
Suporta dois papéis: 'admin' (gerencia espaços) e 'student' (reserva espaços).
Implementa Flask-Login para autenticação (RNF03).
"""

from datetime import datetime, timezone, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models import db


class User(UserMixin, db.Model):
    """Representa um usuário do sistema (admin ou estudante)."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'admin' ou 'student'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-3))))

    # Relacionamentos
    reservations = db.relationship('Reservation', backref='user', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')

    def set_password(self, password):
        """Gera hash seguro da senha (RNF03)."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica a senha contra o hash armazenado."""
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        """Verifica se o usuário é administrador."""
        return self.role == 'admin'

    @property
    def unread_notifications_count(self):
        """Retorna quantidade de notificações não lidas."""
        return self.notifications.filter_by(is_read=False).count()

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
