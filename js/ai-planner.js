// Chat UI + backend integration + table rendering + Gantt chart + basic parsing assist.

// Theme Toggle
function toggleTheme() {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  const btn = document.getElementById('themeToggle');
  if (btn) btn.textContent = newTheme === 'dark' ? '☀️' : '🌙';
}

// Load saved theme
document.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  const btn = document.getElementById('themeToggle');
  if (btn) btn.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
  
  // Event Listeners
  const sendBtn = document.getElementById("sendBtn");
  if (sendBtn) sendBtn.addEventListener("click", sendMessage);
  
  const userInput = document.getElementById("userInput");
  if (userInput) {
      userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") sendMessage();
      });
  }
});

// Quick insert helper
function quickInsert(text) {
  const input = document.getElementById('userInput');
  if (input) {
      input.value = text;
      input.focus();
  }
}

function addMessage(text, role = "assistant", html = false) {
  const chat = document.getElementById("chatWindow");
  if (!chat) return;
  
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
  if (!input) return;
  
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
      
      // Build Gantt Chart
      buildGanttChart(data.table.rows);
    }

    // Render notes
    if (data.notes) addMessage(data.notes, "assistant");
  } catch (err) {
    if (loadingMsg) loadingMsg.remove();
    addMessage("حدث خطأ أثناء المعالجة. حاول مرة أخرى.", "assistant");
    console.error(err);
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

// Build Gantt Chart from table data
function buildGanttChart(rows) {
  const ganttContent = document.getElementById('ganttContent');
  if (!ganttContent) return;
  
  let totalDays = 0;
  rows.forEach(r => {
      const days = parseInt(r.duration) || 1;
      totalDays += days;
  });
  
  let html = '<div class="gantt-chart">';
  let cumulative = 0;
  
  rows.forEach((r, idx) => {
      const days = parseInt(r.duration) || 1;
      const startPercent = (cumulative / totalDays) * 100;
      const widthPercent = (days / totalDays) * 100;
      cumulative += days;
      
      html += `
          <div class="gantt-bar" style="animation-delay: ${idx * 0.1}s">
              <div class="gantt-bar-label">${r.task}</div>
              <div class="gantt-bar-track">
                  <div class="gantt-bar-fill" style="width: ${widthPercent}%; margin-right: ${startPercent}%">
                      ${days}d
                  </div>
              </div>
          </div>
      `;
  });
  
  html += `
      <div class="gantt-bar" style="margin-top: 1rem; background: var(--primary-gradient); color: white;">
          <div class="gantt-bar-label">📅 إجمالي المدة</div>
          <div style="font-weight: 700; font-size: 1.25rem;">${totalDays} يوم</div>
      </div>
  `;
  
  html += '</div>';
  ganttContent.innerHTML = html;
}
