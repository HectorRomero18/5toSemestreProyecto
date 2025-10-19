document.addEventListener("DOMContentLoaded", () => {
  const greeting = document.querySelector(".p");
  const username = greeting.dataset.username;

  // 🔹 Frases en un array
  const frases = [
    `Hola, ${username}! 👋`, // ← primera frase personalizada
    (() => {
      const hour = new Date().getHours();
      if (hour >= 5 && hour < 12) return "Buenos días ☀️";
      else if (hour >= 12 && hour < 18) return "Buenas tardes 🌤️";
      else return "Buenas noches 🌙";
    })(),
    "Vamos a trazar",
    "Notas que flotan",
    "Inspírate y crea",
    "Flota con tus ideas",
    "Imagina y hazlo",
  ];

  let index = 0;

  const mostrarFrase = () => {
    greeting.classList.remove("fade-in", "fade-out");
    greeting.textContent = frases[index];
    greeting.classList.add("fade-in");

    setTimeout(() => {
      greeting.classList.remove("fade-in");
      greeting.classList.add("fade-out");

      setTimeout(() => {
        index++;
        if (index < frases.length) {
          mostrarFrase();
        }
      }, 730); // duración fade-out
    }, 3000); // duración frase visible
  };

  mostrarFrase();
});