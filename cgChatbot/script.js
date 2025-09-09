class MyraChatbot {
  constructor() {
    this.apiBaseUrl = "http://localhost:5000/api"; // backend ka base URL
    this.userId = this.generateUserId();
    this.isTyping = false;

    this.initializeElements();
    this.bindEvents();
    this.checkApiConnection();
  }

  // Initialize UI elements
  initializeElements() {
    this.chatMessages = document.getElementById("chatMessages");
    this.messageInput = document.getElementById("messageInput");
    this.sendButton = document.getElementById("sendButton");
    this.typingIndicator = document.getElementById("typingIndicator");
    this.characterCount = document.getElementById("characterCount");
    this.loadingOverlay = document.getElementById("loadingOverlay");
    this.errorToast = document.getElementById("errorToast");
    this.successToast = document.getElementById("successToast");
  }

  // Bind events (click, enter, typing counter)
  bindEvents() {
    this.sendButton.addEventListener("click", () => this.sendMessage());
    this.messageInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });
    this.messageInput.addEventListener("input", () => {
      const length = this.messageInput.value.length;
      this.characterCount.textContent = `${length}/500`;
      this.characterCount.style.color = length > 450 ? "#ef4444" : "#94a3b8";
    });
  }

  // Generate unique user ID
  generateUserId() {
    return "user_" + Math.random().toString(36).substr(2, 9) + "_" + Date.now();
  }

  // Check backend connection
  async checkApiConnection() {
    try {
      this.showLoading("Connecting to Myra...");
      const response = await fetch(`${this.apiBaseUrl}/careers`); // ✅ backend me /health nahi hai
      if (response.ok) {
        this.hideLoading();
        this.showSuccessToast("Connected to Myra successfully!");
      } else {
        throw new Error("API connection failed");
      }
    } catch (error) {
      this.hideLoading();
      this.showErrorToast(
        "Unable to connect to Myra. Please check if the server is running."
      );
    }
  }

  // Send message to backend
  async sendMessage() {
    const message = this.messageInput.value.trim();
    if (!message || this.isTyping) return;

    this.addMessage(message, "user");
    this.messageInput.value = "";
    this.characterCount.textContent = "0/500";
    this.showTypingIndicator();

    try {
      const response = await fetch(`${this.apiBaseUrl}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message, user_id: this.userId }),
      });

      const data = await response.json();
      this.hideTypingIndicator();

      if (data.reply) {
        this.addMessage(data.reply, "bot");
      } else {
        this.addMessage("❌ Bot did not respond.", "bot");
      }
    } catch (error) {
      this.hideTypingIndicator();
      this.addMessage("⚠️ Error: Cannot connect to the chatbot API.", "bot");
    }
  }

  // Add message to UI
  addMessage(content, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;
    const timestamp = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
    messageDiv.innerHTML = `
      <div class="${sender}-avatar">
        <i class="fas ${sender === "bot" ? "fa-robot" : "fa-user"}"></i>
      </div>
      <div class="message-content">
        <p>${content}</p>
        <div class="message-time">${timestamp}</div>
      </div>
    `;
    this.chatMessages.appendChild(messageDiv);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }

  // Typing indicator
  showTypingIndicator() {
    this.isTyping = true;
    this.typingIndicator.style.display = "flex";
    this.sendButton.disabled = true;
  }

  hideTypingIndicator() {
    this.isTyping = false;
    this.typingIndicator.style.display = "none";
    this.sendButton.disabled = false;
  }

  // Loading overlay
  showLoading(message = "Loading...") {
    this.loadingOverlay.style.display = "flex";
    this.loadingOverlay.querySelector("p").textContent = message;
  }

  hideLoading() {
    this.loadingOverlay.style.display = "none";
  }

  // Toasts
  showErrorToast(message) {
    document.getElementById("errorMessage").textContent = message;
    this.errorToast.style.display = "flex";
    setTimeout(() => this.hideErrorToast(), 5000);
  }

  hideErrorToast() {
    this.errorToast.style.display = "none";
  }

  showSuccessToast(message) {
    document.getElementById("successMessage").textContent = message;
    this.successToast.style.display = "flex";
    setTimeout(() => this.hideSuccessToast(), 3000);
  }

  hideSuccessToast() {
    this.successToast.style.display = "none";
  }
}

// Initialize chatbot
document.addEventListener("DOMContentLoaded", () => {
  window.chatbot = new MyraChatbot();
});
