(function () {
  // 1️⃣ Inject CSS
  const css = document.createElement("link");
  css.rel = "stylesheet";
  css.href = "/static/widget/chatbot.css";
  document.head.appendChild(css);

  // 2️⃣ Create widget HTML
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
        <input
          id="chat-input"
          type="text"
          placeholder="Ask your farming question..."
        />
        <button id="chat-send">➤</button>
      </div>
    </div>
  `;

  document.body.appendChild(widget);

  // 3️⃣ Get elements
  const toggleBtn = document.getElementById("chat-toggle");
  const chatBox = document.getElementById("chat-box");
  const closeBtn = document.getElementById("chat-close");
  const chatBody = document.getElementById("chat-body");
  const chatInput = document.getElementById("chat-input");
  const sendBtn = document.getElementById("chat-send");

  // 4️⃣ Toggle logic
  toggleBtn.onclick = () => chatBox.classList.toggle("hidden");
  closeBtn.onclick = () => chatBox.classList.add("hidden");

  // 5️⃣ Add message to UI
  function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = `msg ${sender}`;
    msg.innerText = text;
    chatBody.appendChild(msg);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  // 6️⃣ Send message to backend
  async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    addMessage(text, "user");
    chatInput.value = "";

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      const data = await response.json();
      addMessage(data.reply || "No response from server.", "bot");

    } catch (error) {
      addMessage("Server not reachable. Please try again.", "bot");
    }
  }

  // 7️⃣ Events
  sendBtn.onclick = sendMessage;
  chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  // 8️⃣ Welcome message
  addMessage("👋 Hello! I’m FarmFluence AI. How can I help you today?", "bot");
})();

