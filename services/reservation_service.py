"""
Serviço de Reservas (RF02-RF06).
Contém toda a lógica de negócio para criação, validação, check-in e cancelamento de reservas.
"""

from datetime import datetime, timedelta, timezone
from models import db
from models.reservation import Reservation
from models.space import Space
from services.notification_service import send_notification


def get_available_spaces(start_time, end_time):
    """
    Retorna espaços disponíveis para um período (RF01).

    Filtra espaços que não estão em manutenção e não possuem
    reservas ativas que conflitem com o período solicitado.

    Args:
        start_time: Início do período desejado.
        end_time: Fim do período desejado.

    Returns:
        Lista de espaços disponíveis.
    """
    # Busca IDs de espaços com reservas conflitantes
    conflicting = db.session.query(Reservation.space_id).filter(
        Reservation.status.in_(['active', 'checked_in']),
        Reservation.start_time < end_time,
        Reservation.end_time > start_time
    ).subquery()

    # Retorna espaços disponíveis sem conflitos
    return Space.query.filter(
        Space.status == 'available',
        ~Space.id.in_(db.session.query(conflicting.c.space_id))
    ).all()


def create_reservation(user_id, space_id, start_time, end_time):
    """
    Cria uma nova reserva (RF02).

    Valida:
    - Se o espaço existe e está disponível
    - Se não há conflito de horário
    - Se o horário é futuro

    Args:
        user_id: ID do usuário que está reservando.
        space_id: ID do espaço a reservar.
        start_time: Início da reserva.
        end_time: Fim da reserva.

    Returns:
        Tuple (reserva, mensagem_erro). Se sucesso, erro é None.
    """
    # Validação: espaço existe?
    space = Space.query.get(space_id)
    if not space:
        return None, 'Espaço não encontrado.'

    # Validação: espaço disponível?
    if not space.is_available:
        return None, 'Este espaço está em manutenção.'

    # Validação: horário válido?
    now = datetime.now(timezone(timedelta(hours=-3)))
    start_aware = start_time.replace(tzinfo=timezone(timedelta(hours=-3)))
    min_start = now + timedelta(minutes=30)

    if start_aware < now:
        return None, '⏰ O horário selecionado já passou. Escolha um horário futuro para sua reserva.'

    if start_aware < min_start:
        horario_minimo = min_start.strftime('%H:%M')
        return None, f'⏳ Para reservas no dia de hoje, o horário mínimo é {horario_minimo} (30 min a partir de agora).'

    if end_time <= start_time:
        return None, '⚠️ O horário de término deve ser posterior ao horário de início.'

    # Validação: conflito de reserva?
    conflict = Reservation.query.filter(
        Reservation.space_id == space_id,
        Reservation.status.in_(['active', 'checked_in']),
        Reservation.start_time < end_time,
        Reservation.end_time > start_time
    ).first()

    if conflict:
        return None, 'Este espaço já está reservado para o período selecionado.'

    # Cria a reserva
    reservation = Reservation(
        user_id=user_id,
        space_id=space_id,
        start_time=start_time,
        end_time=end_time,
        status='active'
    )
    db.session.add(reservation)
    db.session.commit()

    # Envia notificação de confirmação (RF07)
    send_notification(
        user_id,
        '✅ Reserva Confirmada',
        f'Sua reserva para "{space.name}" foi confirmada para '
        f'{start_time.strftime("%d/%m/%Y %H:%M")} - {end_time.strftime("%H:%M")}.'
    )

    return reservation, None


def cancel_reservation(reservation_id, user_id, is_admin=False):
    """
    Cancela uma reserva (RF03).

    Args:
        reservation_id: ID da reserva.
        user_id: ID do usuário solicitando cancelamento.
        is_admin: Se True, permite cancelar reservas de outros usuários.

    Returns:
        Tuple (sucesso, mensagem).
    """
    reservation = Reservation.query.get(reservation_id)

    if not reservation:
        return False, 'Reserva não encontrada.'

    # Verifica permissão
    if not is_admin and reservation.user_id != user_id:
        return False, 'Você não tem permissão para cancelar esta reserva.'

    if reservation.status not in ('active', 'checked_in'):
        return False, 'Esta reserva não pode ser cancelada.'

    reservation.status = 'cancelled'
    db.session.commit()

    # Notifica o usuário (RF07)
    send_notification(
        reservation.user_id,
        '❌ Reserva Cancelada',
        f'Sua reserva para "{reservation.space.name}" em '
        f'{reservation.start_time.strftime("%d/%m/%Y %H:%M")} foi cancelada.'
    )

    return True, 'Reserva cancelada com sucesso.'


def do_checkin(reservation_id, user_id, checkin_window_minutes=5):
    """
    Realiza check-in em uma reserva (RF04, RF05).

    Valida:
    - Se a reserva pertence ao usuário
    - Se a reserva está ativa
    - Se está dentro da janela de check-in (5 min antes/depois)

    Args:
        reservation_id: ID da reserva.
        user_id: ID do usuário fazendo check-in.
        checkin_window_minutes: Janela de tolerância em minutos.

    Returns:
        Tuple (sucesso, mensagem).
    """
    reservation = Reservation.query.get(reservation_id)

    if not reservation:
        return False, 'Reserva não encontrada.'

    if reservation.user_id != user_id:
        return False, 'Esta reserva não pertence a você.'

    if reservation.status != 'active':
        return False, f'Não é possível fazer check-in. Status atual: {reservation.status_label}.'

    # Validação da janela de check-in (RF05)
    now = datetime.now(timezone(timedelta(hours=-3)))
    start = reservation.start_time.replace(tzinfo=timezone(timedelta(hours=-3)))
    window_start = start - timedelta(minutes=checkin_window_minutes)
    window_end = start + timedelta(minutes=checkin_window_minutes)

    if now < window_start:
        return False, (
            f'Check-in disponível a partir de '
            f'{window_start.strftime("%H:%M")} '
            f'({checkin_window_minutes} min antes do horário).'
        )

    if now > window_end:
        return False, 'A janela de check-in expirou.'

    # Realiza check-in
    reservation.status = 'checked_in'
    reservation.checked_in_at = now
    db.session.commit()

    # Notifica (RF07)
    send_notification(
        user_id,
        '📍 Check-in Realizado',
        f'Check-in confirmado para "{reservation.space.name}". Bons estudos!'
    )

    return True, 'Check-in realizado com sucesso!'


def get_user_reservations(user_id=None, status_filter=None):
    """
    Retorna as reservas de um usuário, ou de todos se user_id for None (RF06).

    Args:
        user_id: ID do usuário (ou None para todos).
        status_filter: Filtrar por status específico (opcional).

    Returns:
        Lista de reservas ordenadas por data.
    """
    query = Reservation.query

    if user_id:
        query = query.filter_by(user_id=user_id)

    if status_filter:
        query = query.filter_by(status=status_filter)

    return query.order_by(Reservation.start_time.desc()).all()


def get_usage_stats():
    """
    Retorna estatísticas de uso para relatórios (RF09).

    Returns:
        Dicionário com estatísticas gerais.
    """
    total = Reservation.query.count()
    active = Reservation.query.filter_by(status='active').count()
    checked_in = Reservation.query.filter_by(status='checked_in').count()
    completed = Reservation.query.filter_by(status='completed').count()
    cancelled = Reservation.query.filter_by(status='cancelled').count()
    no_show = Reservation.query.filter_by(status='no_show').count()

    # Espaços mais reservados
    from sqlalchemy import func
    popular_spaces = db.session.query(
        Space.name,
        func.count(Reservation.id).label('total')
    ).join(Reservation).group_by(Space.name).order_by(
        func.count(Reservation.id).desc()
    ).limit(5).all()

    return {
        'total': total,
        'active': active,
        'checked_in': checked_in,
        'completed': completed,
        'cancelled': cancelled,
        'no_show': no_show,
        'popular_spaces': popular_spaces,
    }
