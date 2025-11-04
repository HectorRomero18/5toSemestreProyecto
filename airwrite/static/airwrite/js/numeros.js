// =====================
// números.js usando datos de Django
// =====================

// Obtener datos desde Django
const numbersData = JSON.parse(document.getElementById('modules-data').textContent);

// Imagen de fondo para todos los números
const bgImage = 'https://c.animaapp.com/mh6mj11rEipEzl/img/italian.png';

//  Función para renderizar los números
function renderNumbers() {
  const gridElement = document.getElementById('numbersGrid');
  
  // Limpiar el grid
  gridElement.innerHTML = '';
  
  // Renderizar todos los números
  numbersData.forEach(item => {
    const card = createNumberCard(item);
    gridElement.appendChild(card);
  });
  
  // Agregar event listeners a los botones de acción
  document.querySelectorAll('.action-btn').forEach(button => {
    button.addEventListener('click', (e) => {
      e.stopPropagation();
      const title = button.getAttribute('title');
      const numberName = button.closest('.number-card').querySelector('.number-name').textContent;

      if (title === 'Comprar') {
        alert(`Comprar ${numberName}`);
      } else if (title === 'Escuchar') {
        const numberText = button.closest('.number-card').querySelector('.number-text').textContent.trim();

        fetch(`/numeros/play/${encodeURIComponent(numberText)}/`)
          .then(response => {
            if (!response.ok) throw new Error('Error generando audio');
            return response.blob();
          })
          .then(blob => {
            const url = URL.createObjectURL(blob);
            const audio = new Audio(url);
            audio.play();
          })
          .catch(err => {
            console.error('Error al reproducir número:', err);
            alert('No se pudo generar el audio. Revisa consola del servidor para más detalles.');
          });
      } else if (title === 'Escribir') {
        alert(`Abrir pantalla de escritura para ${numberName}`);
      }
    });
  });
  
  // Click en cada tarjeta
  document.querySelectorAll('.number-card').forEach(card => {
    card.addEventListener('click', () => {
      const numberName = card.querySelector('.number-name').textContent;
      console.log(`Tarjeta clickeada: ${numberName}`);
    });
  });
}

// Función para crear tarjeta
function createNumberCard(item) {
  const card = document.createElement('div');
  card.className = 'number-card';

  const dificultadColors = {
    'Fácil': '#4CAF50',
    'Media': '#FFC107',
    'Difícil': '#F44336'
  };

  card.innerHTML = `
    <div class="number-display">
      <img src="${bgImage}" alt="${item.name || `${item.numero}`}" class="number-bg" />
      <span class="number-text">${item.simbolo}</span>
    </div>
    <div class="number-footer">
      <div class="number-info">
        <span class="number-name">${item.name || `${item.numero}`}</span>
        <span class="number-dificultad" 
              style="display: block; color: ${dificultadColors[item.dificultad] || '#999'}; font-size: 0.8rem;">
          Dificultad: ${item.dificultad || 'Desconocida'}
        </span>
      </div>
      <div class="number-actions">
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

//  Búsqueda
document.getElementById('searchInput').addEventListener('input', (e) => {
  const searchTerm = e.target.value.toLowerCase();
  
  document.querySelectorAll('.number-card').forEach(card => {
    const numberName = card.querySelector('.number-name').textContent.toLowerCase();
    const numberText = card.querySelector('.number-text').textContent.toLowerCase();
    
    card.style.display = (numberName.includes(searchTerm) || numberText.includes(searchTerm)) ? 'block' : 'none';
  });
});

// Inicializar
document.addEventListener('DOMContentLoaded', renderNumbers);
