// Datos de las letras
const vocales = [
  { letter: 'A', name: 'Letra A', price: 120, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' },
  { letter: 'E', name: 'Letra E', price: 110, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' },
  { letter: 'I', name: 'Letra I', price: 105, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' },
  { letter: 'O', name: 'Letra O', price: 115, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' },
  { letter: 'U', name: 'Letra U', price: 100, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' }
];

const consonantes = [
  { letter: 'B', name: 'Letra B', price: 100, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'C', name: 'Letra C', price: 90, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'D', name: 'Letra D', price: 95, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'F', name: 'Letra F', price: 85, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'G', name: 'Letra G', price: 95, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'H', name: 'Letra H', price: 80, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'J', name: 'Letra J', price: 75, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'K', name: 'Letra K', price: 70, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'L', name: 'Letra L', price: 90, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'M', name: 'Letra M', price: 95, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'N', name: 'Letra N', price: 85, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'Ñ', name: 'Letra Ñ', price: 120, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'P', name: 'Letra P', price: 85, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'Q', name: 'Letra Q', price: 95, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'R', name: 'Letra R', price: 90, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'S', name: 'Letra S', price: 85, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'T', name: 'Letra T', price: 80, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'V', name: 'Letra V', price: 85, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'W', name: 'Letra W', price: 95, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'X', name: 'Letra X', price: 100, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'Y', name: 'Letra Y', price: 90, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'Z', name: 'Letra Z', price: 85, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' }
];

// Función para renderizar las letras
function renderLetters() {
  const vocalesGrid = document.getElementById('vocalesGrid');
  const consonantesGrid = document.getElementById('consonantesGrid');
  
  vocalesGrid.innerHTML = '';
  consonantesGrid.innerHTML = '';
  
  // Renderizar vocales
  vocales.forEach(item => {
    const card = createLetterCard(item);
    vocalesGrid.appendChild(card);
  });
  
  // Renderizar consonantes
  consonantes.forEach(item => {
    const card = createLetterCard(item);
    consonantesGrid.appendChild(card);
  });
  
  // Agregar event listeners a los botones de acción
  document.querySelectorAll('.action-btn').forEach(button => {
    button.addEventListener('click', (e) => {
      e.stopPropagation();
      const title = button.getAttribute('title');
      console.log(`Acción: ${title}`);
      
      // Aquí puedes agregar la funcionalidad específica para cada acción
      if (title === 'Comprar') {
        alert(`Comprar ${button.closest('.letter-card').querySelector('.letter-name').textContent}`);
      } else if (title === 'Escuchar') {
        alert(`Reproducir sonido de ${button.closest('.letter-card').querySelector('.letter-name').textContent}`);
      } else if (title === 'Escribir') {
        alert(`Abrir pantalla de escritura para ${button.closest('.letter-card').querySelector('.letter-name').textContent}`);
      }
    });
  });
  
  // Agregar event listeners a las tarjetas
  document.querySelectorAll('.letter-card').forEach(card => {
    card.addEventListener('click', () => {
      const letterName = card.querySelector('.letter-name').textContent;
      console.log(`Tarjeta clickeada: ${letterName}`);
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

// Funcionalidad de búsqueda
document.getElementById('searchInput').addEventListener('input', (e) => {
  const searchTerm = e.target.value.toLowerCase();
  
  document.querySelectorAll('.letter-card').forEach(card => {
    const letterName = card.querySelector('.letter-name').textContent.toLowerCase();
    card.style.display = letterName.includes(searchTerm) ? 'block' : 'none';
  });
});



// Inicializar la página cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', renderLetters);