/* ================================================
   E-Commerce AI Assistant — Enhanced Script
   ================================================ */

const chatBox       = document.getElementById("chatBox");
const chatForm      = document.getElementById("chatForm");
const questionInput = document.getElementById("questionInput");
const sendBtn       = document.getElementById("sendBtn");
const typingIndicator = document.getElementById("typingIndicator");

/* ── Helpers ── */
function getTime() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function getUserInitials() {
  return "You";
}

/* ── Add Message ── */
function addMessage(text, sender) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${sender}`;

  const isBot = sender === "bot";

  const avatar = document.createElement("div");
  avatar.className = `msg-avatar ${isBot ? "bot-avatar" : "user-avatar"}`;
  avatar.textContent = isBot ? "AI" : "Me";

  const bubble = document.createElement("div");
  bubble.className = "msg-bubble";

  const content = document.createElement("div");
  content.innerHTML = text;

  const time = document.createElement("div");
  time.className = "msg-time";
  time.textContent = getTime();

  bubble.appendChild(content);
  bubble.appendChild(time);

  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);

  chatBox.appendChild(wrapper);
  scrollToBottom();

  return { wrapper, bubble, content };
}

function scrollToBottom() {
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
}

/* ── Typing Indicator ── */
function showTyping() {
  typingIndicator.classList.add("visible");
  typingIndicator.style.display = "flex";
  scrollToBottom();
}
function hideTyping() {
  typingIndicator.classList.remove("visible");
  typingIndicator.style.display = "none";
}

/* ── Set input busy state ── */
function setLoading(state) {
  sendBtn.disabled = state;
  questionInput.disabled = state;
  if (state) showTyping(); else hideTyping();
}

/* ── Ask Assistant ── */
async function askAssistant(question) {
  addMessage(question, "user");
  setLoading(true);

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await response.json();
    setLoading(false);
    addMessage(formatAnswer(data.answer), "bot");
  } catch (error) {
    setLoading(false);
    addMessage(
      '⚠️ Something went wrong. Please check your internet connection and try again.',
      "bot"
    );
  }
}

/* ── Format bot answer — basic markdown-like rendering ── */
function formatAnswer(text) {
  if (!text) return "I couldn't find an answer. Please try again.";
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');
}

/* ── Form submit ── */
chatForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const question = questionInput.value.trim();
  if (!question) return;
  questionInput.value = "";
  askAssistant(question);
});

/* ── Quick question ── */
function sendQuickQuestion(question) {
  questionInput.value = question;
  askAssistant(question);
  questionInput.value = "";
  // scroll to chat
  chatBox.scrollIntoView({ behavior: "smooth" });
}

/* ── Clear chat ── */
function clearChat() {
  chatBox.innerHTML = "";
  addMessage(
    "👋 Chat cleared! How can I help you today?",
    "bot"
  );
}

/* ── Order Status Map ── */
const statusSteps = {
  "Delivered":   4,
  "Shipped":     3,
  "Processing":  2,
  "Pending":     1,
};

/* ── Track Order ── */
async function trackOrder() {
  const orderInput  = document.getElementById("orderInput");
  const orderResult = document.getElementById("orderResult");
  const orderTimeline = document.getElementById("orderTimeline");

  const orderId = orderInput.value.trim().toUpperCase();

  // Reset UI
  orderResult.className = "order-result";
  orderResult.style.display = "none";
  orderTimeline.style.display = "none";

  if (!orderId) {
    orderResult.className = "order-result error";
    orderResult.style.display = "block";
    orderResult.textContent = "⚠️ Please enter an order ID.";
    return;
  }

  try {
    const response = await fetch(`/api/order/${orderId}`);
    const data = await response.json();

    if (data.found) {
      orderResult.className = "order-result found";
      orderResult.style.display = "block";
      orderResult.innerHTML = `
        <strong>📦 Order ID:</strong> ${data.order_id}<br>
        <strong>🚦 Status:</strong> ${data.status}<br>
        <strong>📅 Expected Delivery:</strong> ${data.expected_delivery}<br>
        <small style="color:var(--text-muted)">${data.message || ""}</small>
      `;

      // Animate timeline
      showTimeline(data.status);
    } else {
      orderResult.className = "order-result error";
      orderResult.style.display = "block";
      orderResult.textContent = `❌ ${data.message || "Order not found."}`;
      orderTimeline.style.display = "none";
    }
  } catch (error) {
    orderResult.className = "order-result error";
    orderResult.style.display = "block";
    orderResult.textContent = "⚠️ Could not track order right now. Please try again.";
  }
}

function showTimeline(status) {
  const timeline = document.getElementById("orderTimeline");
  timeline.style.display = "block";

  const steps = timeline.querySelectorAll(".timeline-step");
  const activeStep = statusSteps[status] || 1;

  steps.forEach((step, i) => {
    step.classList.remove("done", "active");
    const stepNum = i + 1;

    setTimeout(() => {
      if (stepNum < activeStep) {
        step.classList.add("done");
      } else if (stepNum === activeStep) {
        step.classList.add("active");
      }
    }, i * 200);
  });
}

/* ── Allow Enter key in order input ── */
document.getElementById("orderInput").addEventListener("keydown", function (e) {
  if (e.key === "Enter") trackOrder();
});

/* ── 3D tilt effect on panels ── */
document.querySelectorAll(".panel").forEach(panel => {
  panel.addEventListener("mousemove", function (e) {
    const rect = panel.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const cx = rect.width  / 2;
    const cy = rect.height / 2;
    const rx = ((y - cy) / cy) * 3;
    const ry = ((x - cx) / cx) * -3;
    panel.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg)`;
  });
  panel.addEventListener("mouseleave", function () {
    panel.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg)";
    panel.style.transition = "transform 0.5s ease";
  });
  panel.addEventListener("mouseenter", function () {
    panel.style.transition = "transform 0.1s ease";
  });
});

/* ── Quick action 3D press effect ── */
document.querySelectorAll(".qa-btn").forEach(btn => {
  btn.addEventListener("click", function () {
    this.style.transform = "perspective(600px) rotateX(2deg) translateY(-2px) scale(0.96)";
    setTimeout(() => {
      this.style.transform = "";
    }, 200);
  });
});