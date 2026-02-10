(function () {
  /* ===============================
     Load CSS
     =============================== */
  const css = document.createElement("link");
  css.rel = "stylesheet";
  css.href = "/static/widget/chatbot.css";
  document.head.appendChild(css);

  /* ===============================
     Create Widget HTML
     =============================== */
  const widget = document.createElement("div");
  widget.id = "farm-chatbot-widget";
  widget.innerHTML = `
    <div id="chat-toggle" title="Chat with FarmFluence AI">🌱</div>

    <div id="chat-box" class="hidden">
      <div id="chat-header">
        <span>FarmFluence AI</span>
        <span id="chat-close">✖</span>
      </div>

      <div id="chat-body"></div>

      <div id="chat-footer">
        <input
          id="chat-input"
          type="text"
          placeholder="Ask your farming question..."
          autocomplete="off"
        />
        <button id="chat-mic" title="Voice input">🎙️</button>
        <button id="chat-send">➤</button>
      </div>
    </div>
  `;
  document.body.appendChild(widget);

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

  /* ===============================
     Toggle Logic
     =============================== */
  toggleBtn.onclick = () => {
    chatBox.classList.remove("hidden");
    toggleBtn.style.display = "none";
    setTimeout(() => chatInput.focus(), 200);
  };

  closeBtn.onclick = () => {
    chatBox.classList.add("hidden");
    toggleBtn.style.display = "flex";
  };

  /* ===============================
     Message Helpers
     =============================== */
  function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `msg ${sender}`;
    div.innerText = text;
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function showTyping() {
    const div = document.createElement("div");
    div.className = "msg bot typing";
    div.id = "typing-indicator";
    div.innerText = "FarmFluence AI is typing...";
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function hideTyping() {
    const t = document.getElementById("typing-indicator");
    if (t) t.remove();
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
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      const data = await res.json();
      hideTyping();
      addMessage(data.reply || "No response from server.", "bot");

    } catch (err) {
      hideTyping();
      addMessage("⚠️ Unable to reach server.", "bot");
    }
  }

  sendBtn.onclick = sendMessage;
  chatInput.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
  });

  /* ===============================
     🎙️ Voice Input (Chrome)
     =============================== */
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

  /* ===============================
     Welcome Message
     =============================== */
  addMessage(
    "👋 Hi! I’m FarmFluence AI.\nHow can I help you today?",
    "bot"
  );
})();
