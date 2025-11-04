let currentForm = 'login';
let currentLanguage = 'es';

const translations = {
  es: {
    welcomeText: 'Bienvenido a AirWrite<br />donde aprender es divertido',
    noAccount: 'Únete hoy mismo. AirWrite es&nbsp;&nbsp;',
    registerLink: 'gratis, rápido y seguro.',
    signIn: 'Ingresar',
    register: 'Registrarse',
    btnSignIn: 'Ingresar',
    btnRegister: 'Registrarse',
    continueWith: 'Continue con',
  },
  en: {
    welcomeText: 'Welcome to AirWrite<br />where learning is fun',
    noAccount: "Join today. AirWrite  is&nbsp;&nbsp;",
    registerLink: 'free, fast and secure.',
    signIn: 'Sign In',
    register: 'Register',
    btnSignIn: 'Sign In',
    btnRegister: 'Register',
    continueWith: 'Continue with',
  }
};

function changeLanguage(lang) {
  currentLanguage = lang;
  const t = translations[lang];
  
  document.getElementById('welcomeText').innerHTML = t.welcomeText;
  document.getElementById('noAccountText').innerHTML = t.noAccount;
  document.getElementById('registerLink').textContent = t.registerLink;
  document.getElementById('signInText').textContent = t.signIn;
  document.getElementById('registerText').textContent = t.register;
  document.getElementById('continueText').textContent = t.continueWith;
  document.getElementById('menuInicio').textContent = t.menuInicio;
  document.getElementById('menuAcerca').textContent = t.menuAcerca;
  document.getElementById('menuContacto').textContent = t.menuContacto;
  
  document.getElementById('loginEmail').placeholder = t.placeholderEmail;
  document.getElementById('loginPassword').placeholder = t.placeholderPassword;
  document.getElementById('registerName').placeholder = t.placeholderName;
  document.getElementById('registerEmail').placeholder = t.placeholderEmail;
  document.getElementById('registerPassword').placeholder = t.placeholderPassword;
  
  if (currentForm === 'login') {
    document.getElementById('btnText').textContent = t.btnSignIn;
  } else {
    document.getElementById('btnText').textContent = t.btnRegister;
  }
}
