/**
 * JavaScript principal do sistema.
 * Implementa polling para atualização em tempo real (RF01),
 * controle de notificações e interatividade geral.
 */

document.addEventListener('DOMContentLoaded', () => {
    // ---- Auto-dismiss flash messages ----
    initFlashMessages();

    // ---- Polling de espaços (RF01) ----
    if (document.getElementById('spaces-grid')) {
        initSpacesPolling();
    }

    // ---- Polling de notificações (RF07) ----
    initNotificationBadge();
});


/**
 * Inicializa auto-dismiss dos flash messages.
 * Clique para fechar e auto-remove após 5 segundos.
 */
function initFlashMessages() {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach((flash, index) => {
        // Auto-remove após 5 segundos
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(30px)';
            setTimeout(() => flash.remove(), 300);
        }, 5000 + index * 500);

        // Clique para fechar
        flash.addEventListener('click', () => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(30px)';
            setTimeout(() => flash.remove(), 300);
        });
    });
}


/**
 * Polling de status dos espaços a cada 5 segundos (RF01).
 * Atualiza os cards sem recarregar a página.
 */
function initSpacesPolling() {
    const updateSpaces = async () => {
        try {
            const response = await fetch('/spaces/api/status');
            if (!response.ok) return;

            const spaces = await response.json();
            const grid = document.getElementById('spaces-grid');

            spaces.forEach(space => {
                const card = document.querySelector(`[data-space-id="${space.id}"]`);
                if (card) {
                    // Atualiza status
                    card.setAttribute('data-status', space.status);

                    // Atualiza badge de status
                    const badge = card.querySelector('.status-badge');
                    if (badge) {
                        badge.className = `status-badge ${space.status}`;
                        badge.textContent = space.status_label;
                    }
                }
            });
        } catch (err) {
            // Silencioso em caso de erro de rede
            console.debug('Erro no polling de espaços:', err);
        }
    };

    // Atualiza a cada 5 segundos
    setInterval(updateSpaces, 5000);
}


/**
 * Polling do badge de notificações a cada 10 segundos (RF07).
 */
function initNotificationBadge() {
    const badge = document.getElementById('notification-count');
    if (!badge) return;

    const updateBadge = async () => {
        try {
            const response = await fetch('/notifications/api/count');
            if (!response.ok) return;

            const data = await response.json();
            const count = data.count;

            if (count > 0) {
                badge.textContent = count > 9 ? '9+' : count;
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
            }
        } catch (err) {
            console.debug('Erro no polling de notificações:', err);
        }
    };

    // Atualiza a cada 10 segundos
    setInterval(updateBadge, 10000);
    updateBadge(); // Atualiza imediatamente
}


/**
 * Confirmação antes de ações destrutivas (cancelar reserva, remover espaço).
 */
function confirmAction(message) {
    return confirm(message || 'Tem certeza que deseja realizar esta ação?');
}
