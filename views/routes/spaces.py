"""Rotas de Espaços (RF01) com recomendação inteligente de laboratórios."""

from datetime import datetime, timezone, timedelta
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from models.space import Space
from models.reservation import Reservation

spaces_bp = Blueprint('spaces', __name__, url_prefix='/spaces')

CATEGORY_LABELS = {
    'programacao': 'Programação',
    'web': 'Desenvolvimento Web',
    'dados': 'Banco de Dados',
    'redes': 'Redes e Infraestrutura',
    'ciberseguranca': 'Cibersegurança',
    'ia_ml': 'Inteligência Artificial / Machine Learning',
    'iot_embarcados': 'IoT / Sistemas Embarcados',
    'mobile': 'Desenvolvimento Mobile',
    'uso_basico': 'Uso básico / Estudos gerais',
    'alto_desempenho': 'Alto desempenho',
    'grafica_jogos': 'Computação gráfica / Renderização / Jogos',
    'ios_apple': 'Desenvolvimento para iOS / Ecossistema Apple',
    'modernos': 'Laboratórios mais modernos',
}

CATEGORY_FLOORS = {
    'programacao': [2, 3, 7, 8, 9],
    'web': [2, 3, 7, 8, 9],
    'dados': [3, 9],
    'redes': [2, 6],
    'ciberseguranca': [3, 9],
    'ia_ml': [5, 9],
    'iot_embarcados': [2, 6],
    'mobile': [3, 5, 9],
    'uso_basico': [6, 7, 8],
    'alto_desempenho': [9, 5, 3],
    'grafica_jogos': [5],
    'ios_apple': [5],
    'modernos': [9, 3],
}

CATEGORY_EXACT_SPACES = {
    'ia_ml': {'Laboratório 502 (Lab Gamer)'},
    'grafica_jogos': {'Laboratório 502 (Lab Gamer)'},
    'ios_apple': {'Laboratório 503 (Lab de MacBooks)'},
}


@spaces_bp.route('/')
@login_required
def index():
    """Página principal - visualizar espaços e recomendações por categoria."""
    selected_category = request.args.get('category', '').strip()
    spaces = Space.query.order_by(Space.name).all()

    recommendations = []
    if selected_category in CATEGORY_LABELS:
        recommendations = _recommend_spaces(selected_category, spaces)

    return render_template(
        'spaces/index.html',
        spaces=spaces,
        category_labels=CATEGORY_LABELS,
        selected_category=selected_category,
        recommendations=recommendations,
    )


@spaces_bp.route('/api/status')
@login_required
def api_status():
    spaces = Space.query.order_by(Space.name).all()
    now = datetime.now(timezone(timedelta(hours=-3)))

    result = []
    for space in spaces:
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

    result = [{'start': r.start_time.strftime('%H:%M'), 'end': r.end_time.strftime('%H:%M')} for r in reservations]
    return jsonify(result)


def _recommend_spaces(category, spaces):
    target_floors = CATEGORY_FLOORS.get(category, [])
    preferred_names = CATEGORY_EXACT_SPACES.get(category, set())

    ranked = []
    for space in spaces:
        floor = _extract_floor(space.location)
        score = 0
        reason_parts = []

        if space.name in preferred_names:
            score += 100
            reason_parts.append('equipamento especializado para essa categoria')

        if floor in target_floors:
            rank = len(target_floors) - target_floors.index(floor)
            score += 50 + rank
            reason_parts.append(f'{floor}º andar recomendado para este tipo de uso')

        if 'gpu' in space.description.lower() and category in {'ia_ml', 'grafica_jogos', 'alto_desempenho'}:
            score += 30
            reason_parts.append('possui perfil de hardware com GPU')

        if category == 'uso_basico' and space.capacity >= 28:
            score += 10
            reason_parts.append('boa capacidade para estudos gerais')

        if score > 0 and space.status == 'available':
            ranked.append({'space': space, 'score': score, 'reason': '; '.join(reason_parts)})

    ranked.sort(key=lambda item: (-item['score'], item['space'].name))
    return ranked[:8]


def _extract_floor(location):
    if not location:
        return None
    first = location.strip().split('º')[0]
    return int(first) if first.isdigit() else None
