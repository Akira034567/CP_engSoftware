"""
Rotas de Autenticação (RNF03).
Login, registro e logout de usuários.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login."""
    if current_user.is_authenticated:
        return redirect(url_for('spaces.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Validação de entrada
        if not username or not password:
            flash('Preencha todos os campos.', 'error')
            return render_template('auth/login.html')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Bem-vindo(a), {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('spaces.index'))
        else:
            flash('Usuário ou senha incorretos.', 'error')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de novo usuário."""
    if current_user.is_authenticated:
        return redirect(url_for('spaces.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # Validações de entrada
        errors = []
        if not username or not email or not password:
            errors.append('Preencha todos os campos.')
        if len(username) < 3:
            errors.append('O nome de usuário deve ter pelo menos 3 caracteres.')
        if len(password) < 6:
            errors.append('A senha deve ter pelo menos 6 caracteres.')
        if password != confirm:
            errors.append('As senhas não coincidem.')
        if User.query.filter_by(username=username).first():
            errors.append('Este nome de usuário já está em uso.')
        if User.query.filter_by(email=email).first():
            errors.append('Este e-mail já está cadastrado.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/register.html')

        # Cria o usuário
        user = User(username=username, email=email, role='student')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Conta criada com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Encerra a sessão do usuário."""
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))
