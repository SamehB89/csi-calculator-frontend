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

// Store conversation state
let conversationState = {
  status: null,
  selected_item: null,
  matched_type: null,
  unit: null,
  history: []  // Add conversation history for context
};

async function sendMessage() {
  const input = document.getElementById("userInput");
  if (!input) return;
  
  const query = input.value.trim();
  if (!query) return;
  
  addMessage(query, "user");
  input.value = "";
  const loadingMsg = addLoading();
  
  // Add to conversation history
  conversationState.history.push({role: "user", content: query});

  try {
    // Build request based on conversation state
    const requestData = {
      query,
      lang: document.documentElement.lang,
      history: conversationState.history.slice(-30)  // Send last 30 messages for deep context
    };
    
    // If we're waiting for quantity and user entered a number
    if (conversationState.status === 'need_quantity' || conversationState.status === 'select_item') {
      const qtyMatch = query.match(/[\d.]+/);
      if (qtyMatch) {
        requestData.quantity = parseFloat(qtyMatch[0]);
        if (conversationState.selected_item) {
          requestData.item_code = conversationState.selected_item;
        }
      }
    }
    
    // Use intelligent-ai endpoint for real AI thinking
    const res = await fetch("/api/intelligent-ai", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestData)
    });
    const data = await res.json();
    loadingMsg.remove();

    // Update conversation state
    conversationState.status = data.status;
    
    // Render assistant text
    if (data.text) addMessage(data.text, "assistant");
    
    // Render CSI info if available
    if (data.csi_info && data.csi_info.best_match) {
      const csiHtml = renderCSIInfo(data.csi_info);
      addMessage(csiHtml, "assistant", true);
    }

    // If items are returned, show them as clickable options
    if (data.items && Array.isArray(data.items)) {
      const itemsHtml = buildItemsList(data.items, data.prompt);
      addMessage(itemsHtml, "assistant", true);
    }
    
    // If calculation result, show in table and Gantt
    if (data.status === 'calculated' && data.result) {
      const resultHtml = buildResultCard(data.result);
      addMessage(resultHtml, "assistant", true);
      
      // Build simple Gantt
      buildSimpleGantt(data.result);
    }

    // Render notes
    if (data.notes) addMessage(data.notes, "assistant");
  } catch (err) {
    if (loadingMsg) loadingMsg.remove();
    addMessage("حدث خطأ أثناء المعالجة. حاول مرة أخرى.", "assistant");
    console.error(err);
  }
}

function renderCSIInfo(csiInfo) {
  const match = csiInfo.best_match;
  const lang = document.documentElement.lang;
  
  const itemName = lang === 'ar' ? match.item_name_ar : match.item_name_en;
  const activities = match.typical_activities || [];
  const confidence = match.match_confidence || 0;
  
  let html = `
    <div class="csi-info-card">
      <div class="csi-info-header">
        <span class="csi-info-icon">📋</span>
        <h3 class="csi-info-title">${itemName}</h3>
      </div>
      
      <div class="csi-info-section">
        <div class="csi-info-label">${lang === 'ar' ? 'تصنيف CSI:' : 'CSI Classification:'}</div>
        <div>
          <span class="csi-division-badge">${match.csi_division}</span>
          <span class="csi-division-badge">${match.csi_section}</span>
        </div>
      </div>
      
      <div class="csi-info-section">
        <div class="csi-info-label">${lang === 'ar' ? 'الوحدة الافتراضية:' : 'Default Unit:'}</div>
        <div class="csi-info-value">${match.default_unit}</div>
      </div>
  `;
  
  if (activities.length > 0) {
    html += `
      <div class="csi-info-section">
        <div class="csi-info-label">${lang === 'ar' ? 'الأنشطة النموذجية:' : 'Typical Activities:'}</div>
        <ul class="csi-activities-list">
          ${activities.slice(0, 3).map(act => `<li>${act}</li>`).join('')}
        </ul>
      </div>
    `;
  }
  
  html += `
      <div class="csi-confidence">
        <span>${lang === 'ar' ? 'دقة المطابقة:' : 'Match Confidence:'}</span>
        <div class="csi-confidence-bar">
          <div class="csi-confidence-fill" style="width: ${confidence}%"></div>
        </div>
        <strong>${confidence}%</strong>
      </div>
    </div>
  `;
  
  return html;
}

function buildItemsList(items, prompt) {
  let html = `<div class="items-select-list">`;
  if (prompt) html += `<p class="items-prompt">${prompt}</p>`;
  
  items.forEach(item => {
    // Escape description for onclick (remove single quotes that might break JS)
    const safeDesc = (item.description || '').replace(/'/g, "\\'");
    html += `
      <div class="item-option" onclick="selectItem('${item.code}', '${safeDesc}', '${item.unit}')">
        <strong>${item.code}</strong>
        <span>${item.description}</span>
        <small>الوحدة: <strong>${item.unit}</strong> | الإنتاجية: ${item.daily_output || 'N/A'} ${item.unit}/يوم</small>
      </div>
    `;
  });
  
  html += `</div>`;
  return html;
}

function selectItem(code, description, unit) {
  conversationState.selected_item = code;
  conversationState.selected_unit = unit;
  addMessage(`✅ تم اختيار: ${description}`, "user");
  addMessage(`الرجاء إدخال الكمية بوحدة (${unit}):`, "assistant");
  document.getElementById("userInput").focus();
}

function buildResultCard(result) {
  return `
    <div class="result-card-ai">
      <div class="result-header">📊 نتيجة الحساب</div>
      <div class="result-row"><span>البند:</span> <strong>${result.description}</strong></div>
      <div class="result-row"><span>الكمية:</span> ${result.quantity} ${result.unit}</div>
      <div class="result-row"><span>الإنتاجية اليومية:</span> ${result.daily_output} ${result.unit}/يوم</div>
      <div class="result-row highlight"><span>⏱️ المدة:</span> <strong>${result.duration_days} يوم</strong></div>
      <div class="result-row"><span>👷 ساعات العمل:</span> ${result.total_man_hours} ساعة</div>
      <div class="result-row"><span>🔧 فريق العمل:</span> ${result.crew_structure || 'فريق قياسي'}</div>
    </div>
  `;
}

function buildSimpleGantt(result) {
  const ganttContent = document.getElementById('ganttContent');
  if (!ganttContent) return;
  
  const days = result.duration_days;
  
  ganttContent.innerHTML = `
    <div class="gantt-chart">
      <div class="gantt-bar">
        <div class="gantt-bar-label">${result.description.substring(0, 30)}...</div>
        <div class="gantt-bar-track">
          <div class="gantt-bar-fill" style="width: 100%">${days} يوم</div>
        </div>
      </div>
      <div class="gantt-bar" style="margin-top: 1rem; background: var(--primary-gradient); color: white;">
        <div class="gantt-bar-label">📅 إجمالي المدة</div>
        <div style="font-weight: 700; font-size: 1.25rem;">${days} يوم</div>
      </div>
    </div>
  `;
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
