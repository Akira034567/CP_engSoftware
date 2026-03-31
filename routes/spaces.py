"""
Rotas de Espaços (RF01).
Visualização de espaços disponíveis em tempo real.
"""

from datetime import datetime, timezone, timedelta
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.space import Space
from models.reservation import Reservation

spaces_bp = Blueprint('spaces', __name__, url_prefix='/spaces')


@spaces_bp.route('/')
@login_required
def index():
    """Página principal - visualizar todos os espaços (RF01)."""
    spaces = Space.query.order_by(Space.name).all()
    return render_template('spaces/index.html', spaces=spaces)


@spaces_bp.route('/api/status')
@login_required
def api_status():
    """
    API para atualização em tempo real dos espaços (RF01).
    Retorna status atual de cada espaço (disponível/ocupado/manutenção).
    Usado por polling JavaScript a cada 5 segundos.
    """
    spaces = Space.query.order_by(Space.name).all()
    now = datetime.now(timezone(timedelta(hours=-3)))

    result = []
    for space in spaces:
        # Verifica se há reserva ativa/check-in neste momento
        current_reservation = Reservation.query.filter(
            Reservation.space_id == space.id,
            Reservation.status.in_(['active', 'checked_in']),
            Reservation.start_time <= now,
            Reservation.end_time > now
        ).first()

        if space.status == 'maintenance':
            status = 'maintenance'
            label = 'Manutenção'
        elif current_reservation:
            status = 'occupied'
            label = 'Ocupado'
        else:
            status = 'available'
            label = 'Disponível'

        result.append({
            'id': space.id,
            'name': space.name,
            'description': space.description,
            'capacity': space.capacity,
            'location': space.location,
            'status': status,
            'status_label': label,
        })

    return jsonify(result)


@spaces_bp.route('/api/<int:space_id>/agenda')
@login_required
def api_space_agenda(space_id):
    """
    Retorna as reservas ativas para um espaço em uma data específica.
    Usado no formulário de reserva para mostrar horários ocupados.
    """
    from flask import request
    date_str = request.args.get('date')
    if not date_str:
        return jsonify([])
        
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_of_day = datetime.combine(date_obj, datetime.min.time()).replace(tzinfo=timezone(timedelta(hours=-3)))
        end_of_day = datetime.combine(date_obj, datetime.max.time()).replace(tzinfo=timezone(timedelta(hours=-3)))
    except ValueError:
        return jsonify([])
        
    reservations = Reservation.query.filter(
        Reservation.space_id == space_id,
        Reservation.status.in_(['active', 'checked_in']),
        Reservation.start_time >= start_of_day,
        Reservation.start_time <= end_of_day
    ).order_by(Reservation.start_time).all()
    
    result = [{
        'start': r.start_time.strftime('%H:%M'),
        'end': r.end_time.strftime('%H:%M')
    } for r in reservations]
    
    return jsonify(result)
