"""
Modelo de Reserva.
Gerencia o ciclo de vida completo: criação → check-in → conclusão (ou cancelamento/no-show).
Relaciona usuários a espaços com controle de horário (RF02-RF06, RF10).
"""

from datetime import datetime, timezone, timedelta
from models import db


class Reservation(db.Model):
    """Representa uma reserva de espaço de estudo."""

    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'), nullable=False, index=True)
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    # Status possíveis: 'active', 'checked_in', 'completed', 'cancelled', 'no_show'
    checked_in_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-3))))

    @property
    def is_active(self):
        """Verifica se a reserva está ativa (não cancelada/concluída)."""
        return self.status in ('active', 'checked_in')

    @property
    def status_label(self):
        """Retorna label legível do status em português."""
        labels = {
            'active': 'Ativa',
            'checked_in': 'Check-in Realizado',
            'completed': 'Concluída',
            'cancelled': 'Cancelada',
            'no_show': 'Não Compareceu',
        }
        return labels.get(self.status, self.status)

    @property
    def status_color(self):
        """Retorna classe CSS de cor para o status."""
        colors = {
            'active': 'status-active',
            'checked_in': 'status-checkedin',
            'completed': 'status-completed',
            'cancelled': 'status-cancelled',
            'no_show': 'status-noshow',
        }
        return colors.get(self.status, '')

    def __repr__(self):
        return f'<Reservation {self.id} - {self.status}>'
