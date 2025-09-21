// Datos de progreso por módulo (puedes ajustar estos valores)
const moduleProgress = {
  1: 45,
  2: 65,
  3: 30
};

let clickTimeout;
let selectedModuleId = null;

// Funcionalidad de click simple y doble click
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.module-card').forEach(card => {
    card.addEventListener('click', function (e) {
      e.preventDefault();

      const moduleId = parseInt(this.dataset.moduleId);
      const moduleUrl = this.dataset.url;

      if (!moduleId) return;

      if (clickTimeout) {
        // Doble click
        clearTimeout(clickTimeout);
        clickTimeout = null;
        window.location.href = moduleUrl;
      } else {
        // Click simple
        clickTimeout = setTimeout(() => {
          clickTimeout = null;
          document.querySelectorAll('.module-card').forEach(c => c.classList.remove('selected'));
          this.classList.add('selected');
          selectedModuleId = moduleId;
          showModuleInfo(moduleId);
        }, 250);
      }
    });
  });

  // Funcionalidad de búsqueda
  const searchBar = document.querySelector('.search-bar');
  if (searchBar) {
    searchBar.addEventListener('input', function (e) {
      const searchTerm = e.target.value.toLowerCase();
      const moduleCards = document.querySelectorAll('.module-card');

      moduleCards.forEach(card => {
        const titleElement = card.querySelector('.module-title');
        const descriptionElement = card.querySelector('p');
        if (titleElement && descriptionElement) {
          const title = titleElement.textContent.toLowerCase();
          const description = descriptionElement.textContent.toLowerCase();
          card.style.display = (title.includes(searchTerm) || description.includes(searchTerm) || searchTerm === '') ? '' : 'none';
        }
      });
    });
  }

  // Navegación del sidebar
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
      document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
      item.classList.add('active');
    });
  });

  // Animación de progreso inicial
  setTimeout(() => {
    document.querySelectorAll('.progress-fill').forEach(fill => {
      fill.style.width = '0%';
    });
  }, 100);
});

function showModuleInfo(moduleId) {
  document.querySelectorAll('.current-module').forEach(module => {
    module.style.display = 'none';
    module.classList.remove('show');
  });

  const currentModule = document.getElementById(`current-module-${moduleId}`);
  if (currentModule) {
    currentModule.style.display = 'block';
    const progressFill = currentModule.querySelector('.progress-fill');
    if (progressFill) {
      setTimeout(() => {
        progressFill.style.width = `${moduleProgress[moduleId] || 50}%`;
      }, 100);
    }
    setTimeout(() => {
      currentModule.classList.add('show');
    }, 50);
  }
}