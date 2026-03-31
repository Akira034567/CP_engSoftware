"""
Configurações do sistema de reserva de espaços de estudo.
Define parâmetros de banco de dados, segurança e regras de negócio.
"""

import os

# Diretório base do projeto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuração principal do sistema."""

    # Chave secreta para sessões e CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Banco de dados SQLite (persiste em arquivo)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(BASE_DIR, "instance", "reservas.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Regras de Negócio ---
    # Janela de check-in: minutos antes e depois do horário da reserva
    CHECKIN_WINDOW_MINUTES = 5

    # Intervalo (em segundos) para verificar reservas expiradas (RF10)
    SCHEDULER_CHECK_INTERVAL = 60
