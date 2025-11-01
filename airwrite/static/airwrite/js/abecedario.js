// 1️⃣ Obtener los datos del contexto Django
const modules = JSON.parse(document.getElementById('modules-data').textContent);

// 2️⃣ Separar vocales y consonantes según la categoría
const vocales = modules.filter(item => item.categoria === 'V');
const consonantes = modules.filter(item => item.categoria === 'C');

// 3️⃣ Función para obtener imagen según categoría o dificultad
function obtenerFondo(letra) {
  // Puedes personalizar esto como quieras:
  if (letra.categoria === 'V') {
    return 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png';
  } else {
    return 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png';
  }
}

// 4️⃣ Función para crear una tarjeta de letra (tu mismo diseño)
function createLetterCard(item) {
  const card = document.createElement('div');
  card.className = 'letter-card';
  
  const bg = obtenerFondo(item);
  const dificultadColors = {
    'Fácil': '#4CAF50',   // verde
    'Media': '#FFC107',   // amarillo / ámbar
    'Difícil': '#F44336'  // rojo
  };

  card.innerHTML = `
    <div class="letter-display">
      <img src="${bg}" alt="${item.simbolo}" class="letter-bg" />
      <span class="letter-text">${item.simbolo}</span>
    </div>
    <div class="letter-footer">
      <!-- Wrapper vertical para letra y dificultad -->
      <div class="letter-info">
        <span class="letter-name">${item.letter}</span>
          <span class="letter-name">Dificultad: </span>
          <span class="letter-name" style="color: ${dificultadColors[item.dificultad]}; font-size: 0.8rem;">
            ${item.dificultad}
          </span>

      </div>

      <!-- Botones de acción -->
      <div class="letter-actions">
        <button class="action-btn" title="Escuchar">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
          </svg>
        </button>
        <button class="action-btn" title="Escribir">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>
          </svg>
        </button>
        <button class="action-btn" title="Comprar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="9" cy="21" r="1"/>
            <circle cx="20" cy="21" r="1"/>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
          </svg>
        </button>
      </div>
    </div>
  `;

  return card;
}


// 5️⃣ Renderizar todas las letras
function renderLetters() {
  const vocalesGrid = document.getElementById('vocalesGrid');
  const consonantesGrid = document.getElementById('consonantesGrid');

  vocalesGrid.innerHTML = '';
  consonantesGrid.innerHTML = '';

  vocales.forEach(item => vocalesGrid.appendChild(createLetterCard(item)));
  consonantes.forEach(item => consonantesGrid.appendChild(createLetterCard(item)));

  // Acciones de botones
  document.querySelectorAll('.action-btn').forEach(button => {
    button.addEventListener('click', (e) => {
      e.stopPropagation();
      const title = button.getAttribute('title');
      const letter = button.closest('.letter-card').querySelector('.letter-name').textContent;

      if (title === 'Comprar') {
        alert(`Comprar ${letter}`);
      } else if (title === 'Escuchar') {
        alert(`Escuchar ${letter}`);
      } else if (title === 'Escribir') {
        alert(`Abrir pantalla de escritura para ${letter}`);
      }
    });
  });
}

// 6️⃣ Búsqueda
document.getElementById('searchInput').addEventListener('input', (e) => {
  const searchTerm = e.target.value.toLowerCase();
  document.querySelectorAll('.letter-card').forEach(card => {
    const letterName = card.querySelector('.letter-name').textContent.toLowerCase();
    card.style.display = letterName.includes(searchTerm) ? 'block' : 'none';
  });
});

// 7️⃣ Inicializar al cargar
document.addEventListener('DOMContentLoaded', renderLetters);
