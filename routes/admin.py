"""
Rotas de Administração (RF08, RF09).
Gerenciamento de espaços e relatórios de uso.
Acesso restrito a usuários com role 'admin'.
"""

from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.space import Space
from models.user import User
from models.reservation import Reservation
from services.reservation_service import get_usage_stats

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator para restringir acesso a administradores."""
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            flash('Acesso negado. Apenas administradores.', 'error')
            return redirect(url_for('spaces.index'))
        return f(*args, **kwargs)
    return decorated


# ---- Gerenciar Espaços (RF08) ----

@admin_bp.route('/spaces')
@admin_required
def manage_spaces():
    """Lista todos os espaços para gerenciamento."""
    spaces = Space.query.order_by(Space.name).all()
    return render_template('admin/manage_spaces.html', spaces=spaces)


@admin_bp.route('/spaces/new', methods=['GET', 'POST'])
@admin_required
def new_space():
    """Cria um novo espaço de estudo."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        capacity = request.form.get('capacity', type=int, default=1)
        location = request.form.get('location', '').strip()

        # Validação
        if not name:
            flash('O nome do espaço é obrigatório.', 'error')
            return render_template('admin/space_form.html', space=None)

        if capacity < 1:
            flash('A capacidade deve ser pelo menos 1.', 'error')
            return render_template('admin/space_form.html', space=None)

        space = Space(
            name=name,
            description=description,
            capacity=capacity,
            location=location,
            status='available'
        )
        db.session.add(space)
        db.session.commit()

        flash(f'Espaço "{name}" criado com sucesso!', 'success')
        return redirect(url_for('admin.manage_spaces'))

    return render_template('admin/space_form.html', space=None)


@admin_bp.route('/spaces/<int:space_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_space(space_id):
    """Edita um espaço existente."""
    space = Space.query.get_or_404(space_id)

    if request.method == 'POST':
        space.name = request.form.get('name', '').strip()
        space.description = request.form.get('description', '').strip()
        space.capacity = request.form.get('capacity', type=int, default=1)
        space.location = request.form.get('location', '').strip()
        space.status = request.form.get('status', 'available')

        if not space.name:
            flash('O nome do espaço é obrigatório.', 'error')
            return render_template('admin/space_form.html', space=space)

        db.session.commit()
        flash(f'Espaço "{space.name}" atualizado!', 'success')
        return redirect(url_for('admin.manage_spaces'))

    return render_template('admin/space_form.html', space=space)


@admin_bp.route('/spaces/<int:space_id>/delete', methods=['POST'])
@admin_required
def delete_space(space_id):
    """Remove um espaço de estudo."""
    space = Space.query.get_or_404(space_id)

    # Verifica se há reservas ativas
    active_reservations = Reservation.query.filter(
        Reservation.space_id == space_id,
        Reservation.status.in_(['active', 'checked_in'])
    ).count()

    if active_reservations > 0:
        flash('Não é possível remover um espaço com reservas ativas.', 'error')
        return redirect(url_for('admin.manage_spaces'))

    name = space.name
    db.session.delete(space)
    db.session.commit()
    flash(f'Espaço "{name}" removido.', 'success')
    return redirect(url_for('admin.manage_spaces'))


# ---- Relatórios (RF09) ----

@admin_bp.route('/reports')
@admin_required
def reports():
    """Dashboard de relatórios de uso."""
    stats = get_usage_stats()
    total_users = User.query.count()
    total_spaces = Space.query.count()

    return render_template(
        'admin/reports.html',
        stats=stats,
        total_users=total_users,
        total_spaces=total_spaces
    )
