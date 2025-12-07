const API_BASE = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    loadDivisions();
    setupEventListeners();
    searchItems(); // Load initial items

    // Initial language application
    if (typeof applyLanguage === 'function') {
        applyLanguage();
    }
});

function setupEventListeners() {
    document.getElementById('division-filter').addEventListener('change', handleDivisionChange);
    document.getElementById('subdiv1-filter').addEventListener('change', handleSubDiv1Change);
    document.getElementById('subdiv2-filter').addEventListener('change', handleSubDiv2Change);

    // Close modal when clicking outside
    window.onclick = function (event) {
        const modal = document.getElementById('details-modal');
        if (event.target == modal) {
            closeModal();
        }
    }
}

async function loadDivisions() {
    try {
        const response = await fetch(`${API_BASE}/divisions`);
        const divisions = await response.json();

        const select = document.getElementById('division-filter');
        const sidebar = document.getElementById('divisions-list');

        // Clear existing options except first
        select.innerHTML = '<option value="">All Divisions</option>';
        sidebar.innerHTML = '<h3>Divisions</h3>';

        divisions.forEach(div => {
            // Add to select
            const option = document.createElement('option');
            option.value = div.code;
            option.textContent = `${div.code} - ${div.name}`;
            select.appendChild(option);

            // Add to sidebar
            const divItem = document.createElement('div');
            divItem.className = 'division-item';
            divItem.textContent = `${div.code} - ${div.name}`;
            divItem.onclick = () => {
                select.value = div.code;
                handleDivisionChange();
            };
            sidebar.appendChild(divItem);
        });

        // Update placeholders after loading
        if (typeof updateSelectOptions === 'function') {
            updateSelectOptions();
        }
    } catch (error) {
        console.error('Error loading divisions:', error);
    }
}

async function handleDivisionChange() {
    const mainCode = document.getElementById('division-filter').value;
    const sub1Select = document.getElementById('subdiv1-filter');
    const sub2Select = document.getElementById('subdiv2-filter');

    // Reset child filters
    sub1Select.innerHTML = '<option value="">Select Sub-Division 1</option>';
    sub1Select.disabled = true;
    sub2Select.innerHTML = '<option value="">Select Sub-Division 2</option>';
    sub2Select.disabled = true;

    searchItems();

    if (!mainCode) return;

    try {
        const response = await fetch(`${API_BASE}/subdivisions1?main_code=${mainCode}`);
        const subs = await response.json();

        if (subs.length > 0) {
            sub1Select.disabled = false;
            subs.forEach(sub => {
                const option = document.createElement('option');
                option.value = sub.code;
                option.textContent = `${sub.code} - ${sub.name}`;
                sub1Select.appendChild(option);
            });
        }

        // Update placeholders after loading
        if (typeof updateSelectOptions === 'function') {
            updateSelectOptions();
        }
    } catch (error) {
        console.error('Error loading sub-divisions 1:', error);
    }
}

async function handleSubDiv1Change() {
    const sub1Code = document.getElementById('subdiv1-filter').value;
    const sub2Select = document.getElementById('subdiv2-filter');

    const mainCode = document.getElementById('division-filter').value;
    
    // Reset child filter
    sub2Select.innerHTML = '<option value="">Select Sub-Division 2</option>';
    sub2Select.disabled = true;

    searchItems();

    if (!sub1Code) return;

    try {
        const response = await fetch(`${API_BASE}/subdivisions2?sub1_code=${sub1Code}&main_code=${mainCode}`);
        const subs = await response.json();

        if (subs.length > 0) {
            sub2Select.disabled = false;
            subs.forEach(sub => {
                const option = document.createElement('option');
                option.value = sub.code;
                option.textContent = `${sub.code} - ${sub.name}`;
                sub2Select.appendChild(option);
            });
        }

        // Update placeholders after loading
        if (typeof updateSelectOptions === 'function') {
            updateSelectOptions();
        }
    } catch (error) {
        console.error('Error loading sub-divisions 2:', error);
    }
}

async function handleSubDiv2Change() {
    searchItems();
}

async function searchItems() {
    const searchQuery = document.getElementById('search-input').value;
    const mainDiv = document.getElementById('division-filter').value;
    const sub1 = document.getElementById('subdiv1-filter').value;
    const sub2 = document.getElementById('subdiv2-filter').value;

    let url = `${API_BASE}/items?`;
    if (searchQuery) url += `q=${encodeURIComponent(searchQuery)}&`;
    if (mainDiv) url += `main_code=${mainDiv}&`;
    if (sub1) url += `sub1_code=${sub1}&`;
    if (sub2) url += `sub2_code=${sub2}&`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error searching items:', error);
    }
}

function displayResults(data) {
    console.log('Search results:', data); // Debug log

    const tbody = document.querySelector('#items-table tbody');
    const countSpan = document.getElementById('results-count');

    tbody.innerHTML = '';

    let items = [];
    let count = 0;

    // Handle different response formats (array vs object)
    if (Array.isArray(data)) {
        items = data;
        count = data.length;
    } else if (data && Array.isArray(data.items)) {
        items = data.items;
        count = data.count || items.length;
    } else {
        console.error('Unexpected data format:', data);
        items = [];
        count = 0;
    }

    // Update count with translation handling
    const countText = translations && translations[window.currentLang] ? translations[window.currentLang].itemsFound : 'items found';
    countSpan.textContent = `${count} ${countText}`;

    if (items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No items found</td></tr>';
        return;
    }

    items.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.full_code || item.item_code}</td>
            <td>${item.description}</td>
            <td>${item.unit}</td>
            <td>${item.daily_output || '-'}</td>
            <td>
                <button class="view-btn" onclick="viewDetails('${item.full_code}')">
                    ${translations && translations[window.currentLang] ? translations[window.currentLang].view : 'View'}
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function viewDetails(code) {
    try {
        const response = await fetch(`${API_BASE}/item/${encodeURIComponent(code)}`);
        const item = await response.json();

        const modalBody = document.getElementById('modal-body');
        const modalTitle = document.getElementById('modal-title');

        // Get translations
        const t = (key) => translations && translations[window.currentLang] ? translations[window.currentLang][key] : key;

        modalTitle.textContent = `${item.full_code} - ${item.description}`;

        let crewHtml = '';
        if (item.crews && item.crews.length > 0) {
            crewHtml = `
                <div class="crew-details">
                    <h4>${t('crewStructure')}</h4>
                    <table class="crew-table">
                        <thead>
                            <tr>
                                <th>${t('code')}</th>
                                <th>${t('description')}</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${item.crews.map(c => `
                                <tr>
                                    <td>${c.code}</td>
                                    <td>${c.description}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        }

        modalBody.innerHTML = `
            <div class="item-details-grid">
                <div class="detail-card">
                    <h4>${t('dailyOutput')}</h4>
                    <p>${item.daily_output || '-'} / ${item.unit}</p>
                </div>
                <div class="detail-card">
                    <h4>${t('manHours')}</h4>
                    <p>${item.man_hours || '-'}</p>
                </div>
                <div class="detail-card">
                    <h4>${t('equipHours')}</h4>
                    <p>${item.equip_hours || '-'}</p>
                </div>
            </div>
            
            ${crewHtml}
        `;

        document.getElementById('details-modal').style.display = 'block';
    } catch (error) {
        console.error('Error loading details:', error);
    }
}

function closeModal() {
    document.getElementById('details-modal').style.display = 'none';
}
