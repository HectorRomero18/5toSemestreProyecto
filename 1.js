// Obtener datos de las letras favoritas desde Django
const favoriteLettersData = JSON.parse(document.getElementById('favorite-letters-data').textContent);

// Variables globales
let currentFilter = 'all';
let favoriteLetters = favoriteLettersData || [];

// Si no hay datos desde Django, usar datos de ejemplo
if (favoriteLetters.length === 0) {
    favoriteLetters = [
        { id: 1, letter: 'A', name: 'Letra A', favoriteDate: '2024-01-15', type: 'vocal', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png', isFavorite: true },
        { id: 2, letter: 'E', name: 'Letra E', favoriteDate: '2024-01-20', type: 'vocal', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png', isFavorite: true },
        { id: 3, letter: 'M', name: 'Letra M', favoriteDate: '2024-02-05', type: 'consonante', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png', isFavorite: true },
        { id: 4, letter: 'P', name: 'Letra P', favoriteDate: '2024-02-10', type: 'consonante', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png', isFavorite: true },
        { id: 5, letter: 'S', name: 'Letra S', favoriteDate: '2024-02-15', type: 'consonante', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png', isFavorite: true },
        { id: 6, letter: 'L', name: 'Letra L', favoriteDate: '2024-02-20', type: 'consonante', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png', isFavorite: true }
    ];
}

// Función para formatear fecha
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

// Función para filtrar letras
function filterLetters(type) {
    currentFilter = type;
    
    // Actualizar botones activos
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(.filter-btn[data-filter="${type}"]).classList.add('active');
    
    // Filtrar y renderizar letras
    renderFavoriteLetters();
}

// Función para obtener letras filtradas
function getFilteredLetters() {
    if (currentFilter === 'all') {
        return favoriteLetters;
    }
    return favoriteLetters.filter(letter => letter.type === currentFilter);
}

// Función para quitar de favoritos
function removeFromFavorites(letterId) {
    // En una implementación real, haríamos una llamada a la API para actualizar en la base de datos
    console.log(Quitando de favoritos: ${letterId});
    
    // Encontrar la letra para mostrar el nombre en la notificación
    const letter = favoriteLetters.find(l => l.id === letterId);
    
    // Actualizar la lista local (simulación)
    const index = favoriteLetters.findIndex(l => l.id === letterId);
    if (index !== -1) {
        favoriteLetters.splice(index, 1);
    }
    
    // Actualizar estadísticas y renderizar
    updateStats();
    renderFavoriteLetters();
    
    // Mostrar mensaje de confirmación
    if (letter) {
        alert(${letter.name} eliminada de favoritos);
    }
}

// Función para actualizar las estadísticas
function updateStats() {
    const vocals = favoriteLetters.filter(letter => letter.type === 'vocal').length;
    const consonants = favoriteLetters.filter(letter => letter.type === 'consonante').length;
    
    document.getElementById('totalFavorites').textContent = favoriteLetters.length;
    document.getElementById('vocalsCount').textContent = vocals;
    document.getElementById('consonantsCount').textContent = consonants;
}

// Función para renderizar las letras favoritas
function renderFavoriteLetters() {
    const favoritesContent = document.getElementById('favoritesContent');
    const filteredLetters = getFilteredLetters();
    
    if (filteredLetters.length === 0) {
        favoritesContent.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">⭐</div>
                <h2 class="empty-title">No hay letras favoritas</h2>
                <p class="empty-description">${
                    currentFilter === 'all' 
                    ? 'Aún no has marcado ninguna letra como favorita. ¡Explora la tienda y marca tus letras preferidas!' 
                    : No tienes letras ${currentFilter === 'vocal' ? 'vocales' : 'consonantes'} marcadas como favoritas
                }</p>
                <button class="cta-button" onclick="window.location.href='tienda.html'">Explorar Letras</button>
            </div>
        `;
        return;
    }
    
    favoritesContent.innerHTML = `
        <div class="letters-grid" id="favoritesGrid">
            <!-- Las letras favoritas se generarán con JavaScript -->
        </div>
    `;
    
    const favoritesGrid = document.getElementById('favoritesGrid');
    
    // Renderizar letras favoritas
    filteredLetters.forEach(item => {
        const card = createLetterCard(item);
        favoritesGrid.appendChild(card);
    });
    
    // Agregar event listeners a los botones de corazón
    document.querySelectorAll('.heart-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const letterId = button.getAttribute('data-letter-id');
            removeFromFavorites(parseInt(letterId));
        });
    });
    
    // Agregar event listeners a las tarjetas
    document.querySelectorAll('.letter-card').forEach(card => {
        card.addEventListener('click', () => {
            const letterName = card.querySelector('.letter-name').textContent;
            console.log(Tarjeta clickeada: ${letterName});
        });
    });
}

// Función para crear una tarjeta de letra
function createLetterCard(item) {
    const card = document.createElement('div');
    card.className = 'letter-card';
    
    card.innerHTML = `
        <div class="letter-display">
            <img src="${item.bg}" alt="${item.name}" class="letter-bg" />
            <span class="letter-text">${item.letter}</span>
        </div>
        <div class="letter-footer">
            <span class="letter-name">${item.name}</span>
            <div class="letter-actions">
                <button class="heart-btn" title="Quitar Favorito" data-letter-id="${item.id}">
                    <svg class="heart-icon" width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                    </svg>
                </button>
            </div>
        </div>
    `;
    
    return card;
}

// Funcionalidad de búsqueda
document.getElementById('searchInput').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    
    // Si no hay término de búsqueda, mostrar todas las letras filtradas
    if (!searchTerm) {
        renderFavoriteLetters();
        return;
    }
    
    const filteredLetters = getFilteredLetters().filter(letter => 
        letter.name.toLowerCase().includes(searchTerm) || 
        letter.letter.toLowerCase().includes(searchTerm)
    );
    
    const favoritesGrid = document.getElementById('favoritesGrid');
    if (!favoritesGrid) return;
    
    favoritesGrid.innerHTML = '';
    
    if (filteredLetters.length === 0) {
        favoritesGrid.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1; max-width: 100%;">
                <div class="empty-icon">🔍</div>
                <h2 class="empty-title">No se encontraron letras</h2>
                <p class="empty-description">No hay letras que coincidan con "${searchTerm}"</p>
                <button class="cta-button" onclick="document.getElementById('searchInput').value=''; renderFavoriteLetters();">Ver Todas</button>
            </div>
        `;
        return;
    }
    
    // Renderizar letras filtradas
    filteredLetters.forEach(item => {
        const card = createLetterCard(item);
        favoritesGrid.appendChild(card);
    });
    
    // Reagregar event listeners después de la búsqueda
    document.querySelectorAll('.heart-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const letterId = button.getAttribute('data-letter-id');
            removeFromFavorites(parseInt(letterId));
        });
    });
});

// Agregar event listeners a los botones de filtro
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const filterType = btn.getAttribute('data-filter');
        filterLetters(filterType);
    });
});

// Inicializar la página
function initPage() {
    updateStats();
    renderFavoriteLetters();
}

// Ejecutar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', initPage);