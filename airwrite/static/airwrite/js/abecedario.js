// Obtener los datos del contexto Django
const modules = JSON.parse(document.getElementById('modules-data').textContent);

// Separar vocales y consonantes según la categoría
const vocales = modules.filter(item => item.categoria === 'V');
const consonantes = modules.filter(item => item.categoria === 'C');

//  Función para obtener imagen según categoría
function obtenerFondo(letra) {
  if (letra.categoria === 'V') {
    return 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png';
  } else {
    return 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png';
  }
}

// Crear tarjeta de letra
function createLetterCard(item) {
  const card = document.createElement('div');
  card.className = 'letter-card';

  const bg = obtenerFondo(item);
  const dificultadColors = {
    'Fácil': '#4CAF50',
    'Media': '#FFC107',
    'Difícil': '#F44336'
  };

  // Decide el botón de escribir según si está bloqueada
  let escribirBtn = '';
  if (!item.bloqueada) {
    // Desbloqueada → lápiz
    console.log("Letra desbloqueada:", item.bloqueada);
    escribirBtn = `
      <button class="action-btn" title="Escribir">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>
        </svg>
      </button>
    `;
  } else {
    // Bloqueada → candado
    escribirBtn = `
      <button class="action-btn bloqueada" title="Bloqueada">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>
      </button>
    `;
  }

  card.innerHTML = `
    <div class="letter-display">
      <img src="${bg}" alt="${item.simbolo}" class="letter-bg" />
      <span class="letter-text">${item.simbolo}</span>
    </div>
    <div class="letter-footer">
      <div class="letter-info">
        <span class="letter-name">${item.letter}</span>
        <span class="letter-name">Dificultad: </span>
        <span class="letter-name" style="color: ${dificultadColors[item.dificultad]}; font-size: 0.8rem;">
          ${item.dificultad}
        </span>
      </div>
      <div class="letter-actions">
        <button class="action-btn" title="Escuchar">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
          </svg>
        </button>
        ${escribirBtn}
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


// Renderizar letras y agregar eventos
function renderLetters() {
  const vocalesGrid = document.getElementById('vocalesGrid');
  const consonantesGrid = document.getElementById('consonantesGrid');

  vocalesGrid.innerHTML = '';
  consonantesGrid.innerHTML = '';

  vocales.forEach(item => vocalesGrid.appendChild(createLetterCard(item)));
  consonantes.forEach(item => consonantesGrid.appendChild(createLetterCard(item)));

  // Eventos botones
  document.querySelectorAll('.action-btn').forEach(button => {
      button.addEventListener('click', (e) => {
          e.stopPropagation();
          const title = button.getAttribute('title');
          const letter = button.closest('.letter-card').querySelector('.letter-name').textContent;

          if (title === 'Escuchar') {
              playLetter(letter);
          } else if (title === 'Comprar') {
              window.location.href = '/tienda/'
          } else if (title === 'Escribir') {
              // Desbloqueada → abrir pantalla de escritura
              Swal.fire({
                  icon: 'success',
                  title: `Escribir ${letter}`,
                  text: '¡Preparando pantalla de escritura!',
              });
          } else if (title === 'Bloqueada') {
              // Letra bloqueada → mensaje SweetAlert
              Swal.fire({
                  icon: 'warning',
                  title: `${letter} bloqueada`,
                  text: 'Desbloquea o compra esta letra para poder usarla',
                  confirmButtonText: 'Aceptar'
              });
          }
      });
  });

}

// Búsqueda
document.getElementById('searchInput').addEventListener('input', (e) => {
  const searchTerm = e.target.value.toLowerCase();
  document.querySelectorAll('.letter-card').forEach(card => {
    const letterName = card.querySelector('.letter-name').textContent.toLowerCase();
    card.style.display = letterName.includes(searchTerm) ? 'block' : 'none';
  });
});

// Función para reproducir letra con fetch
async function playLetter(letter) {
    try {
        const response = await fetch(`/abecedario/letters/play/${letter}/`);
        if (!response.ok) throw new Error("Error generando audio");
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);
        audio.play();
    } catch (err) {
        console.error(err);
    }
}

// Modificar el listener de botones "Escuchar"
document.querySelectorAll('.action-btn').forEach(button => {
    button.addEventListener('click', (e) => {
        e.stopPropagation();
        const title = button.getAttribute('title');
        const letter = button.closest('.letter-card').querySelector('.letter-name').textContent;

        if (title === 'Escuchar') {
            playLetter(letter);
        } else if (title === 'Comprar') {
            alert(`Comprar ${letter}`);
        } else if (title === 'Escribir') {
            alert(`Abrir pantalla de escritura para ${letter}`);
        }
    });
});


// Inicializar
document.addEventListener('DOMContentLoaded', renderLetters);
