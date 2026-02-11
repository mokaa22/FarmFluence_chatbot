(function () {

  /* ===============================
     Load CSS
     =============================== */
  const css = document.createElement("link");
  css.rel = "stylesheet";
  css.href = "https://ai.farmfluence.online/static/widget/chatbot.css";
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
     Create Welcome Tooltip (Persistent)
     =============================== */
  const welcomeBubble = document.createElement("div");
  welcomeBubble.id = "chat-welcome-bubble";
  welcomeBubble.innerText =
    "👋 Hello! I am your AI Assistant. How can I help you today?";
  widget.appendChild(welcomeBubble);


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
     STATE
     =============================== */
  let isOpen = false;


  function openChat() {
    chatBox.style.display = "flex";
    toggleBtn.style.display = "none";
    welcomeBubble.style.display = "none"; // hide bubble when opened
    isOpen = true;
    setTimeout(() => chatInput.focus(), 150);
  }

  function closeChat() {
    chatBox.style.display = "none";
    toggleBtn.style.display = "flex";
    welcomeBubble.style.display = "block"; // show bubble again
    isOpen = false;
  }


  /* ===============================
     Toggle Handlers
     =============================== */
  toggleBtn.onclick = () => {
    if (!isOpen) openChat();
  };

  closeBtn.onclick = () => {
    if (isOpen) closeChat();
  };


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


  /* ===============================
     Typing Indicator
     =============================== */
  function showTyping() {
    const t = document.createElement("div");
    t.id = "typing";
    t.className = "msg bot typing";
    t.innerText = "FarmFluence AI is typing...";
    chatBody.appendChild(t);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function hideTyping() {
    const t = document.getElementById("typing");
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
      const res = await fetch("https://ai.farmfluence.online/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      const data = await res.json();
      hideTyping();
      addMessage(data.reply, "bot");

    } catch {
      hideTyping();
      addMessage("⚠️ Server not reachable.", "bot");
    }
  }

  sendBtn.onclick = sendMessage;
  chatInput.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
  });


  /* ===============================
     Voice (Chrome)
     =============================== */
  micBtn.onclick = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Voice works only in Chrome");
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
     Initial State
     =============================== */
  closeChat();

  addMessage(
    "👋 Hi! Ask me anything about farming. Please enter your name & location.",
    "bot"
  );

})();
