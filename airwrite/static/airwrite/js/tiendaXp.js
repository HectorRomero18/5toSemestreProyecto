// Datos de las letras
const letters = [
  { letter: 'A', name: 'Letra A', vowel: true, price: 120, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' },
  { letter: 'B', name: 'Letra B', vowel: false, price: 100, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'C', name: 'Letra C', vowel: false, price: 90, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'D', name: 'Letra D', vowel: false, price: 95, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'E', name: 'Letra E', vowel: true, price: 110, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' },
  { letter: 'F', name: 'Letra F', vowel: false, price: 85, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'G', name: 'Letra G', vowel: false, price: 95, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'H', name: 'Letra H', vowel: false, price: 80, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'I', name: 'Letra I', vowel: true, price: 105, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png' },
  { letter: 'J', name: 'Letra J', vowel: false, price: 75, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'K', name: 'Letra K', vowel: false, price: 70, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'L', name: 'Letra L', vowel: false, price: 90, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' },
  { letter: 'M', name: 'Letra M', vowel: false, price: 95, bg: 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png' }
];

const favorites = {};
let currentFilter = 'all';
let currentLetter = letters[0];

function updateFeaturedCard() {
  const featuredCard = document.getElementById('featuredCard');
  const featuredLetter = document.getElementById('featuredLetter');
  const featuredInfo = document.getElementById('featuredInfo');
  
  // Aplicar animación de cambio suave
  featuredCard.classList.add('changing');
  featuredLetter.classList.add('changing');
  featuredInfo.classList.add('changing');
  
  // Aplicar color según si es vocal o consonante
  if (currentLetter.vowel) {
    featuredCard.style.background = 'linear-gradient(135deg, #3B9EFF 0%, #2B7FD9 100%)';
  } else {
    featuredCard.style.background = 'linear-gradient(135deg, #FFC107 0%, #FFB300 100%)';
  }
  
  // Actualizar contenido después de un pequeño delay para que coincida con la animación
  setTimeout(() => {
    featuredLetter.textContent = currentLetter.letter;
    document.querySelector('.featured-title').textContent = currentLetter.name;
    document.querySelector('.featured-price').textContent = `Precio ${currentLetter.price} Xp`;
    
    // Remover clases de animación después de que termine
    setTimeout(() => {
      featuredCard.classList.remove('changing');
      featuredLetter.classList.remove('changing');
      featuredInfo.classList.remove('changing');
    }, 600);
  }, 100);
}

function renderLetters() {
  const lettersGrid = document.getElementById('lettersGrid');
  lettersGrid.innerHTML = '';

  letters.forEach((item, index) => {
    if (currentFilter !== 'all') {
      if (currentFilter === 'vowel' && !item.vowel) return;
      if (currentFilter === 'consonant' && item.vowel) return;
    }

    const card = document.createElement('div');
    card.className = 'letter-card';
    card.addEventListener('click', () => {
      currentLetter = item;
      updateFeaturedCard();
    });
    card.innerHTML = `
      <div class="letter-display">
        <img src="${item.bg}" alt="${item.name}" class="letter-bg" />
        <span class="letter-text">${item.letter}</span>
      </div>
      <div class="letter-footer">
        <span class="letter-name">${item.name}</span>
        <button class="btn-favorite-small ${favorites[index] ? 'active' : ''}" data-index="${index}">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="${favorites[index] ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
            <path d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.219l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z"/>
          </svg>
        </button>
      </div>
    `;
    lettersGrid.appendChild(card);
  });

  document.querySelectorAll('.btn-favorite-small').forEach(btn => {
    btn.addEventListener('click', handleFavoriteClick);
  });
}

function handleFavoriteClick(e) {
  e.stopPropagation();
  const btn = e.currentTarget;
  const index = btn.dataset.index;
  
  favorites[index] = !favorites[index];
  renderLetters();
}

document.querySelectorAll('.sidebar-item').forEach(item => {
  item.addEventListener('click', () => {
    document.querySelectorAll('.sidebar-item').forEach(nav => nav.classList.remove('active'));
    item.classList.add('active');
  });
});

document.querySelectorAll('.btn-category').forEach(btn => {
  btn.addEventListener('click', () => {
    currentFilter = btn.dataset.filter;
    renderLetters();
  });
});

document.getElementById('searchInput').addEventListener('input', (e) => {
  const searchTerm = e.target.value.toLowerCase();
  document.querySelectorAll('.letter-card').forEach(card => {
    const letterName = card.querySelector('.letter-name').textContent.toLowerCase();
    card.style.display = letterName.includes(searchTerm) ? 'block' : 'none';
  });
});

document.getElementById('featuredFavorite').addEventListener('click', function() {
  this.classList.toggle('active');
});

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
  updateFeaturedCard();
  renderLetters();
});