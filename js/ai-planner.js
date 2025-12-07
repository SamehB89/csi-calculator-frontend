// Chat UI + backend integration + table rendering + basic parsing assist.

function addMessage(text, role = "assistant", html = false) {
  const chat = document.getElementById("chatWindow");
  const msg = document.createElement("div");
  msg.className = `message ${role}`;
  if (html) {
    msg.innerHTML = text;
  } else {
    msg.textContent = text;
  }
  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
  return msg;
}

function addLoading() {
  const m = addMessage(`<span class="loading-dots">جاري المعالجة</span>`, "assistant", true);
  return m;
}

async function sendMessage() {
  const input = document.getElementById("userInput");
  const query = input.value.trim();
  if (!query) return;
  addMessage(query, "user");
  input.value = "";
  const loadingMsg = addLoading();

  try {
    const res = await fetch("/api/ai", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query,
        lang: document.documentElement.lang
      })
    });
    const data = await res.json();
    loadingMsg.remove();

    // Render assistant text
    if (data.text) addMessage(data.text, "assistant");

    // Render table if provided
    if (data.table && Array.isArray(data.table.rows)) {
      const tableHtml = buildResultTable(data.table);
      addMessage(tableHtml, "assistant", true);
    }

    // Render notes or gantt summary
    if (data.notes) addMessage(data.notes, "assistant");
  } catch (err) {
    loadingMsg.remove();
    addMessage("حدث خطأ أثناء المعالجة. حاول مرة أخرى.", "assistant");
  }
}

function buildResultTable(tbl) {
  const lang = document.documentElement.lang;
  const th = lang === "ar"
    ? ["النشاط", "الكمية", "الوحدة", "فريق العمل", "المعدات", "المُدة"]
    : ["Task", "Qty", "Unit", "Crew", "Equipment", "Duration"];

  let html = `<table class="chat-result-table"><thead><tr>`;
  th.forEach(h => html += `<th>${h}</th>`);
  html += `</tr></thead><tbody>`;

  tbl.rows.forEach(r => {
    html += `<tr>
      <td>${r.task}</td>
      <td>${r.qty}</td>
      <td>${r.unit}</td>
      <td>${r.crew}</td>
      <td>${r.equipment}</td>
      <td>${r.duration}</td>
    </tr>`;
  });

  html += `</tbody></table>`;
  return html;
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("sendBtn").addEventListener("click", sendMessage);
  document.getElementById("userInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});
