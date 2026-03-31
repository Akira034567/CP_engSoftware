"""
Pacote de modelos do sistema.
Inicializa a instância do SQLAlchemy usada por todos os modelos.
"""

from flask_sqlalchemy import SQLAlchemy

# Instância global do SQLAlchemy
db = SQLAlchemy()
