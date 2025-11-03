// =========================
// FAVORITOS.JS (CORREGIDO)
// =========================

// Variables globales
let favoriteLetters = [];
let currentFilter = 'all';

// -----------------------------
// Obtener CSRF token de cookies
// -----------------------------
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
        c = c.trim();
        if (c.startsWith(name + '=')) {
            return decodeURIComponent(c.substring(name.length + 1));
        }
    }
    return '';
}

// -----------------------------
// Inicializar la página
// -----------------------------
function initPage() {
    const modulesScript = document.getElementById('modules-data');
    if (modulesScript) {
        try {
            let data = JSON.parse(modulesScript.textContent);
            if (Array.isArray(data)) {
                favoriteLetters = data;
            } else if (data && typeof data === 'object') {
                favoriteLetters = Object.values(data);
            } else {
                favoriteLetters = [];
            }
            console.log('Datos cargados desde Django:', favoriteLetters);
        } catch (e) {
            console.error('Error al parsear modules-data:', e);
        }
    } else {
        console.warn('No se encontró modules-data en el DOM');
    }

    updateStats();
    renderFavoriteLetters();
    setupEventListeners();
}

// -----------------------------
// Filtros
// -----------------------------
function filterLetters(dificultad) {
    currentFilter = dificultad;

    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`.filter-btn[data-filter="${dificultad}"]`)?.classList.add('active');

    renderFavoriteLetters();
}

function getFilteredLetters() {
    if (currentFilter === 'all') return favoriteLetters;
    if (currentFilter === 'vocal') return favoriteLetters.filter(letter => letter.tipo === 'V');
    if (currentFilter === 'consonante') return favoriteLetters.filter(letter => letter.tipo === 'C');
    return favoriteLetters.filter(letter => letter.dificultad === currentFilter);
}

// -----------------------------
// Eliminar de favoritos localmente
// -----------------------------
function removeFromFavorites(letraId) {
    const index = favoriteLetters.findIndex(l => l.letra_id === letraId);
    if (index !== -1) favoriteLetters.splice(index, 1);

    updateStats();
    renderFavoriteLetters();
}

// -----------------------------
// Actualizar estadísticas
// -----------------------------
function updateStats() {
    const total = favoriteLetters.length;
    const vocals = favoriteLetters.filter(l => l.tipo === 'V').length;
    const consonants = favoriteLetters.filter(l => l.tipo === 'C').length;

    document.getElementById('totalFavorites').textContent = total;
    document.getElementById('vocalsCount').textContent = vocals;
    document.getElementById('consonantsCount').textContent = consonants;
}

// -----------------------------
// Crear tarjeta de letra
// -----------------------------
function createLetterCard(item) {
    const card = document.createElement('div');
    card.className = 'letter-card';
    card.dataset.tipo = item.tipo;
    card.dataset.dificultad = item.dificultad;

    card.innerHTML = `
        <div class="letter-display">
            <img src="${item.bg}" alt="${item.simbolo}" class="letter-bg" />
            <span class="letter-text">${item.simbolo}</span>
        </div>
        <div class="letter-footer">
            <span class="letter-name">${item.letter}</span>
            <div class="letter-actions">
                <button class="heart-btn active" title="Quitar Favorito" data-letra-id="${item.letra_id}">
                    <svg class="heart-icon" width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 
                                 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 
                                 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 
                                 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                    </svg>
                </button>
            </div>
        </div>
    `;
    return card;
}

// -----------------------------
// Renderizar letras favoritas
// -----------------------------
function renderFavoriteLetters() {
    const favoritesContent = document.getElementById('favoritesContent');
    const filteredLetters = getFilteredLetters();

    if (filteredLetters.length === 0) {
        favoritesContent.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">⭐</div>
                <h2 class="empty-title">No hay letras favoritas</h2>
                <p class="empty-description">No tienes letras marcadas como favoritas en esta categoría.</p>
            </div>
        `;
        return;
    }

    favoritesContent.innerHTML = `<div class="letters-grid" id="favoritesGrid"></div>`;
    const favoritesGrid = document.getElementById('favoritesGrid');

    filteredLetters.forEach(item => favoritesGrid.appendChild(createLetterCard(item)));

    // Event listeners para los botones de corazón
    document.querySelectorAll('.heart-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            e.stopPropagation();
            const letraId = parseInt(button.getAttribute('data-letra-id'));
            const isFavorite = button.classList.contains('active');

            try {
                if (isFavorite) {
                    // Quitar favorito
                    const resp = await fetch('/favoritos/delete/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCSRFToken(),
                        },
                        body: JSON.stringify({ letra_id: letraId }),
                    });
                    const data = await resp.json();
                    if (data.status) {
                        button.classList.remove('active');
                        removeFromFavorites(letraId);
                    }
                } else {
                    // Agregar favorito
                    const resp = await fetch('/favoritos/add/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCSRFToken(),
                        },
                        body: JSON.stringify({ letra_id: letraId }),
                    });
                    const data = await resp.json();
                    if (data.status) {
                        button.classList.add('active');
                        favoriteLetters.push({
                            letra_id: data.favorito.letra_id,
                            letter: button.closest('.letter-card').querySelector('.letter-text').textContent,
                            tipo: button.closest('.letter-card').dataset.tipo || 'V',
                            dificultad: button.closest('.letter-card').dataset.dificultad || 'Fácil',
                            bg: button.closest('.letter-card').querySelector('.letter-bg').src,
                        });
                        updateStats();
                        renderFavoriteLetters();
                    }
                }
            } catch (err) {
                console.error('Error al actualizar favorito:', err);
            }
        });
    });
}

// -----------------------------
// Búsqueda
// -----------------------------
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filtered = getFilteredLetters().filter(l => l.letter.toLowerCase().includes(searchTerm));

        const grid = document.getElementById('favoritesGrid');
        if (!grid) return;

        grid.innerHTML = '';
        if (filtered.length === 0) {
            grid.innerHTML = `<div class="empty-state" style="grid-column: 1 / -1;">No se encontraron letras</div>`;
            return;
        }

        filtered.forEach(item => grid.appendChild(createLetterCard(item)));
    });
}

// -----------------------------
// Eventos iniciales
// -----------------------------
function setupEventListeners() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => filterLetters(btn.getAttribute('data-filter')));
    });

    setupSearch();
}

// -----------------------------
// Iniciar
// -----------------------------
document.addEventListener('DOMContentLoaded', initPage);
