// Datos de las sílabas - solo con A y E
const silabas = [
  // Sílabas con B
  { silaba: 'BA', name: 'Sílaba BA', price: 120 },
  { silaba: 'BE', name: 'Sílaba BE', price: 110 },
  
  // Sílabas con C
  { silaba: 'CA', name: 'Sílaba CA', price: 115 },
  { silaba: 'CE', name: 'Sílaba CE', price: 105 },
  
  // Sílabas con D
  { silaba: 'DA', name: 'Sílaba DA', price: 100 },
  { silaba: 'DE', name: 'Sílaba DE', price: 95 },
  
  // Sílabas con F
  { silaba: 'FA', name: 'Sílaba FA', price: 90 },
  { silaba: 'FE', name: 'Sílaba FE', price: 85 },
  
  // Sílabas con G
  { silaba: 'GA', name: 'Sílaba GA', price: 95 },
  { silaba: 'GE', name: 'Sílaba GE', price: 90 },
  
  // Sílabas con H
  { silaba: 'HA', name: 'Sílaba HA', price: 80 },
  { silaba: 'HE', name: 'Sílaba HE', price: 75 },
  
  // Sílabas con J
  { silaba: 'JA', name: 'Sílaba JA', price: 85 },
  { silaba: 'JE', name: 'Sílaba JE', price: 80 },
  
  // Sílabas con K
  { silaba: 'KA', name: 'Sílaba KA', price: 75 },
  { silaba: 'KE', name: 'Sílaba KE', price: 70 },
  
  // Sílabas con L
  { silaba: 'LA', name: 'Sílaba LA', price: 90 },
  { silaba: 'LE', name: 'Sílaba LE', price: 85 },
  
  // Sílabas con M
  { silaba: 'MA', name: 'Sílaba MA', price: 95 },
  { silaba: 'ME', name: 'Sílaba ME', price: 90 },
  
  // Sílabas con N
  { silaba: 'NA', name: 'Sílaba NA', price: 85 },
  { silaba: 'NE', name: 'Sílaba NE', price: 80 },
  
  // Sílabas con Ñ
  { silaba: 'ÑA', name: 'Sílaba ÑA', price: 100 },
  { silaba: 'ÑE', name: 'Sílaba ÑE', price: 95 },
  
  // Sílabas con P
  { silaba: 'PA', name: 'Sílaba PA', price: 85 },
  { silaba: 'PE', name: 'Sílaba PE', price: 80 },
  
  // Sílabas con Q
  { silaba: 'QA', name: 'Sílaba QA', price: 95 },
  { silaba: 'QE', name: 'Sílaba QE', price: 90 },
  
  // Sílabas con R
  { silaba: 'RA', name: 'Sílaba RA', price: 90 },
  { silaba: 'RE', name: 'Sílaba RE', price: 85 },
  
  // Sílabas con S
  { silaba: 'SA', name: 'Sílaba SA', price: 85 },
  { silaba: 'SE', name: 'Sílaba SE', price: 80 },
  
  // Sílabas con T
  { silaba: 'TA', name: 'Sílaba TA', price: 80 },
  { silaba: 'TE', name: 'Sílaba TE', price: 75 },
  
  // Sílabas con V
  { silaba: 'VA', name: 'Sílaba VA', price: 85 },
  { silaba: 'VE', name: 'Sílaba VE', price: 80 },
  
  // Sílabas con W
  { silaba: 'WA', name: 'Sílaba WA', price: 95 },
  { silaba: 'WE', name: 'Sílaba WE', price: 90 },
  
  // Sílabas con X
  { silaba: 'XA', name: 'Sílaba XA', price: 100 },
  { silaba: 'XE', name: 'Sílaba XE', price: 95 },
  
  // Sílabas con Y
  { silaba: 'YA', name: 'Sílaba YA', price: 90 },
  { silaba: 'YE', name: 'Sílaba YE', price: 85 },
  
  // Sílabas con Z
  { silaba: 'ZA', name: 'Sílaba ZA', price: 85 },
  { silaba: 'ZE', name: 'Sílaba ZE', price: 80 }
];

// Imagen de fondo para todas las sílabas
const bgImage = 'https://c.animaapp.com/mh6mj11rEipEzl/img/italian.png';

// Función para renderizar las sílabas
function renderSilabas() {
  const gridElement = document.getElementById('silabasGrid');
  
  // Limpiar el grid
  gridElement.innerHTML = '';
  
  // Renderizar todas las sílabas
  silabas.forEach(item => {
    const card = createSilabaCard(item);
    gridElement.appendChild(card);
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
      const silabaName = card.querySelector('.letter-name').textContent;
      console.log(`Tarjeta clickeada: ${silabaName}`);
    });
  });
}

// Función para crear una tarjeta de sílaba
function createSilabaCard(item) {
  const card = document.createElement('div');
  card.className = 'letter-card';
  
  card.innerHTML = `
    <div class="letter-display">
      <img src="${bgImage}" alt="${item.name}" class="letter-bg" />
      <span class="letter-text">${item.silaba}</span>
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
    const silabaName = card.querySelector('.letter-name').textContent.toLowerCase();
    const silabaText = card.querySelector('.letter-text').textContent.toLowerCase();
    
    // Mostrar u ocultar según coincidencia en nombre o texto
    card.style.display = (silabaName.includes(searchTerm) || silabaText.includes(searchTerm)) ? 'block' : 'none';
  });
});


// Inicializar la página
document.addEventListener('DOMContentLoaded', renderSilabas);