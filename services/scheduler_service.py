"""
Serviço de Agendamento (RF10).
Verifica periodicamente reservas que expiraram sem check-in
e as marca como 'no_show' (não compareceu).
"""

from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from models import db
from models.reservation import Reservation
from services.notification_service import send_notification


# Instância global do scheduler
scheduler = BackgroundScheduler(daemon=True)


def check_expired_reservations(app, checkin_window_minutes=2):
    """
    Verifica reservas ativas cuja janela de check-in já expirou.
    Marca como 'no_show' e notifica o usuário (RF10).

    Args:
        app: Instância do Flask (para contexto do banco).
        checkin_window_minutes: Janela de tolerância em minutos.
    """
    with app.app_context():
        now = datetime.now(timezone(timedelta(hours=-3)))
        # Reservas ativas cujo horário de início + janela já passou
        cutoff = now - timedelta(minutes=checkin_window_minutes)

        expired = Reservation.query.filter(
            Reservation.status == 'active',
            Reservation.start_time <= cutoff
        ).all()

        for reservation in expired:
            reservation.status = 'no_show'

            # Notifica usuário (RF07)
            send_notification(
                reservation.user_id,
                '⚠️ Reserva Cancelada - Não Comparecimento',
                f'Sua reserva para "{reservation.space.name}" em '
                f'{reservation.start_time.strftime("%d/%m/%Y %H:%M")} '
                f'foi cancelada automaticamente por não comparecimento.'
            )

        if expired:
            db.session.commit()


def complete_finished_reservations(app):
    """
    Marca como 'completed' reservas com check-in cujo horário de fim já passou.

    Args:
        app: Instância do Flask (para contexto do banco).
    """
    with app.app_context():
        now = datetime.now(timezone(timedelta(hours=-3)))

        finished = Reservation.query.filter(
            Reservation.status == 'checked_in',
            Reservation.end_time <= now
        ).all()

        for reservation in finished:
            reservation.status = 'completed'

            send_notification(
                reservation.user_id,
                '🎓 Sessão Concluída',
                f'Sua sessão em "{reservation.space.name}" foi concluída. '
                f'Obrigado por utilizar nossos espaços!'
            )

        if finished:
            db.session.commit()


def init_scheduler(app):
    """
    Inicializa o scheduler com as tarefas periódicas.

    Args:
        app: Instância do Flask.
    """
    checkin_window = app.config.get('CHECKIN_WINDOW_MINUTES', 2)
    interval = app.config.get('SCHEDULER_CHECK_INTERVAL', 60)

    # Verifica reservas expiradas a cada intervalo
    scheduler.add_job(
        func=check_expired_reservations,
        trigger='interval',
        seconds=interval,
        args=[app, checkin_window],
        id='check_expired',
        replace_existing=True
    )

    # Completa reservas finalizadas
    scheduler.add_job(
        func=complete_finished_reservations,
        trigger='interval',
        seconds=interval,
        args=[app],
        id='complete_finished',
        replace_existing=True
    )

    scheduler.start()
