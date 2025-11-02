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

    // Inicializar el gráfico al cargar la página
    document.addEventListener('DOMContentLoaded', function () {
      renderChart('week');
      updateSessionTime();
    });
