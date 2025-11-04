// =====================
// comprada.js
// =====================

const purchasedLettersData = JSON.parse(document.getElementById('modules-data').textContent);

// Transformar datos para que tengan los mismos campos que tu JS
let purchasedLetters = purchasedLettersData.map(item => ({
    letter: item.simbolo,
    name: item.nombre || `${item.letra}`,
    purchaseDate: item.fecha,
    type: item.tipo || 'V',
    bg: item.bg || 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' // placeholder si no hay imagen
}));

// Variables globales
let currentFilter = 'all';

// Función para formatear fecha
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

// Contar vocales y consonantes
function countLettersByType() {
    const vocals = purchasedLetters.filter(letter => letter.type === 'V').length;
    const consonants = purchasedLetters.filter(letter => letter.type === 'C').length;
    return { vocals, consonants };
}

// Actualizar estadísticas en el DOM
function updateStats() {
    const { vocals, consonants } = countLettersByType();
    document.getElementById('totalLetters').textContent = purchasedLetters.length;
    document.getElementById('vocalsCount').textContent = vocals;
    document.getElementById('consonantsCount').textContent = consonants;
}

//  Filtrar letras por tipo
function filterLetters(type) {
    currentFilter = type;

    // Actualizar botones activos
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`.filter-btn[data-filter="${type}"]`)?.classList.add('active');

    // Renderizar letras filtradas
    renderPurchasedLetters();
}

//  Obtener letras filtradas según el filtro actual
function getFilteredLetters() {
    if (currentFilter === 'all') return purchasedLetters;
    // Mapear el filtro al valor que envio desde Django
    const typeMap = {
        'vocal': 'V',
        'consonante': 'C'
    };
    return purchasedLetters.filter(letter => letter.type === typeMap[currentFilter]);
}

// Renderizar letras en el grid
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

    purchasedContent.innerHTML = `<div class="letters-grid" id="purchasedGrid"></div>`;
    const purchasedGrid = document.getElementById('purchasedGrid');

    filteredLetters.forEach(item => {
        const card = createLetterCard(item);
        purchasedGrid.appendChild(card);
    });

    // Agregar click a cada tarjeta
    document.querySelectorAll('.letter-card').forEach(card => {
        card.addEventListener('click', () => {
            const letterName = card.querySelector('.letter-name').textContent;
            console.log(`Tarjeta clickeada: ${letterName}`);
            // Aquí podrías abrir un modal con más detalles de la letra
        });
    });
}

// Crear tarjeta de letra
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

// Event listeners a botones de filtro
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const filterType = btn.getAttribute('data-filter');
        filterLetters(filterType);
    });
});

//  Inicializar página
function initPage() {
    updateStats();
    renderPurchasedLetters();
}

// Ejecutar al cargar DOM
document.addEventListener('DOMContentLoaded', initPage);
