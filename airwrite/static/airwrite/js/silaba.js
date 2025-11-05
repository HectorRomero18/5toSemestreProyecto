// Obtener los datos del contexto Django
const modules = JSON.parse(document.getElementById('modules-data').textContent);

// Imagen de fondo para todas las sílabas
const bgImage = 'https://c.animaapp.com/mh6mj11rEipEzl/img/italian.png';

// Colores para dificultades
const dificultadColors = {
  'Fácil': '#4CAF50',
  'Media': '#FFC107',
  'Difícil': '#F44336'
};

// Función para renderizar las sílabas
function renderSilabas() {
  const gridElement = document.getElementById('silabasGrid');

  // Limpiar el grid
  gridElement.innerHTML = '';

  // Renderizar todas las sílabas
  modules.forEach(item => {
    const card = createSilabaCard(item);
    gridElement.appendChild(card);
  });

  // Agregar event listeners a los botones de acción
  document.querySelectorAll('.action-btn').forEach(button => {
    button.addEventListener('click', (e) => {
      e.stopPropagation();
      const title = button.getAttribute('title');
      const letterCard = button.closest('.letter-card');
      const letter = button.closest('.letter-card').querySelector('.letter-name').textContent;
      const letterId = letterCard.getAttribute('data-id');

      if (title === 'Escuchar') {
        playSilaba(letter);
      } else if (title === 'Escribir') {
        // Desbloqueada → abrir pantalla de escritura
        Swal.fire({
          icon: 'success',
          title: `Escribir ${letter}`,
          text: '¡Preparando pantalla de escritura!',
          showCancelButton: false,
          confirmButtonText: 'Ir a la pantalla',
          confirmButtonColor: '#3085d6', // color del botón
          didOpen: () => {
              // Opcional: puedes aplicar estilos aquí si quieres
          },
          preConfirm: () => {
              // Redirige al hacer clic en el botón
              window.location.href= `/trazos/${letterId}/`;
          }
        });
      } else if (title === 'Bloqueada') {
        // Letra bloqueada → mensaje SweetAlert
        Swal.fire({
            icon: 'warning',
            title: `${letter} bloqueada`,
            text: 'Desbloquea las letras que conforman esta silaba para poder usarla',
            confirmButtonText: 'Aceptar'
        });
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
  card.setAttribute('data-id', item.id);

  const blockedClass = item.bloqueada ? 'blocked' : '';
  const blockedIcon = item.bloqueada ? `
    <div class="blocked-icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
        <circle cx="12" cy="16" r="1"/>
        <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
      </svg>
    </div>
  ` : '';

  // Botón de bloqueada para todas las sílabas
  const bloqueadaBtn = `
    <button class="action-btn bloqueada" title="Bloqueada">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
        <circle cx="12" cy="16" r="1"/>
        <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
      </svg>
    </button>
  `;

  card.innerHTML = `
    <div class="letter-display ${blockedClass}">
      <img src="${bgImage}" alt="${item.simbolo}" class="letter-bg" />
      <span class="letter-text">${item.silaba}</span>
      ${blockedIcon}
    </div>
    <div class="letter-footer">
      <div class="letter-info">
        <span class="letter-name"> ${item.simbolo}</span>
        <span class="letter-name">Dificultad: </span>
        <span class="letter-name" style="color: ${dificultadColors[item.dificultad]}; font-size: 0.8rem;">
          ${item.dificultad}
        </span>
      </div>
      <div class="letter-actions">
        <button class="action-btn" title="Escuchar" ${item.bloqueada ? 'disabled' : ''}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
              </svg>
        </button>
        ${bloqueadaBtn}
      </div>
    </div>
  `;

  return card;
}

// Función para reproducir sílaba con fetch
async function playSilaba(silaba) {
    try {
        const response = await fetch(`/silabas/play/${silaba}/`);
        if (!response.ok) throw new Error("Error generando audio");
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);
        audio.play();
    } catch (err) {
        console.error(err);
    }
}

// Búsqueda
document.getElementById('searchInput').addEventListener('input', (e) => {
  const searchTerm = e.target.value.toLowerCase();
  document.querySelectorAll('.letter-card').forEach(card => {
    const letterName = card.querySelector('.letter-name').textContent.toLowerCase();
    card.style.display = letterName.includes(searchTerm) ? 'block' : 'none';
  });
});

// Inicializar
document.addEventListener('DOMContentLoaded', renderSilabas);
