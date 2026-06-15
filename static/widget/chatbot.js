(function () {

  /* Prevent duplicate loading */
  if (document.getElementById("farm-chatbot-widget")) {
    return;
  }

  /* ===============================
     Load CSS
     =============================== */
  const css = document.createElement("link");
  css.rel = "stylesheet";
  css.href = "https://ai.farmfluence.in/static/widget/chatbot.css";
  document.head.appendChild(css);

  /* ===============================
     Create Widget
     =============================== */
  const widget = document.createElement("div");
  widget.id = "farm-chatbot-widget";

  widget.innerHTML = `
    <div id="chat-toggle">🌱</div>

    <div id="chat-box">
      <div id="chat-header">
        <span>FarmFluence AI</span>
        <span id="chat-close">✖</span>
      </div>

      <div id="chat-body"></div>

      <div id="chat-footer">
        <input id="chat-input" placeholder="Ask your farming question..." />
        <button id="chat-mic">🎙️</button>
        <button id="chat-send">➤</button>
      </div>
    </div>
  `;

  document.body.appendChild(widget);

  /* ===============================
     Welcome Bubble
     =============================== */
  const welcomeBubble = document.createElement("div");
  welcomeBubble.id = "chat-welcome-bubble";
  welcomeBubble.innerText =
    "👋 Hello! I am your AI Assistant. How can I help you today?";

  widget.appendChild(welcomeBubble);
  welcomeBubble.style.display = "block";

  /* ===============================
     Elements
     =============================== */
  const toggleBtn = document.getElementById("chat-toggle");
  const chatBox = document.getElementById("chat-box");
  const closeBtn = document.getElementById("chat-close");
  const chatBody = document.getElementById("chat-body");
  const chatInput = document.getElementById("chat-input");
  const sendBtn = document.getElementById("chat-send");
  const micBtn = document.getElementById("chat-mic");

  let isOpen = false;

  /* ===============================
     Open / Close Logic
     =============================== */
  function openChat() {
    chatBox.style.display = "flex";
    toggleBtn.style.display = "none";
    welcomeBubble.style.display = "none";
    isOpen = true;

    setTimeout(() => {
      chatInput.focus();
    }, 150);
  }

  function closeChat() {
    chatBox.style.display = "none";
    toggleBtn.style.display = "flex";
    isOpen = false;
  }

  toggleBtn.onclick = () => {
    if (isOpen) {
      closeChat();
    } else {
      openChat();
    }
  };

  closeBtn.onclick = closeChat;

  /* ===============================
     Click Outside to Close
     =============================== */
  document.addEventListener("click", (e) => {
    if (
      isOpen &&
      !chatBox.contains(e.target) &&
      !toggleBtn.contains(e.target)
    ) {
      closeChat();
    }
  });

  /* ===============================
     Hover Bubble
     =============================== */
  toggleBtn.addEventListener("mouseenter", () => {
    if (!isOpen) {
      welcomeBubble.style.display = "block";
    }
  });

  toggleBtn.addEventListener("mouseleave", () => {
    if (!isOpen) {
      welcomeBubble.style.display = "none";
    }
  });

  /* ===============================
     Messages
     =============================== */
  function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `msg ${sender}`;
    div.innerText = text;

    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function showTyping() {
    const typing = document.createElement("div");
    typing.id = "typing";
    typing.className = "msg bot typing";
    typing.innerText = "FarmFluence AI is typing...";

    chatBody.appendChild(typing);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function hideTyping() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
  }

  /* ===============================
     Send Message
     =============================== */
  async function sendMessage() {
    const text = chatInput.value.trim();

    if (!text) return;

    addMessage(text, "user");
    chatInput.value = "";

    showTyping();

    try {
      const response = await fetch(
        "https://ai.farmfluence.in/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          mode: "cors",
          body: JSON.stringify({
            message: text
          })
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      hideTyping();

      addMessage(
        data.reply || "⚠️ No response received.",
        "bot"
      );

    } catch (error) {
      console.error("FarmFluence Error:", error);

      hideTyping();

      addMessage(
        "⚠️ FarmFluence AI is currently unavailable. Please try again in a few moments.",
        "bot"
      );
    }
  }

  sendBtn.onclick = sendMessage;

  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  /* ===============================
     Voice Input
     =============================== */
  micBtn.onclick = () => {

    if (!("webkitSpeechRecognition" in window)) {
      alert("Voice input works only in Chrome.");
      return;
    }

    const rec = new webkitSpeechRecognition();

    rec.lang = "en-IN";
    rec.continuous = false;
    rec.interimResults = false;

    rec.onresult = (e) => {
      chatInput.value = e.results[0][0].transcript;
      sendMessage();
    };

    rec.start();
  };

  /* ===============================
     Init
     =============================== */
  closeChat();

  addMessage(
    "👋 Welcome to FarmFluence AI. Please enter your name and location, then ask any agriculture-related question.",
    "bot"
  );

})();
