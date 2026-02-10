(function () {
  // Load CSS
  const css = document.createElement("link");
  css.rel = "stylesheet";
  css.href = "/static/widget/chatbot.css";
  document.head.appendChild(css);

  // Create widget
  const widget = document.createElement("div");
  widget.id = "farm-chatbot-widget";
  widget.innerHTML = `
    <div id="chat-toggle">🌱</div>

    <div id="chat-box" class="hidden">
      <div id="chat-header">
        FarmFluence AI
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

  // Elements
  const toggleBtn = document.getElementById("chat-toggle");
  const chatBox = document.getElementById("chat-box");
  const closeBtn = document.getElementById("chat-close");
  const chatBody = document.getElementById("chat-body");
  const chatInput = document.getElementById("chat-input");
  const sendBtn = document.getElementById("chat-send");
  const micBtn = document.getElementById("chat-mic");

  // Toggle open
  toggleBtn.onclick = () => {
    chatBox.classList.remove("hidden");
    toggleBtn.style.display = "none";
    setTimeout(() => chatInput.focus(), 200);
  };

  // Close chat
  closeBtn.onclick = () => {
    chatBox.classList.add("hidden");
    toggleBtn.style.display = "flex";
  };

  // Add message
  function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `msg ${sender}`;
    div.innerText = text;
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  // Send message
  async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    addMessage(text, "user");
    chatInput.value = "";

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();
      addMessage(data.reply, "bot");
    } catch {
      addMessage("⚠️ Server not reachable", "bot");
    }
  }

  sendBtn.onclick = sendMessage;
  chatInput.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
  });

  // 🎙️ Voice input
  micBtn.onclick = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Voice input works only in Chrome");
      return;
    }
    const rec = new webkitSpeechRecognition();
    rec.lang = "en-IN";
    rec.onresult = e => {
      chatInput.value = e.results[0][0].transcript;
      sendMessage();
    };
    rec.start();
  };

  // Welcome
  addMessage("👋 Hello! I’m FarmFluence AI. How can I help you today? Please enter your name and location", "bot");
})();
