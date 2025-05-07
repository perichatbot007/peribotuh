// Element selectors
const mainSection = document.querySelector('.main-section');
const aboutSection = document.querySelector('.about-section');
const footer = document.querySelector('footer');
const formSection = document.getElementById("form-section");
const chatSection = document.getElementById("chat-section");
const sidebar = document.getElementById("chatSidebar");
const menuBtn = document.getElementById("menuBtn");
const menuBtnChat = document.getElementById("menuBtnChat");
const navLinks = document.getElementById("navLinks");
const backBtn = document.getElementById("backBtn");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const chatHistory = document.getElementById("chatHistory");

function showMainPage(push = true) {
  aboutSection.classList.remove('active');
  mainSection.classList.add('active');
  document.querySelector('.features').style.display = 'grid';
  footer.style.display = 'flex';
  document.getElementById("menuBtn").style.display = "block";
  document.getElementById("navLinks").style.display = "flex";
  document.querySelector("header").style.display = "flex";
  formSection.style.display = "none";
  chatSection.classList.remove("active");
  chatSection.style.display = "none";
  if (push) history.pushState({ page: 'main' }, '', '');
}

function showAboutPage(push = true) {
  mainSection.classList.remove('active');
  aboutSection.classList.add('active');
  document.querySelector('.features').style.display = 'none';
  footer.style.display = 'none';
  document.getElementById("menuBtn").style.display = "none";
  if (push) history.pushState({ page: 'about' }, '', '');
}

function showLoginForm(push = true) {
  formSection.style.display = "flex";
  mainSection.classList.remove('active');
  aboutSection.classList.remove('active');
  footer.style.display = 'none';
  document.getElementById("login-view").classList.add("active");
  document.getElementById("signup-view").classList.remove("active");
  if (push) history.pushState({ page: 'login' }, '', '');
}

function showSignupForm(push = true) {
  formSection.style.display = "flex";
  mainSection.classList.remove('active');
  aboutSection.classList.remove('active');
  footer.style.display = 'none';
  document.getElementById("signup-view").classList.add("active");
  document.getElementById("login-view").classList.remove("active");
  if (push) history.pushState({ page: 'signup' }, '', '');
}

function showChatbot(push = true) {
  chatSection.style.display = "flex";
  chatSection.classList.add("active");
  mainSection.classList.remove('active');
  aboutSection.classList.remove('active');
  footer.style.display = 'none';
  document.querySelector('.features').style.display = 'none';
  document.getElementById('navLinks').style.display = 'none';
  document.getElementById("menuBtn").style.display = "none";
  document.querySelector('header').style.display = 'none';
  const chatBox = document.getElementById('chatBox');
  chatBox.innerHTML = '';
  if (push) history.pushState({ page: 'chat' }, '', '');
}

function togglePassword(fieldId, btn) {
  const input = document.getElementById(fieldId);
  const icon = btn.querySelector("i");
  input.type = input.type === "password" ? "text" : "password";
  icon.classList.toggle("fa-eye");
  icon.classList.toggle("fa-eye-slash");
}

async function handleLogin() {
  const user = document.getElementById("login-username").value.trim();
  const pass = document.getElementById("login-password").value.trim();
  const errorDiv = document.getElementById("login-error");
  errorDiv.textContent = "";

  if (!user || !pass) {
    errorDiv.textContent = "Please fill in all fields.";
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: user, password: pass })
    });
    const result = await response.json();
    alert(result.message);
    if (response.ok) {
      formSection.style.display = "none";
      showChatbot();
    } else {
      errorDiv.textContent = result.error || "Login failed.";
    }
  } catch (err) {
    errorDiv.textContent = "Server error.";
  }
}

async function handleSignup() {
  const name = document.getElementById("signup-name").value.trim();
  const email = document.getElementById("signup-email").value.trim();
  const pass = document.getElementById("signup-password").value.trim();
  const cpass = document.getElementById("signup-cpass").value.trim();
  const errorDiv = document.getElementById("signup-error");
  const passError = document.getElementById("password-match-error");
  errorDiv.textContent = "";
  passError.textContent = "";

  if (!name || !email || !pass || !cpass) {
    errorDiv.textContent = "Please fill in all fields.";
    return;
  }
  if (pass !== cpass) {
    passError.textContent = "Passwords do not match.";
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password: pass, confirm_password: cpass })
    });
    const result = await response.json();
    alert(result.message);
    if (response.ok) {
      formSection.style.display = "none";
      showChatbot();
    } else {
      errorDiv.textContent = result.error || "Signup failed.";
    }
  } catch (err) {
    errorDiv.textContent = "Server error.";
  }
}

chatInput.addEventListener('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});

chatInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
});

function sendMessage() {
  const message = chatInput.value.trim();
  if (!message) return;

  chatInput.disabled = true;
  sendBtn.disabled = true;

  saveMessageToHistory(message);
  chatInput.value = '';
  chatInput.style.height = 'auto';

  const chatBox = document.getElementById('chatBox');
  let currentConversation = chatBox.querySelector('.chat-conversation');
  if (!currentConversation) {
    currentConversation = document.createElement('div');
    currentConversation.className = 'chat-conversation';
    chatBox.appendChild(currentConversation);
  }

  const welcomeMessage = document.querySelector('.welcome-message');
  if (welcomeMessage) welcomeMessage.remove();

  const userMsg = document.createElement('div');
  userMsg.className = 'chat-message user-message';
  userMsg.textContent = message;
  currentConversation.appendChild(userMsg);

  fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  })
    .then(res => res.json())
    .then(data => {
      const botMsg = document.createElement('div');
      botMsg.className = 'chat-message bot-message';
      botMsg.textContent = data.response || "No response.";
      currentConversation.appendChild(botMsg);
    })
    .catch(err => {
      const botMsg = document.createElement('div');
      botMsg.className = 'chat-message bot-message';
      botMsg.textContent = "Oops! Something went wrong.";
      currentConversation.appendChild(botMsg);
    })
    .finally(() => {
      chatInput.disabled = false;
      sendBtn.disabled = false;
      chatInput.focus();
      setTimeout(() => {
        document.querySelector(".chat-content").scrollTo({
          top: document.querySelector(".chat-content").scrollHeight,
          behavior: "smooth"
        });
      }, 100);
    });
}

function saveMessageToHistory(message) {
  let history = JSON.parse(localStorage.getItem("chatHistory")) || [];
  history.push(message);
  localStorage.setItem("chatHistory", JSON.stringify(history));
}

function showChatHistory() {
  const history = JSON.parse(localStorage.getItem("chatHistory")) || [];
  chatHistory.innerHTML = history.length
    ? history.map((msg, index) => `
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px;">
          <span style="flex: 1; cursor: pointer;" onclick="goToConversation('${msg}')">• ${msg}</span>
          <button onclick="deleteHistoryItem(${index})" style="background: none; border: none; color: red; cursor: pointer;">🗑️</button>
        </div>`).join("")
    : "<p>No previous messages.</p>";
}

function goToConversation(promptText) {
  localStorage.setItem('selectedPrompt', promptText);
  showChatbot();
  setTimeout(() => scrollToSelectedPrompt(), 500);
}

function scrollToSelectedPrompt() {
  const selectedPrompt = localStorage.getItem('selectedPrompt');
  if (!selectedPrompt) return;

  const conversations = document.querySelectorAll('.chat-conversation');
  for (const convo of conversations) {
    const userMessages = convo.querySelectorAll('.chat-message.user-message');
    for (const msg of userMessages) {
      if (msg.textContent.trim() === selectedPrompt.trim()) {
        convo.scrollIntoView({ behavior: 'smooth', block: 'start' });
        convo.style.border = '2px solid #00ffff';
        convo.style.borderRadius = '10px';
        convo.style.padding = '10px';
        setTimeout(() => {
          convo.style.border = 'none';
          convo.style.padding = '0';
        }, 2000);
        localStorage.removeItem('selectedPrompt');
        return;
      }
    }
  }
}

function deleteHistoryItem(index) {
  let history = JSON.parse(localStorage.getItem("chatHistory")) || [];
  history.splice(index, 1);
  localStorage.setItem("chatHistory", JSON.stringify(history));
  showChatHistory();
}

// Sidebar and navigation handlers
menuBtn.addEventListener('click', () => {
  sidebar.classList.add('show');
  menuBtnChat.style.display = 'none';
  navLinks.classList.toggle('show');
});

menuBtnChat.addEventListener('click', () => {
  sidebar.classList.add('show');
  menuBtnChat.style.display = 'none';
  document.getElementById('chatBackArrow').style.display = 'none';
});

backBtn.addEventListener('click', () => {
  sidebar.classList.remove('show');
  menuBtnChat.style.display = 'block';
  document.getElementById('chatBackArrow').style.display = 'block';
});

document.getElementById("toggleHistoryContainer").addEventListener("click", () => {
  const isVisible = chatHistory.style.display === "block";
  chatHistory.style.display = isVisible ? "none" : "block";
  if (!isVisible) showChatHistory();
});

sendBtn.addEventListener('click', sendMessage);

document.getElementById('clearHistoryBtn').addEventListener('click', () => {
  localStorage.removeItem('chatHistory');
  chatHistory.innerHTML = "<p>No previous messages.</p>";
});

document.getElementById('formBackBtn').addEventListener('click', function (e) {
  e.preventDefault();
  formSection.style.display = "none";
  showMainPage();
});

document.getElementById('aboutBtn').addEventListener('click', e => {
  e.preventDefault();
  showAboutPage();
});

document.getElementById('headerLoginBtn').addEventListener('click', e => {
  e.preventDefault();
  showLoginForm();
});

document.getElementById('headerSigninBtn').addEventListener('click', e => {
  e.preventDefault();
  showSignupForm();
});

document.getElementById('tryChatbotBtn').addEventListener('click', e => {
  e.preventDefault();
  showChatbot();
});

document.getElementById('helpBtn').addEventListener('click', e => {
  e.preventDefault();
  showAboutPage();
  setTimeout(() => {
    document.getElementById('helpSection').scrollIntoView({ behavior: 'smooth' });
  }, 100);
});

document.getElementById('bd').addEventListener('click', e => {
  e.preventDefault();
  showChatbot();
});

window.onload = () => {
  showMainPage(false);
};
