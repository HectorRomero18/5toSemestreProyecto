// document.addEventListener("DOMContentLoaded", () => {
//   const greeting = document.querySelector(".p");
//   const username = greeting.dataset.username;

//   // 🔹 Frases en un array
//   const frases = [
//     `Hola, ${username}! 👋`, // ← primera frase personalizada
//     (() => {
//       const hour = new Date().getHours();
//       if (hour >= 5 && hour < 12) return "Buenos días ☀️";
//       else if (hour >= 12 && hour < 18) return "Buenas tardes 🌤️";
//       else return "Buenas noches 🌙";
//     })(),
//     "Vamos a trazar",
//     "Notas que flotan",
//     "Inspírate y crea",
//     "Flota con tus ideas",
//     "Imagina y hazlo",
//   ];

//   let index = 0;

//   const mostrarFrase = () => {
//     greeting.classList.remove("fade-in", "fade-out");
//     greeting.textContent = frases[index];
//     greeting.classList.add("fade-in");

//     setTimeout(() => {
//       greeting.classList.remove("fade-in");
//       greeting.classList.add("fade-out");

//       setTimeout(() => {
//         index++;
//         if (index < frases.length) {
//           mostrarFrase();
//         }
//       }, 730); // duración fade-out
//     }, 3000); // duración frase visible
//   };

//   mostrarFrase();
// });

    // Obtener el día actual de la semana (0 = Domingo, 1 = Lunes, etc.)
    const today = new Date().getDay();
    const todayIndex = today === 0 ? 6 : today - 1; // Convertir a índice (Lun=0, Dom=6)

    // Inicializar datos de actividad con 0 minutos para todos los días
    const activityData = {
      week: [
        { label: 'Lun', minutes: 0, dayIndex: 0 },
        { label: 'Mart', minutes: 0, dayIndex: 1 },
        { label: 'Mier', minutes: 0, dayIndex: 2 },
        { label: 'Juev', minutes: 0, dayIndex: 3 },
        { label: 'Vier', minutes: 0, dayIndex: 4 },
        { label: 'Sab', minutes: 0, dayIndex: 5 },
        { label: 'Dom', minutes: 0, dayIndex: 6 }
      ],
      day: [
        { label: '9am', minutes: 0 },
        { label: '11am', minutes: 0 },
        { label: '1pm', minutes: 0 },
        { label: '3pm', minutes: 0 },
        { label: '5pm', minutes: 0 },
        { label: '7pm', minutes: 0 },
        { label: '9pm', minutes: 0 }
      ],
      month: [
        { label: 'Sem 1', minutes: 0 },
        { label: 'Sem 2', minutes: 0 },
        { label: 'Sem 3', minutes: 0 },
        { label: 'Sem 4', minutes: 0 }
      ]
    };

    // Tiempo de inicio de la sesión
    const sessionStartTime = new Date();

    // Función para renderizar el gráfico
    function renderChart(period) {
      const chartContainer = document.getElementById('activityChart');
      const data = activityData[period];

      // Encontrar el valor máximo para normalizar las alturas
      const maxMinutes = Math.max(...data.map(d => d.minutes), 1); // Mínimo 1 para evitar división por 0
      const maxHeight = 220; // Altura máxima en píxeles

      // Limpiar el contenedor
      chartContainer.innerHTML = '';

      // Crear las barras
      data.forEach((item, index) => {
        const barHeight = item.minutes > 0 ? Math.max((item.minutes / maxMinutes) * maxHeight, 10) : 10;
        const isActive = period === 'week' && item.dayIndex === todayIndex;

        const wrapper = document.createElement('div');
        wrapper.className = 'chart-bar-wrapper';

        const bar = document.createElement('div');
        bar.className = 'chart-bar';
        bar.style.height = `${barHeight}px`;
        bar.style.opacity = isActive ? '1' : '0.2';
        bar.title = `${item.minutes} minutos`;

        const label = document.createElement('span');
        label.className = 'chart-label';
        label.textContent = item.label;

        wrapper.appendChild(bar);
        wrapper.appendChild(label);
        chartContainer.appendChild(wrapper);
      });
    }

    // Manejar los tabs de actividad
    document.querySelectorAll('.activity-tab').forEach(tab => {
      tab.addEventListener('click', function () {
        // Remover clase active de todos los tabs
        document.querySelectorAll('.activity-tab').forEach(t => t.classList.remove('active'));

        // Agregar clase active al tab clickeado
        this.classList.add('active');

        // Renderizar el gráfico con el período seleccionado
        const period = this.getAttribute('data-period');
        renderChart(period);
      });
    });

    // Actualizar el tiempo de sesión cada segundo
    function updateSessionTime() {
      setInterval(() => {
        const currentTime = new Date();
        const elapsedSeconds = Math.floor((currentTime - sessionStartTime) / 1000);
        const elapsedMinutes = Math.floor(elapsedSeconds / 60);

        // Actualizar el día actual con el tiempo transcurrido
        activityData.week[todayIndex].minutes = elapsedMinutes;

        // Re-renderizar si estamos en la vista semanal
        const activeTab = document.querySelector('.activity-tab.active');
        if (activeTab && activeTab.getAttribute('data-period') === 'week') {
          renderChart('week');
        }
      }, 1000); // Actualizar cada segundo para ver cambios más rápido
    }

    // Carrusel automático con controles
// Carrusel avanzado con animaciones suaves
function initCarousel() {
  const track = document.querySelector('.carousel-track');
  const slides = document.querySelectorAll('.carousel-card');
  const dots = document.querySelectorAll('.carousel-dot');
  const prevBtn = document.querySelector('.prev-btn');
  const nextBtn = document.querySelector('.next-btn');
  
  if (!track || !slides.length) return;
  
  let currentSlide = 0;
  const totalSlides = slides.length;
  let autoPlayInterval;
  let isTransitioning = false;
  
  
  function updateCarousel(smooth = true) {
    if (isTransitioning) return;
    
    isTransitioning = true;
    
    // Aplicar transición suave
    if (smooth) {
      track.style.transition = 'transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
    } else {
      track.style.transition = 'none';
    }
    
    // Mover el track
    track.style.transform = `translateX(-${currentSlide * 100}%)`;
    
    // Actualizar dots con animación
    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === currentSlide);
    });
    
    // Agregar efecto de escala a la carta activa
    slides.forEach((slide, index) => {
      if (index === currentSlide) {
        slide.style.opacity = '1';
        slide.style.transform = 'scale(1)';
      } else {
        slide.style.opacity = '0.7';
        slide.style.transform = 'scale(0.95)';
      }
    });
    
    setTimeout(() => {
      isTransitioning = false;
    }, 600);
  }
  
  function nextSlide() {
    if (isTransitioning) return;
    currentSlide = (currentSlide + 1) % totalSlides;
    updateCarousel();
    resetAutoPlay();
  }
  
  function prevSlide() {
    if (isTransitioning) return;
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    updateCarousel();
    resetAutoPlay();
  }
  
  function goToSlide(slideIndex) {
    if (isTransitioning || slideIndex === currentSlide) return;
    currentSlide = slideIndex;
    updateCarousel();
    resetAutoPlay();
  }
  
  // Event listeners para botones
  if (nextBtn) {
    nextBtn.addEventListener('click', (e) => {
      e.preventDefault();
      nextSlide();
    });
  }
  
  if (prevBtn) {
    prevBtn.addEventListener('click', (e) => {
      e.preventDefault();
      prevSlide();
    });
  }
  
  // Event listeners para dots
  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => goToSlide(index));
  });
  
  // Auto play
  function startAutoPlay() {
    stopAutoPlay();
    autoPlayInterval = setInterval(() => {
      nextSlide();
    }, 5000); // Cambio cada 5 segundos
  }
  
  function stopAutoPlay() {
    if (autoPlayInterval) {
      clearInterval(autoPlayInterval);
      autoPlayInterval = null;
    }
  }
  
  function resetAutoPlay() {
    stopAutoPlay();
    startAutoPlay();
  }
  
  // Pausar auto play al interactuar
  const carouselContainer = document.querySelector('.carousel-container');
  if (carouselContainer) {
    carouselContainer.addEventListener('mouseenter', stopAutoPlay);
    carouselContainer.addEventListener('mouseleave', startAutoPlay);
    
    // Soporte para touch
    carouselContainer.addEventListener('touchstart', stopAutoPlay);
    carouselContainer.addEventListener('touchend', () => {
      setTimeout(startAutoPlay, 3000);
    });
  }
  
  // Swipe para móviles mejorado
  let startX = 0;
  let endX = 0;
  let startTime = 0;
  
  if (track) {
    track.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
      startTime = Date.now();
    }, { passive: true });
    
    track.addEventListener('touchmove', (e) => {
      if (isTransitioning) return;
      endX = e.touches[0].clientX;
    }, { passive: true });
    
    track.addEventListener('touchend', (e) => {
      if (isTransitioning) return;
      endX = e.changedTouches[0].clientX;
      handleSwipe();
    });
  }
  
  function handleSwipe() {
    const diff = startX - endX;
    const timeDiff = Date.now() - startTime;
    const velocity = Math.abs(diff) / timeDiff;
    const swipeThreshold = 50;
    
    // Solo registrar swipe si es lo suficientemente rápido o largo
    if (Math.abs(diff) > swipeThreshold || velocity > 0.3) {
      if (diff > 0) {
        nextSlide(); // Swipe izquierda
      } else {
        prevSlide(); // Swipe derecha
      }
    }
  }
  
  // Soporte para teclado
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
      prevSlide();
    } else if (e.key === 'ArrowRight') {
      nextSlide();
    }
  });
  
  // Inicializar
  updateCarousel(false);
  startAutoPlay();
  
  // Prevenir transiciones durante resize
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    stopAutoPlay();
    resizeTimer = setTimeout(() => {
      updateCarousel(false);
      startAutoPlay();
    }, 250);
  });
}

// Animación de entrada para el video
function initVideoAnimation() {
  const video = document.querySelector('.main-video');
  if (!video) return;
  
  // Reproducir automáticamente con un fade in suave
  video.style.opacity = '0';
  video.style.transition = 'opacity 1s ease';
  
  video.addEventListener('loadeddata', () => {
    setTimeout(() => {
      video.style.opacity = '1';
    }, 300);
  });
  
  // Control de reproducción al hacer hover
  const videoContainer = document.querySelector('.video-container');
  if (videoContainer) {
    videoContainer.addEventListener('mouseenter', () => {
      video.playbackRate = 1.0;
    });
    
    videoContainer.addEventListener('mouseleave', () => {
      video.playbackRate = 1.0;
    });
  }
}

// Animaciones de scroll suaves
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });
  
  // Observar elementos animables
  document.querySelectorAll('.course-card, .planning-card, .stat-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
}

// Mejorar la experiencia de búsqueda
function initSearchEnhancement() {
  const searchInput = document.querySelector('.search-input');
  if (!searchInput) return;
  
  let searchTimeout;
  
  searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      const query = e.target.value.toLowerCase();
      const courseCards = document.querySelectorAll('.course-card');
      
      courseCards.forEach(card => {
        const title = card.querySelector('.course-title')?.textContent.toLowerCase();
        const description = card.querySelector('.course-lessons')?.textContent.toLowerCase();
        
        if (title?.includes(query) || description?.includes(query) || !query) {
          card.style.display = 'block';
          card.style.opacity = '1';
          card.style.transform = 'scale(1)';
        } else {
          card.style.opacity = '0.3';
          card.style.transform = 'scale(0.95)';
        }
      });
    }, 300);
  });
}

// Efectos hover para tarjetas de planificación
function initPlanningCardEffects() {
  const planningCards = document.querySelectorAll('.planning-card');
  
  planningCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateX(5px)';
      this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateX(0)';
      this.style.boxShadow = 'none';
    });
  });
}

// Animación para las estadísticas
function initStatisticsAnimation() {
  const statCards = document.querySelectorAll('.stat-card');
  
  statCards.forEach((card, index) => {
    setTimeout(() => {
      card.style.opacity = '1';
      card.style.transform = 'scale(1)';
    }, index * 100);
  });
}

// Efecto de carga progresiva
function initProgressiveLoading() {
  const elements = document.querySelectorAll('[class*="section"]');
  
  elements.forEach((element, index) => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
      element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      element.style.opacity = '1';
      element.style.transform = 'translateY(0)';
    }, index * 150);
  });
}

// Tooltips para botones
function initTooltips() {
  const buttons = document.querySelectorAll('[aria-label]');
  
  buttons.forEach(button => {
    button.addEventListener('mouseenter', function() {
      const tooltip = document.createElement('div');
      tooltip.textContent = this.getAttribute('aria-label');
      tooltip.style.cssText = `
        position: absolute;
        background: #303030;
        color: white;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 12px;
        white-space: nowrap;
        pointer-events: none;
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.3s ease;
      `;
      
      document.body.appendChild(tooltip);
      
      const rect = this.getBoundingClientRect();
      tooltip.style.top = rect.bottom + 10 + 'px';
      tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
      
      setTimeout(() => {
        tooltip.style.opacity = '1';
      }, 10);
      
      this._tooltip = tooltip;
    });
    
    button.addEventListener('mouseleave', function() {
      if (this._tooltip) {
        this._tooltip.style.opacity = '0';
        setTimeout(() => {
          this._tooltip.remove();
          delete this._tooltip;
        }, 300);
      }
    });
  });
}

// Precargar imágenes del carrusel
function preloadCarouselImages() {
  const images = [
    'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=500&h=300&fit=crop',
    'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500&h=300&fit=crop',
    'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=500&h=300&fit=crop',
    'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=500&h=300&fit=crop',
    'https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=500&h=300&fit=crop'
  ];
  
  images.forEach(src => {
    const img = new Image();
    img.src = src;
  });
}

// Inicializar toda la página
document.addEventListener('DOMContentLoaded', function() {
  console.log('🚀 Inicializando AIRWRITE SOFT Dashboard...');
  
  // Precargar recursos
  preloadCarouselImages();
  
  // Inicializar componentes principales
  initCarousel();
  initVideoAnimation();
  initScrollAnimations();
  initSearchEnhancement();
  initPlanningCardEffects();
  initStatisticsAnimation();
  initTooltips();
  
  // Carga progresiva con delay
  setTimeout(() => {
    initProgressiveLoading();
  }, 100);
  
  // Mensaje de bienvenida en consola
  console.log('%c✨ Dashboard cargado exitosamente', 'color: #369eff; font-size: 14px; font-weight: bold;');
  console.log('%c🎨 Diseño moderno y responsive activado', 'color: #43e97b; font-size: 12px;');
  
  // Agregar clase de carga completa
  setTimeout(() => {
    document.body.classList.add('loaded');
  }, 500);
});

// Manejo de errores global
window.addEventListener('error', function(e) {
  console.error('Error detectado:', e.message);
});

// Optimización de rendimiento
let ticking = false;
window.addEventListener('scroll', function() {
  if (!ticking) {
    window.requestAnimationFrame(function() {
      // Aquí puedes agregar lógica adicional en scroll
      ticking = false;
    });
    ticking = true;
  }
});

// Prevenir comportamiento indeseado en producción
if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
  // Desactivar console en producción
  console.log = function() {};
  console.warn = function() {};
  console.error = function() {};
}

// Manejo de visibilidad de página
document.addEventListener('visibilitychange', function() {
  if (document.hidden) {
    // Pausar animaciones cuando la pestaña no está visible
    const video = document.querySelector('.main-video');
    if (video) video.pause();
  } else {
    // Reanudar cuando vuelve a estar visible
    const video = document.querySelector('.main-video');
    if (video) video.play();
  }
});
    // Inicializar el gráfico al cargar la página
    document.addEventListener('DOMContentLoaded', function () {
      renderChart('week');
      updateSessionTime();
    });
