let currentForm = 'login';
let currentLanguage = 'es';

const translations = {
  es: {
    welcomeText: 'Bienvenido a AirWrite<br />donde aprender es divertido',
    noAccount: '¿No tienes una cuenta? Puedes&nbsp;&nbsp;',
    registerLink: 'Registrarte aquí.',
    signIn: 'Ingresar',
    register: 'Registrarse',
    btnSignIn: 'Ingresar',
    btnRegister: 'Registrarse',
    continueWith: 'O continue con',
    menuInicio: 'Inicio',
    menuAcerca: 'Acerca de',
    menuContacto: 'Contacto',
    placeholderEmail: 'Ingrese Email',
    placeholderName: 'Ingrese Nombre',
    placeholderPassword: '••••••••'
  },
  en: {
    welcomeText: 'Welcome to AirWrite<br />where learning is fun',
    noAccount: "Don't have an account? You can&nbsp;&nbsp;",
    registerLink: 'Register here.',
    signIn: 'Sign In',
    register: 'Register',
    btnSignIn: 'Sign In',
    btnRegister: 'Register',
    continueWith: 'Or continue with',
    menuInicio: 'Home',
    menuAcerca: 'About',
    menuContacto: 'Contact',
    placeholderEmail: 'Enter Email',
    placeholderName: 'Enter Name',
    placeholderPassword: '••••••••'
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

function togglePasswordVisibility(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(iconId);
  
  if (input.type === 'password') {
    input.type = 'text';
    icon.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>';
  } else {
    input.type = 'password';
    icon.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>';
  }
}

function switchToLogin() {
  if (currentForm === 'login') return;
  
  const registerForm = document.getElementById('registerForm');
  const loginForm = document.getElementById('loginForm');
  const btnText = document.getElementById('btnText');
  const loginLine = document.getElementById('loginLine');
  const registerLine = document.getElementById('registerLine');
  
  loginLine.classList.remove('inactive');
  loginLine.classList.add('active');
  registerLine.classList.remove('active');
  registerLine.classList.add('inactive');
  
  registerForm.classList.add('slide-out-right');
  
  setTimeout(() => {
    registerForm.classList.add('hidden');
    registerForm.classList.remove('slide-out-right');
    
    loginForm.classList.remove('hidden');
    loginForm.classList.add('slide-in-left');
    
    setTimeout(() => {
      loginForm.classList.remove('slide-in-left');
    }, 300);
    
    btnText.textContent = translations[currentLanguage].btnSignIn;
    currentForm = 'login';
  }, 300);
}

function switchToRegister() {
  if (currentForm === 'register') return;
  
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const btnText = document.getElementById('btnText');
  const loginLine = document.getElementById('loginLine');
  const registerLine = document.getElementById('registerLine');
  
  loginLine.classList.remove('active');
  loginLine.classList.add('inactive');
  registerLine.classList.remove('inactive');
  registerLine.classList.add('active');
  
  loginForm.classList.add('slide-out-left');
  
  setTimeout(() => {
    loginForm.classList.add('hidden');
    loginForm.classList.remove('slide-out-left');
    
    registerForm.classList.remove('hidden');
    registerForm.classList.add('slide-in-right');
    
    setTimeout(() => {
      registerForm.classList.remove('slide-in-right');
    }, 300);
    
    btnText.textContent = translations[currentLanguage].btnRegister;
    currentForm = 'register';
  }, 300);
}

// Permitir enviar con Enter
document.addEventListener('keypress', function(e) {
  if (e.key === 'Enter') {
    const activeForm = currentForm === 'login' ? 
      document.getElementById('loginForm') : 
      document.getElementById('registerForm');
    
    if (activeForm && !activeForm.classList.contains('hidden')) {
      activeForm.submit();
    }
  }
});