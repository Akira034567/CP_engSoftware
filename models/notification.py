"""
Modelo de Notificação.
Permite envio de mensagens dentro do sistema para os usuários (RF07).
"""

from datetime import datetime, timezone, timedelta
from models import db


class Notification(db.Model):
    """Representa uma notificação enviada a um usuário."""

    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-3))))

    @property
    def time_ago(self):
        """Retorna tempo relativo da notificação (ex: 'há 5 minutos')."""
        now = datetime.now(timezone(timedelta(hours=-3)))
        diff = now - self.created_at.replace(tzinfo=timezone(timedelta(hours=-3)))
        seconds = int(diff.total_seconds())

        if seconds < 60:
            return 'agora mesmo'
        elif seconds < 3600:
            minutes = seconds // 60
            return f'há {minutes} min'
        elif seconds < 86400:
            hours = seconds // 3600
            return f'há {hours}h'
        else:
            days = seconds // 86400
            return f'há {days}d'

    def __repr__(self):
        return f'<Notification {self.id} - {self.title}>'
