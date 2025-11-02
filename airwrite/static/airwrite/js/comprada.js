// Obtener datos de las letras compradas desde Django
const purchasedLettersData = JSON.parse(document.getElementById('purchased-letters-data').textContent);

// Variables globales
let currentFilter = 'all';
let purchasedLetters = purchasedLettersData || [];

// Si no hay datos desde Django, usar datos de ejemplo
if (purchasedLetters.length === 0) {
    purchasedLetters = [
        { letter: 'A', name: 'Letra A', purchaseDate: '2024-01-15', type: 'vocal', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' },
        { letter: 'E', name: 'Letra E', purchaseDate: '2024-01-20', type: 'vocal', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' },
        { letter: 'I', name: 'Letra I', purchaseDate: '2024-01-22', type: 'vocal', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' },
        { letter: 'O', name: 'Letra O', purchaseDate: '2024-01-25', type: 'vocal', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' },
        { letter: 'U', name: 'Letra U', purchaseDate: '2024-01-28', type: 'vocal', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' },
        { letter: 'B', name: 'Letra B', purchaseDate: '2024-01-25', type: 'consonante', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
        { letter: 'C', name: 'Letra C', purchaseDate: '2024-02-01', type: 'consonante', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
        { letter: 'D', name: 'Letra D', purchaseDate: '2024-02-03', type: 'consonante', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
        { letter: 'F', name: 'Letra F', purchaseDate: '2024-02-05', type: 'consonante', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
        { letter: 'G', name: 'Letra G', purchaseDate: '2024-02-07', type: 'consonante', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
        { letter: 'H', name: 'Letra H', purchaseDate: '2024-02-10', type: 'consonante', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
        { letter: 'J', name: 'Letra J', purchaseDate: '2024-02-12', type: 'consonante', bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' }
    ];
}

// Función para formatear fecha
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

// Función para contar vocales y consonantes
function countLettersByType() {
    const vocals = purchasedLetters.filter(letter => letter.type === 'vocal').length;
    const consonants = purchasedLetters.filter(letter => letter.type === 'consonante').length;
    
    return { vocals, consonants };
}

// Función para actualizar las estadísticas
function updateStats() {
    const { vocals, consonants } = countLettersByType();
    
    document.getElementById('totalLetters').textContent = purchasedLetters.length;
    document.getElementById('vocalsCount').textContent = vocals;
    document.getElementById('consonantsCount').textContent = consonants;
}

// Función para filtrar letras
function filterLetters(type) {
    currentFilter = type;
    
    // Actualizar botones activos
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`.filter-btn[data-filter="${type}"]`).classList.add('active');
    
    // Filtrar y renderizar letras
    renderPurchasedLetters();
}

// Función para obtener letras filtradas
function getFilteredLetters() {
    if (currentFilter === 'all') {
        return purchasedLetters;
    }
    return purchasedLetters.filter(letter => letter.type === currentFilter);
}

// Función para renderizar las letras compradas
function renderPurchasedLetters() {
    const purchasedContent = document.getElementById('purchasedContent');
    const filteredLetters = getFilteredLetters();
    
    if (filteredLetters.length === 0) {
        purchasedContent.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🔍</div>
                <h2 class="empty-title">No hay letras en esta categoría</h2>
                <p class="empty-description">No tienes letras compradas en la categoría seleccionada</p>
                <button class="cta-button" onclick="filterLetters('all')">Ver Todas las Letras</button>
            </div>
        `;
        return;
    }
    
    purchasedContent.innerHTML = `
        <div class="letters-grid" id="purchasedGrid">
            <!-- Las letras compradas se generarán con JavaScript -->
        </div>
    `;
    
    const purchasedGrid = document.getElementById('purchasedGrid');
    
    // Renderizar letras compradas
    filteredLetters.forEach(item => {
        const card = createLetterCard(item);
        purchasedGrid.appendChild(card);
    });
    
    // Agregar event listeners a las tarjetas
    document.querySelectorAll('.letter-card').forEach(card => {
        card.addEventListener('click', () => {
            const letterName = card.querySelector('.letter-name').textContent;
            console.log(`Tarjeta clickeada: ${letterName}`);
            // Aquí podrías abrir un modal con más detalles de la letra
        });
    });
}

// Función para crear una tarjeta de letra
function createLetterCard(item) {
    const card = document.createElement('div');
    card.className = 'letter-card';
    
    card.innerHTML = `
        <div class="purchased-badge">COMPRADO</div>
        <div class="letter-display">
            <img src="${item.bg}" alt="${item.name}" class="letter-bg" />
            <span class="letter-text">${item.letter}</span>
        </div>
        <div class="letter-footer">
            <div class="letter-name">${item.name}</div>
            <div class="letter-date">Comprado: ${formatDate(item.purchaseDate)}</div>
        </div>
    `;
    
    return card;
}

// Funcionalidad de búsqueda
document.getElementById('searchInput').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    
    document.querySelectorAll('.letter-card').forEach(card => {
        const letterName = card.querySelector('.letter-name').textContent.toLowerCase();
        card.style.display = letterName.includes(searchTerm) ? 'block' : 'none';
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
    renderPurchasedLetters();
}

// Ejecutar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', initPage);