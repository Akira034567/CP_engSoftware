"""
Rotas de Notificações (RF07).
Visualização e gerenciamento de notificações do sistema.
"""

from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
from services.notification_service import (
    get_user_notifications,
    mark_as_read,
    mark_all_as_read,
)

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')


@notifications_bp.route('/')
@login_required
def index():
    """Lista as notificações do usuário (RF07)."""
    notifications = get_user_notifications(current_user.id)
    return render_template('notifications/index.html', notifications=notifications)


@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])
@login_required
def read(notification_id):
    """Marca uma notificação como lida."""
    mark_as_read(notification_id, current_user.id)
    return redirect(url_for('notifications.index'))


@notifications_bp.route('/read-all', methods=['POST'])
@login_required
def read_all():
    """Marca todas as notificações como lidas."""
    mark_all_as_read(current_user.id)
    return redirect(url_for('notifications.index'))


@notifications_bp.route('/api/count')
@login_required
def api_count():
    """API para badge de notificações no header (polling)."""
    count = current_user.unread_notifications_count
    return jsonify({'count': count})
