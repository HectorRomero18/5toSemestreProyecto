document.addEventListener('DOMContentLoaded', () => { 
  // Obtener datos del contexto Django
  const modules = JSON.parse(document.getElementById('modules-data').textContent);
  const compradas = JSON.parse(document.getElementById('compradas-data').textContent)
                        .map(l => l.toLowerCase());

  let currentFilter = 'all';
  const favorites = {};
  let currentFeatured = null;

  // ----------cargar favoritos desde localStorage ----------
  const savedFavorites = JSON.parse(localStorage.getItem('favorites')) || {};
  Object.assign(favorites, savedFavorites);

  function getItemKey(itemOrLetter) {
    if (!itemOrLetter) return null;
    if (typeof itemOrLetter === 'string') return itemOrLetter.toLowerCase();
    return (itemOrLetter.letter || itemOrLetter.simbolo || '').toLowerCase();
  }

  function isPurchased(item) {
    const key = getItemKey(item);
    return key && compradas.includes(key);
  }

  const dificultadColors = {
    'Fácil': '#4CAF50',
    'Media': '#FFC107',
    'Difícil': '#F44336'
  };

  function obtenerFondo(letra) {
    return letra.categoria === 'Vocales'
      ? 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-1.png'
      : 'https://c.animaapp.com/mh6mj11rEipEzl/img/group-4.png';
  }

  function getCSRFToken() {
    let cookieValue = null;
    const name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach(cookie => {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
      });
    }
    return cookieValue;
  }

  function createLetterCard(item) {
    const card = document.createElement('div');
    card.className = 'letter-card';
    const letra = item.letter;
    const resultado = letra.charAt(0).toUpperCase() + letra.slice(1, -1) + letra.slice(-1).toUpperCase();

   card.innerHTML = `
      <div class="letter-display">
        <img src="${obtenerFondo(item)}" alt="${item.simbolo}" class="letter-bg" />
        <span class="letter-text">${item.letra_obj}</span>
      </div>
      <div class="letter-footer">
        <div class="letter-info">
          <span class="letter-name" style="display:block;">${resultado}</span>
          <span class="letter-name" style="display:block; font-size:0.8rem; color:${dificultadColors[item.dificultad] || '#999'}">
            Dificultad: ${item.dificultad}
          </span>
        </div>
        <div class="letter-actions">
          <!-- Agregamos data-letra-id -->
          <button class="btn-favorite-small ${favorites[item.letter] ? 'active' : ''}" 
                  data-nombre="${item.letter}" 
                  data-letra-id="${item.id}">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="${favorites[item.letter] ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
              <path d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.219l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z"/>
            </svg>
          </button>
        </div>
      </div>
    `;

    // Listener para el botón de favorito
    const favBtn = card.querySelector('.btn-favorite-small');
    favBtn.onclick = async (e) => {
      e.stopPropagation(); // Evita que también se dispare el click del card
      const letraId = favBtn.dataset.letraId; 
      const nombre = favBtn.dataset.nombre;
      if (!letraId) return;
      console.log(`Boton presionado para ${nombre}, ID: ${letraId}`);

      const isFavorite = favBtn.classList.contains('active');

      try {
        if (isFavorite) {
          // Quitar favorito
          const resp = await fetch('/favoritos/delete/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCSRFToken(),
              },
              body: JSON.stringify({ letra_id: letraId }),
          });
          const data = await resp.json();
          if (data.status) {
              favBtn.classList.remove('active');
              favBtn.querySelector('svg').setAttribute('fill', 'none'); // actualizar el corazón
              delete favorites[nombre]; // eliminar del objeto de favoritos
          } else {
              console.error('Error del servidor:', data.error);
          }
        } else {
          // Agregar favorito
          const resp = await fetch('/favoritos/add/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ nombre }),
          });
          const data = await resp.json();
          if (data.status) {
            favBtn.classList.add('active');
            favBtn.querySelector('svg').setAttribute('fill', 'currentColor');
            favorites[nombre] = true;
          } else console.error('Error del servidor:', data.error);
        }
      } catch (err) {
        console.error('Error al actualizar favorito:', err);
      }

      localStorage.setItem('favorites', JSON.stringify(favorites));
    };


    card.addEventListener('click', () => {
      updateFeaturedCard(item);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    return card;
  }

  function renderLetters() {
    const lettersGrid = document.getElementById('lettersGrid');
    lettersGrid.innerHTML = '';
    modules
      .filter(item => {
        if (currentFilter === 'vowel') return item.categoria === 'Vocales';
        if (currentFilter === 'consonant') return item.categoria === 'Consonantes';
        return true;
      })
      .forEach(item => lettersGrid.appendChild(createLetterCard(item)));
  }

  function updateFeaturedCard(item) {
    currentFeatured = item;
    const featuredCard = document.getElementById('featuredCard');
    const featuredLetter = document.getElementById('featuredLetter');
    const featuredInfo = document.getElementById('featuredInfo');

    featuredLetter.textContent = item.letra_obj;
    const letra = item.letter;
    const resultado = letra.charAt(0).toUpperCase() + letra.slice(1, -1) + letra.slice(-1).toUpperCase();

    featuredInfo.querySelector('.featured-title').textContent = resultado;
    featuredInfo.querySelector('.featured-categoria').textContent = `Categoria: ${item.categoria}`;
    featuredInfo.querySelector('.featured-price').textContent = `Precio: ${item.price} XP`;

    featuredCard.style.background = item.categoria === 'Vocales'
      ? 'linear-gradient(135deg, #3B9EFF 0%, #2B7FD9 100%)'
      : 'linear-gradient(135deg, #FFC107 0%, #FFB300 100%)';

    const buyBtn = document.querySelector('.btn-buy');
    if (isPurchased(item)) {
      buyBtn.textContent = 'Obtenido';
      buyBtn.disabled = true;
    } else {
      buyBtn.textContent = 'Obtener';
      buyBtn.disabled = false;
    }

    // ---------- Sincronizar corazón del featured con favoritos ----------
    const featuredFavBtn = document.getElementById('featuredFavorite');
    if (favorites[item.letter]) {
      featuredFavBtn.classList.add('active');
      featuredFavBtn.querySelector('svg').setAttribute('fill', 'currentColor');
    } else {
      featuredFavBtn.classList.remove('active');
      featuredFavBtn.querySelector('svg').setAttribute('fill', 'none');
    }

    // ---------- Evento eliminar/agregar del featured ----------
    featuredFavBtn.onclick = async () => {
      const nombre = item.letter;
      if (!nombre) return;

      const isFavorite = featuredFavBtn.classList.contains('active');

      try {
        if (isFavorite) {
          const resp = await fetch('/favoritos/delete/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ letra_id: item.id }),
          });
          const data = await resp.json();
          if (data.status) {
            featuredFavBtn.classList.remove('active');
            featuredFavBtn.querySelector('svg').setAttribute('fill', 'none');
            delete favorites[nombre];
          } else console.error('Error del servidor:', data.error);
        } else {
          const resp = await fetch('/favoritos/add/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ nombre }),
          });
          const data = await resp.json();
          if (data.status) {
            featuredFavBtn.classList.add('active');
            featuredFavBtn.querySelector('svg').setAttribute('fill', 'currentColor');
            favorites[nombre] = true;
          } else console.error('Error del servidor:', data.error);
        }
      } catch (err) {
        console.error('Error al actualizar favorito:', err);
      }

      localStorage.setItem('favorites', JSON.stringify(favorites));
    };
  }

  document.querySelectorAll('.btn-category').forEach(btn => {
    btn.addEventListener('click', () => {
      currentFilter = btn.dataset.filter;
      renderLetters();
      document.querySelectorAll('.btn-category').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  document.getElementById('searchInput').addEventListener('input', e => {
    const searchTerm = e.target.value.toLowerCase();
    document.querySelectorAll('.letter-card').forEach(card => {
      const letterName = card.querySelector('.letter-name').textContent.toLowerCase();
      card.style.display = letterName.includes(searchTerm) ? 'block' : 'none';
    });
  });

  document.querySelector('.btn-buy').addEventListener('click', () => {
    if (!currentFeatured) return;
    const featuredLetter = document.getElementById('featuredLetter').textContent;
    const priceText = document.querySelector('.featured-price').textContent;
    const price = parseInt(priceText.replace(/\D/g, ''));

    Swal.fire({
      title: `Comprar ${featuredLetter}?`,
      text: `Esta letra cuesta ${price} XP.`,
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'Sí, comprar',
      cancelButtonText: 'Cancelar'
    }).then(result => {
      if (result.isConfirmed) {
        const letraKey = encodeURIComponent(
          currentFeatured?.simbolo || currentFeatured?.caracter || currentFeatured?.letter || featuredLetter
        );
        fetch('/tiendaXp/comprar/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
          },
          body: `letra=${letraKey}&precio=${price}`
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            Swal.fire('¡Compra realizada!', data.message, 'success');
            document.querySelector('.xp-badge').textContent = `${data.user_xp}Xp`;
            const key = getItemKey(currentFeatured || featuredLetter);
            if (key && !compradas.includes(key)) compradas.push(key);
            const buyBtn = document.querySelector('.btn-buy');
            buyBtn.textContent = 'Comprado';
            buyBtn.disabled = true;
          } else {
            Swal.fire('Error', data.message, 'error');
          }
        })
        .catch(() => Swal.fire('Error', 'No se pudo procesar la compra', 'error'));
      }
    });
  });

  renderLetters();
  if (modules.length > 0) updateFeaturedCard(modules[0]);
});
