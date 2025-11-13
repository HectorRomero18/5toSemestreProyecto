// JS extraido de index.html inline
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

let mediaRecorder;
let audioChunks = [];

const recordButton = document.getElementById('recordButton');
const clearButton = document.getElementById('clearButton');

if (!clearButton) {
  alert("Clear button not found");
} else {
  clearButton.onclick = async function() {
  try {
    const response = await fetch(window.urls.clear_canvas, {
      method: "POST",
      headers: { 'X-CSRFToken': csrftoken }
    });
    const data = await response.json();
    if (data.status === "ok") {
      // Force refresh the canvas feed
      const canvasImg = document.querySelector('.canvas-feed');
      if (canvasImg) {
        canvasImg.src = canvasImg.src.split('?')[0] + '?t=' + Date.now();
      }
    }
  } catch (err) {
    console.error("Error clearing canvas:", err);
  }
};

// recordButton.onclick = async function() {
//   if (!mediaRecorder || mediaRecorder.state === "inactive") {
//     try {
//       const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//       mediaRecorder = new MediaRecorder(stream);
//       audioChunks = [];

//       mediaRecorder.ondataavailable = e => {
//         audioChunks.push(e.data);
//       };

//       mediaRecorder.onstop = async () => {
//         const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
//         const formData = new FormData();
//         formData.append("audio", audioBlob, "comando.webm");

//         // Mostrar alerta de procesamiento
//         showTranscriptionAlert();

//         try {
//           const response = await fetch(window.urls.transcribir_audio_api, {
//             method: "POST",
//             body: formData,
//             headers: { 'X-CSRFToken': csrftoken }
//           });
//           const data = await response.json();
//           if (data.comando) {
//             showTranscriptionSuccess(data.comando);
//           } else {
//             showTranscriptionError(data.error || "Error desconocido");
//           }
//         } catch (err) {
//           showTranscriptionError("Error al procesar el audio");
//         }
//       };

//       mediaRecorder.start();
//       recordButton.classList.add('recording');
//     } catch (err) {
//       console.error("Error al acceder al micrófono:", err);
//       // Could show an alert here if needed
//     }
//   } else if (mediaRecorder.state === "recording") {
//     mediaRecorder.stop();
//     recordButton.classList.remove('recording');
//     mediaRecorder.stream.getTracks().forEach(track => track.stop());
//   }
// };

// function showTranscriptionAlert() {
//     const alert = document.getElementById('transcriptionAlert');
//     const timerIcon = alert.querySelector('.timer-icon');
//     const checkIcon = alert.querySelector('.check-icon');
//     const errorIcon = alert.querySelector('.error-icon');
//     const message = document.getElementById('alertMessage');
//     const result = document.getElementById('alertResult');
    
//     // Resetear estado
//     timerIcon.classList.remove('hidden');
//     checkIcon.classList.add('hidden');
//     errorIcon.classList.add('hidden');
//     message.textContent = 'Transcribiendo...';
//     result.classList.remove('show');
//     result.textContent = '';
    
//     alert.classList.add('show');
// }

// function showTranscriptionSuccess(transcribedText) {
//     const alert = document.getElementById('transcriptionAlert');
//     const timerIcon = alert.querySelector('.timer-icon');
//     const checkIcon = alert.querySelector('.check-icon');
//     const message = document.getElementById('alertMessage');
//     const result = document.getElementById('alertResult');
    
//     timerIcon.classList.add('hidden');
//     checkIcon.classList.remove('hidden');
//     message.textContent = '¡Transcripción exitosa!';
//     result.textContent = transcribedText;
//     result.classList.add('show');
    
//     // Cerrar automáticamente después de 3 segundos
//     setTimeout(() => {
//         hideTranscriptionAlert();
//     }, 3000);
// }

// function showTranscriptionError(errorMessage) {
//     const alert = document.getElementById('transcriptionAlert');
//     const timerIcon = alert.querySelector('.timer-icon');
//     const errorIcon = alert.querySelector('.error-icon');
//     const message = document.getElementById('alertMessage');
//     const result = document.getElementById('alertResult');
    
//     timerIcon.classList.add('hidden');
//     errorIcon.classList.remove('hidden');
//     message.textContent = 'Error en la transcripción';
//     result.textContent = errorMessage;
//     result.classList.add('show');
    
//     // Cerrar automáticamente después de 4 segundos
//     setTimeout(() => {
//         hideTranscriptionAlert();
//     }, 4000);
// }

// function hideTranscriptionAlert() {
//     const alert = document.getElementById('transcriptionAlert');
//     alert.classList.remove('show');
// }

}

// Función para cambiar el color del lápiz
document.addEventListener("DOMContentLoaded", () => {
    const colorButton = document.getElementById('colorButton');
    const colorMenu = document.getElementById('colorMenu');

    if (!colorButton || !colorMenu) {
        console.error("❌ Elementos del dropdown no encontrados");
        return;
    }

    colorButton.addEventListener('click', (e) => {
        e.stopPropagation();
        colorMenu.classList.toggle('show');
    });

    document.addEventListener('click', () => {
        colorMenu.classList.remove('show');
    });
});

// Función para cambiar el grosor del lápiz
document.addEventListener("DOMContentLoaded", () => {
    const grosorButton = document.getElementById('grosorButton');
    const grosorMenu = document.getElementById('grosorMenu');

    if (!grosorButton || !grosorMenu) {
        console.error("❌ Elementos del dropdown de grosor no encontrados");
        return;
    }

    grosorButton.addEventListener('click', (e) => {
        e.stopPropagation(); // evita que el clic cierre el menú
        grosorMenu.classList.toggle('show');
    });

    document.addEventListener('click', () => {
        grosorMenu.classList.remove('show');
    });

    // Detectar clic en opciones
    grosorMenu.querySelectorAll('.grosor-option').forEach(btn => {
        btn.addEventListener('click', () => {
            const selectedGrosor = btn.dataset.grosor;
            console.log("Grosor seleccionado:", selectedGrosor);
            grosorMenu.classList.remove('show');
            // Aquí puedes llamar a tu función que cambia el grosor en el canvas
        });
    });
});

// Función para manejar la tecla A para alternar el trazo (iniciar/detener)
document.addEventListener('keydown', (event) => {
    if (event.key === 'a' || event.key === 'A') {
        // Prevenir comportamiento por defecto si es necesario
        event.preventDefault();

        // Enviar solicitud para alternar el dibujo
        fetch(window.urls.toggle_drawing, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                console.log('Dibujo alternado');
            } else {
                console.error('Error al alternar dibujo:', data);
            }
        })
        .catch(err => console.error('Error en fetch:', err));
    }
});


// JavaScript para el select de navegación
document.addEventListener('DOMContentLoaded', function() {
    const selectContainer = document.querySelector('.nav-select-container');
    const selectTrigger = document.querySelector('.nav-select-trigger');
    
    if (selectTrigger) {
        selectTrigger.addEventListener('click', function(e) {
            e.preventDefault();
            selectContainer.classList.toggle('open');
        });
        
        // Cerrar al hacer click fuera
        document.addEventListener('click', function(e) {
            if (!selectContainer.contains(e.target)) {
                selectContainer.classList.remove('open');
            }
        });
        
        // Cerrar después de seleccionar una opción
        document.querySelectorAll('.nav-option').forEach(option => {
            option.addEventListener('click', function() {
                selectContainer.classList.remove('open');
            });
        });
    }
});
// Limpiar canvas cuando se cierra la página
window.addEventListener('beforeunload', function(event) {
    // Usar sendBeacon para una petición confiable durante el cierre de la página
    if (navigator.sendBeacon) {
        const data = new FormData();
        data.append('csrfmiddlewaretoken', csrftoken);
        navigator.sendBeacon(window.urls.clear_canvas, data);
    } else {
        // Fallback para navegadores que no soportan sendBeacon
        const xhr = new XMLHttpRequest();
        xhr.open('POST', window.urls.clear_canvas, false); // false hace la petición síncrona
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.send();
    }
});

// Función para verificar el trazo
document.addEventListener("DOMContentLoaded", () => {
    const verificarButton = document.getElementById('verificarButton');
    if (verificarButton) {
        verificarButton.onclick = async function() {
            try {
                const response = await fetch(window.urls.validar_trazo, {
                    method: "POST",
                    headers: { 'X-CSRFToken': csrftoken }
                });
                const data = await response.json();
                if (data.status === "ok") {
                    alert(`Precisión: ${data.score}%`);
                } else {
                    alert("Error: " + data.error);
                }
            } catch (err) {
                console.error("Error al verificar trazo:", err);
                alert("Error al verificar trazo");
            }
        };
    }
});
