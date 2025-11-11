/* // JS extraído de index.html inline
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
        event.preventDefault();
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
        
        document.addEventListener('click', function(e) {
            if (!selectContainer.contains(e.target)) {
                selectContainer.classList.remove('open');
            }
        });
        
        document.querySelectorAll('.nav-option').forEach(option => {
            option.addEventListener('click', function() {
                selectContainer.classList.remove('open');
            });
        });
    }
});

// Limpiar canvas cuando se cierra la página
window.addEventListener('beforeunload', function(event) {
    if (navigator.sendBeacon) {
        const data = new FormData();
        data.append('csrfmiddlewaretoken', csrftoken);
        navigator.sendBeacon(window.urls.clear_canvas, data);
    } else {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', window.urls.clear_canvas, false);
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.send();
    }
});

// =======================
// ENVÍO DE TRAZO PARA VALIDACIÓN
// =======================
async function enviarTrazo(coordenadas, letra) {
    if (!coordenadas || coordenadas.length === 0) {
        console.warn("No hay coordenadas para enviar");
        return;
    }

    const coordsPython = coordenadas.map(pt => [pt.x, pt.y]);

    try {
        const response = await fetch(window.urls.validar_trazo, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                caracter: letra,
                coordenadas: coordsPython
            })
        });

        const data = await response.json();
        if (data.error) {
            console.error("Error al validar trazo:", data.error);
        } else {
            console.log("Resultado de validación:", data.resultado);
            const resultado = data.resultado;
            if (resultado.es_correcto) {
                alert(`✅ Muy bien ${resultado.usuario}! La letra ${resultado.letra} fue correcta con ${(resultado.similitud * 100).toFixed(1)}% de similitud.`);
            } else {
                alert(`❌ ${resultado.usuario}, la letra ${resultado.letra} no coincide. Similitud: ${(resultado.similitud * 100).toFixed(1)}%`);
            }
        }
    } catch (err) {
        console.error("Error en fetch de validar trazo:", err);
    }
}

// =======================
// CAPTURA AUTOMÁTICA DE TRAZOS DESDE CÁMARA
// =======================
async function capturarTrazoAutomatico() {
    const letraSeleccionada = window.currentCaracter || "A"; 
    if (!letraSeleccionada) return;

    try {
        const response = await fetch(window.urls.capturar_trazo, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({ letra: letraSeleccionada })
        });

        const data = await response.json();
        if (!data.trazo || data.trazo.length === 0) {
            console.warn("No se capturó ningún trazo desde la cámara");
            return;
        }

        enviarTrazo(data.trazo, letraSeleccionada);

    } catch (err) {
        console.error("Error al capturar trazo automáticamente:", err);
    }
}

// =======================
// INTEGRACIÓN CON SELECCIÓN DE LETRA
// =======================
document.addEventListener('DOMContentLoaded', () => {
    const letrasElements = document.querySelectorAll('.nav-option'); // letras del módulo
    letrasElements.forEach(el => {
        el.addEventListener('click', () => {
            window.currentCaracter = el.dataset.letra; 
            console.log("Letra seleccionada:", window.currentCaracter);
            capturarTrazoAutomatico(); 
        });
    });
});
 */
// =======================
// UTILS
// =======================
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
let dibujando = false;
if (typeof window.currentCaracter === 'undefined') {
  window.currentCaracter = null;
}

// =======================
// BOTONES DE CANVAS
// =======================
const recordButton = document.getElementById('recordButton');
const clearButton = document.getElementById('clearButton');

if (clearButton) {
  clearButton.onclick = async function() {
    try {
      const response = await fetch(window.urls.clear_canvas, {
        method: "POST",
        headers: { 'X-CSRFToken': csrftoken }
      });
      const data = await response.json();
      if (data.status === "ok") {
        const canvasImg = document.querySelector('.canvas-feed');
        if (canvasImg) {
          canvasImg.src = canvasImg.src.split('?')[0] + '?t=' + Date.now();
        }
      }
    } catch (err) {
      console.error("Error clearing canvas:", err);
    }
  };
} else {
  alert("Clear button not found");
}

// =======================
// COLOR DEL LÁPIZ
// =======================
document.addEventListener("DOMContentLoaded", () => {
  const colorButton = document.getElementById('colorButton');
  const colorMenu = document.getElementById('colorMenu');

  if (colorButton && colorMenu) {
    colorButton.addEventListener('click', (e) => {
      e.stopPropagation();
      colorMenu.classList.toggle('show');
    });

    document.addEventListener('click', () => {
      colorMenu.classList.remove('show');
    });
  } else {
    console.error("❌ Elementos del dropdown de color no encontrados");
  }
});

// =======================
// GROSOR DEL LÁPIZ
// =======================
document.addEventListener("DOMContentLoaded", () => {
  const grosorButton = document.getElementById('grosorButton');
  const grosorMenu = document.getElementById('grosorMenu');

  if (grosorButton && grosorMenu) {
    grosorButton.addEventListener('click', (e) => {
      e.stopPropagation();
      grosorMenu.classList.toggle('show');
    });

    document.addEventListener('click', () => {
      grosorMenu.classList.remove('show');
    });

    grosorMenu.querySelectorAll('.grosor-option').forEach(btn => {
      btn.addEventListener('click', () => {
        const selectedGrosor = btn.dataset.grosor;
        console.log("Grosor seleccionado:", selectedGrosor);
        grosorMenu.classList.remove('show');
        // aquí puedes conectar con el canvas real
      });
    });
  } else {
    console.error("❌ Elementos del dropdown de grosor no encontrados");
  }
});

// =======================
// TECLA “A” — alternar captura automática
// =======================
document.addEventListener('keydown', (event) => {
  if (event.key === 'a' || event.key === 'A') {
    event.preventDefault();
    dibujando = !dibujando;
    console.log(dibujando ? "🟢 Iniciando captura automática" : "⏸️ Captura detenida");

    // avisar al backend (mantiene compatibilidad con el original)
    fetch(window.urls.toggle_drawing, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({})
    }).catch(err => console.error('Error alternando dibujo:', err));

    if (dibujando) capturarTrazoAutomatico();
  }
});

// =======================
// SELECT DE NAVEGACIÓN (letras / sílabas / números)
// =======================
document.addEventListener('DOMContentLoaded', function() {
  const selectContainer = document.querySelector('.nav-select-container');
  const selectTrigger = document.querySelector('.nav-select-trigger');
  
  if (selectTrigger) {
    selectTrigger.addEventListener('click', function(e) {
      e.preventDefault();
      selectContainer.classList.toggle('open');
    });
    
    document.addEventListener('click', function(e) {
      if (!selectContainer.contains(e.target)) {
        selectContainer.classList.remove('open');
      }
    });
    
    document.querySelectorAll('.nav-option').forEach(option => {
      option.addEventListener('click', function() {
        const caracter = option.dataset.letra || option.dataset.silaba || option.dataset.numero;
        window.currentCaracter = caracter;
        console.log("Caracter seleccionado:", window.currentCaracter);
        selectContainer.classList.remove('open');
        capturarTrazoAutomatico(); // mismo comportamiento que antes
      });
    });
  }
});

// =======================
// LIMPIAR CANVAS AL SALIR
// =======================
window.addEventListener('beforeunload', function(event) {
  if (navigator.sendBeacon) {
    const data = new FormData();
    data.append('csrfmiddlewaretoken', csrftoken);
    navigator.sendBeacon(window.urls.clear_canvas, data);
  } else {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', window.urls.clear_canvas, false);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send();
  }
});

// =======================
// FUNCIÓN — CAPTURAR TRAZO AUTOMÁTICO
// =======================
async function capturarTrazoAutomatico() {
  const caracterSeleccionado = window.currentCaracter;
  if (!caracterSeleccionado) {
    console.warn("No hay caracter seleccionado");
    return;
  }

  try {
    const response = await fetch(window.urls.capturar_trazo, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      },
      body: JSON.stringify({ letra: caracterSeleccionado })
    });

    const data = await response.json();
    if (!data.trazo || data.trazo.length === 0) {
      console.warn("No se capturó ningún trazo desde la cámara");
      return;
    }

    await enviarTrazo(data.trazo, caracterSeleccionado);

    if (dibujando) capturarTrazoAutomatico(); // recursivo si se sigue dibujando
  } catch (err) {
    console.error("Error al capturar trazo automáticamente:", err);
  }
}

// =======================
// FUNCIÓN — ENVIAR TRAZO
// =======================
async function enviarTrazo(coordenadas, caracter) {
  if (!coordenadas || coordenadas.length === 0) {
    console.warn("No hay coordenadas para enviar");
    return;
  }

  const coordsPython = coordenadas.map(pt => [pt.x, pt.y]);

  try {
    const response = await fetch(window.urls.validar_trazo, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      },
      body: JSON.stringify({
        caracter,
        coordenadas: coordsPython
      })
    });

    const data = await response.json();
    if (data.error) {
      console.error("Error al validar trazo:", data.error);
      return;
    }

    const resultado = data.resultado;
    if (resultado.es_correcto) {
      alert(`✅ Muy bien ${resultado.usuario}! ${resultado.letra} fue correcta con ${(resultado.similitud * 100).toFixed(1)}% de similitud.`);
    } else {
      alert(`❌ ${resultado.usuario}, ${resultado.letra} no coincide. Similitud: ${(resultado.similitud * 100).toFixed(1)}%`);
    }
  } catch (err) {
    console.error("Error en fetch de validar trazo:", err);
  }
}
// =======================
// TECLA “E” — Enviar trazo actual al backend
// =======================
document.addEventListener('keydown', async (event) => {
  if (event.key === 'e' || event.key === 'E') {
    event.preventDefault();

    console.log("📤 Enviando trazo manualmente con tecla 'E'...");

    // Obtener la letra seleccionada y capturar el trazo actual
    const caracterSeleccionado = window.currentCaracter;
    if (!caracterSeleccionado) {
      alert("⚠️ No hay letra seleccionada.");
      return;
    }

    try {
      // Pedimos el trazo actual (igual que hace capturarTrazoAutomatico)
      const response = await fetch(window.urls.capturar_trazo, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({ letra: caracterSeleccionado })
      });

      const data = await response.json();
      if (!data.trazo || data.trazo.length === 0) {
        alert("⚠️ No se encontró ningún trazo para enviar.");
        return;
      }

      // Enviar trazo a la vista ValidarTrazoView
      await enviarTrazo(data.trazo, caracterSeleccionado);
      console.log("✅ Trazo enviado con éxito mediante la tecla 'E'.");

    } catch (err) {
      console.error("❌ Error al enviar trazo con tecla E:", err);
    }
  }
});

// =======================
// BOTÓN VERIFICAR — Verificar trazo actual
// =======================
document.addEventListener('DOMContentLoaded', () => {
  const verificarBtn = document.getElementById('verificarButton');
  if (verificarBtn) {
    verificarBtn.addEventListener('click', async () => {
      const caracterSeleccionado = window.currentCaracter;
      if (!caracterSeleccionado) {
        alert("⚠️ No hay letra seleccionada.");
        return;
      }

      try {
        const response = await fetch(window.urls.capturar_trazo, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
          },
          body: JSON.stringify({ letra: caracterSeleccionado })
        });

        const data = await response.json();
        if (!data.trazo || data.trazo.length === 0) {
          alert("⚠️ No se encontró ningún trazo para verificar.");
          return;
        }

        await enviarTrazo(data.trazo, caracterSeleccionado);
      } catch (err) {
        console.error("❌ Error al verificar trazo:", err);
        alert("❌ Error al verificar el trazo.");
      }
    });
  }
});
