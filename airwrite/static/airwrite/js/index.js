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
const buttonText = document.getElementById('buttonText');
const statusEl = document.getElementById('status');

recordButton.onclick = async function() {
  if (!mediaRecorder || mediaRecorder.state === "inactive") {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];

      mediaRecorder.ondataavailable = e => {
        audioChunks.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append("audio", audioBlob, "comando.webm");

        statusEl.className = "status processing";
        statusEl.innerText = "⏳ Procesando audio...";

        try {
          const response = await fetch(window.urls.transcribir_audio_api, {
            method: "POST",
            body: formData,
            headers: { 'X-CSRFToken': csrftoken }
          });
          const data = await response.json();
          if (data.comando) {
            statusEl.className = "status success";
            statusEl.textContent = "✅ Comando: " + data.comando;
          } else {
            statusEl.className = "status error";
            statusEl.textContent = "❌ " + (data.error || "Error desconocido");
          }
        } catch (err) {
          statusEl.className = "status error";
          statusEl.innerText = "❌ Error al procesar el audio";
        }
      };

      mediaRecorder.start();
      recordButton.classList.add('recording');
      buttonText.textContent = "⏹️ Detener Grabación";
      statusEl.className = "status recording";
      statusEl.innerText = "🔴 Grabando...";
    } catch (err) {
      statusEl.className = "status error";
      statusEl.innerText = "❌ Error al acceder al micrófono";
    }
  } else if (mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    recordButton.classList.remove('recording');
    buttonText.textContent = "🎤 Iniciar Grabación";
    statusEl.className = "status";
    statusEl.innerText = "";
    mediaRecorder.stream.getTracks().forEach(track => track.stop());
  }
};