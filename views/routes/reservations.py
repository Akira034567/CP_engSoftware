"""
Rotas de Reservas (RF02-RF06).
Criação, cancelamento, check-in e histórico de reservas.
"""

from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from models.space import Space
from services.reservation_service import (
    create_reservation,
    cancel_reservation,
    do_checkin,
    get_user_reservations,
)

reservations_bp = Blueprint('reservations', __name__, url_prefix='/reservations')


@reservations_bp.route('/')
@login_required
def my_reservations():
    """Lista as reservas do usuário logado (RF06)."""
    status_filter = request.args.get('status')
    if current_user.is_admin:
        reservations = get_user_reservations(None, status_filter)
    else:
        reservations = get_user_reservations(current_user.id, status_filter)
    return render_template(
        'reservations/my_reservations.html',
        reservations=reservations,
        current_filter=status_filter
    )


@reservations_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_reservation():
    """Formulário para criar uma nova reserva (RF02)."""
    if request.method == 'POST':
        space_id = request.form.get('space_id', type=int)
        date_str = request.form.get('date', '')
        start_str = request.form.get('start_time', '')
        end_str = request.form.get('end_time', '')

        # Validação de entrada
        if not all([space_id, date_str, start_str, end_str]):
            flash('Preencha todos os campos.', 'error')
            return redirect(url_for('reservations.new_reservation'))

        try:
            start_time = datetime.strptime(f'{date_str} {start_str}', '%Y-%m-%d %H:%M')
            end_time = datetime.strptime(f'{date_str} {end_str}', '%Y-%m-%d %H:%M')
        except ValueError:
            flash('Formato de data/hora inválido.', 'error')
            return redirect(url_for('reservations.new_reservation'))

        reservation, error = create_reservation(
            user_id=current_user.id,
            space_id=space_id,
            start_time=start_time,
            end_time=end_time
        )

        if error:
            flash(error, 'error')
            return redirect(url_for('reservations.new_reservation'))

        flash('Reserva criada com sucesso!', 'success')
        return redirect(url_for('reservations.my_reservations'))

    # GET: mostra formulário
    spaces = Space.query.filter_by(status='available').order_by(Space.name).all()
    return render_template('reservations/create.html', spaces=spaces)


@reservations_bp.route('/<int:reservation_id>/cancel', methods=['POST'])
@login_required
def cancel(reservation_id):
    """Cancela uma reserva (RF03)."""
    success, message = cancel_reservation(
        reservation_id,
        current_user.id,
        is_admin=current_user.is_admin
    )

    flash(message, 'success' if success else 'error')
    return redirect(url_for('reservations.my_reservations'))


@reservations_bp.route('/<int:reservation_id>/checkin', methods=['POST'])
@login_required
def checkin(reservation_id):
    """Realiza check-in na reserva (RF04, RF05)."""
    window = current_app.config.get('CHECKIN_WINDOW_MINUTES', 2)
    success, message = do_checkin(reservation_id, current_user.id, window)

    flash(message, 'success' if success else 'error')
    return redirect(url_for('reservations.my_reservations'))
