"""
Modelo de Espaço de Estudo.
Representa os espaços físicos que podem ser reservados (RF01, RF08).
"""

from datetime import datetime, timezone, timedelta
from models import db


class Space(db.Model):
    """Representa um espaço de estudo disponível para reserva."""

    __tablename__ = 'spaces'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    capacity = db.Column(db.Integer, nullable=False, default=1)
    location = db.Column(db.String(200), default='')
    status = db.Column(db.String(20), nullable=False, default='available')  # 'available' ou 'maintenance'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-3))))

    # Relacionamentos
    reservations = db.relationship('Reservation', backref='space', lazy='dynamic')

    @property
    def is_available(self):
        """Verifica se o espaço está disponível (não em manutenção)."""
        return self.status == 'available'

    def __repr__(self):
        return f'<Space {self.name} ({self.status})>'
