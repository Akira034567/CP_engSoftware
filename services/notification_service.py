"""
Serviço de Notificações (RF07).
Centraliza a criação e envio de notificações dentro do sistema.
"""

from models import db
from models.notification import Notification


def send_notification(user_id, title, message):
    """
    Envia uma notificação para um usuário.

    Args:
        user_id: ID do usuário destinatário.
        title: Título da notificação.
        message: Corpo da mensagem.

    Returns:
        A notificação criada.
    """
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message
    )
    db.session.add(notification)
    db.session.commit()
    return notification


def mark_as_read(notification_id, user_id):
    """
    Marca uma notificação como lida.

    Args:
        notification_id: ID da notificação.
        user_id: ID do usuário dono da notificação (segurança).

    Returns:
        True se marcou com sucesso, False caso contrário.
    """
    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=user_id
    ).first()

    if notification:
        notification.is_read = True
        db.session.commit()
        return True
    return False


def mark_all_as_read(user_id):
    """Marca todas as notificações de um usuário como lidas."""
    Notification.query.filter_by(
        user_id=user_id,
        is_read=False
    ).update({'is_read': True})
    db.session.commit()


def get_user_notifications(user_id, limit=50):
    """
    Retorna as notificações de um usuário, ordenadas por data.

    Args:
        user_id: ID do usuário.
        limit: Número máximo de notificações.

    Returns:
        Lista de notificações.
    """
    return Notification.query.filter_by(
        user_id=user_id
    ).order_by(
        Notification.created_at.desc()
    ).limit(limit).all()
