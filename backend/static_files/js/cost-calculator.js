// ========================================
// Cost Calculator Module
// ========================================

// Note: window.currentCrewResults is defined in crew-calculator.html

// Currency symbol mapping
const currencySymbols = {
    EGP: { ar: 'ج.م.', en: 'EGP' },
    USD: { ar: '$', en: '$' },
    EUR: { ar: '€', en: '€' },
    GBP: { ar: '£', en: '£' },
    CNY: { ar: '¥', en: '¥' },
    SAR: { ar: 'ر.س.', en: 'SAR' },
    KWD: { ar: 'د.ك.', en: 'KWD' },
    QAR: { ar: 'ر.ق.', en: 'QAR' },
    OTHER: { ar: 'عملة', en: 'Currency' }
};

// Current selected currency
let selectedCurrency = 'EGP';
let customCurrencySymbol = '';

// Store current cost data
let currentCostData = {
    labor: [],
    equipment: [],
    materials: 0,
    profitMargin: 15,
    vatRate: 14
};

// Show cost section after crew calculation
function showCostSection() {
    if (!window.currentCrewResults) {
        showError(t('noCrewData'));
        return;
    }
    
    // Generate cost input fields based on crew results
    generateLaborCostInputs();
    generateEquipmentCostInputs();
    
    // Set unit label
    const unitLabel = document.getElementById('unitLabel');
    if (unitLabel && window.currentCrewResults.item) {
        unitLabel.textContent = window.currentCrewResults.item.unit || t('unit');
    }
    
    // Load saved prices if available
    loadSavedPrices();
    
    // Show the section
    document.getElementById('costSection').style.display = 'block';
    document.getElementById('costSection').scrollIntoView({ behavior: 'smooth' });
}

// Generate labor cost input fields
function generateLaborCostInputs() {
    const container = document.getElementById('laborCostInputs');
    if (!container || !window.currentCrewResults || !window.currentCrewResults.crew) return;
    
    const labor = window.currentCrewResults.crew.labor || [];
    const totalDays = window.currentCrewResults.calculations.total_days || 1;
    
    container.innerHTML = '';
    
    if (labor.length === 0) {
        container.innerHTML = '<p class="no-data">لا توجد بيانات عمالة</p>';
        return;
    }
    
    labor.forEach((member, index) => {
        const currencyUnit = getCurrencyUnit('day');
        const itemHtml = `
            <div class="cost-input-item" data-type="labor" data-index="${index}">
                <label>
                    <span class="input-label">${member.position}</span>
                    <span class="input-details">${member.count} ${t('worker')} × ${totalDays.toFixed(1)} ${t('day')}</span>
                </label>
                <div class="input-with-unit">
                    <input type="number" 
                           class="cost-input labor-price" 
                           id="laborPrice_${index}"
                           data-count="${member.count}"
                           data-days="${totalDays}"
                           data-position="${member.position}"
                           placeholder="0" 
                           min="0" 
                           oninput="calculateTotalCost()">
                    <span class="unit labor-unit">${currencyUnit}</span>
                    <span class="auto-calculation" id="laborCalc_${index}">= 0 ${getCurrencySymbol()}</span>
                </div>
            </div>
        `;
        container.innerHTML += itemHtml;
    });
}

// Generate equipment cost input fields
function generateEquipmentCostInputs() {
    const container = document.getElementById('equipmentCostInputs');
    if (!container || !window.currentCrewResults || !window.currentCrewResults.crew) return;
    
    const equipment = window.currentCrewResults.crew.equipment || [];
    
    container.innerHTML = '';
    
    if (equipment.length === 0) {
        container.innerHTML = '<p class="no-data">لا توجد معدات مطلوبة</p>';
        return;
    }
    
    equipment.forEach((equip, index) => {
        const currencyUnit = getCurrencyUnit('hour');
        const itemHtml = `
            <div class="cost-input-item" data-type="equipment" data-index="${index}">
                <label>
                    <span class="input-label">${equip.position}</span>
                    <span class="input-details">${equip.count} × ${equip.total_hours.toFixed(1)} ${t('hour')}</span>
                </label>
                <div class="input-with-unit">
                    <input type="number" 
                           class="cost-input equipment-price" 
                           id="equipPrice_${index}"
                           data-count="${equip.count}"
                           data-hours="${equip.total_hours}"
                           data-position="${equip.position}"
                           placeholder="0" 
                           min="0" 
                           oninput="calculateTotalCost()">
                    <span class="unit equipment-unit">${currencyUnit}</span>
                    <span class="auto-calculation" id="equipCalc_${index}">= 0 ${getCurrencySymbol()}</span>
                </div>
            </div>
        `;
        container.innerHTML += itemHtml;
    });
}

// Toggle materials section
function toggleMaterialsSection() {
    const checkbox = document.getElementById('includeMaterials');
    const section = document.getElementById('materialsCostSection');
    const subtotalRow = document.getElementById('materialsSubtotalRow');
    const summaryRow = document.getElementById('summaryMaterialsRow');
    
    if (checkbox.checked) {
        section.style.display = 'block';
        subtotalRow.style.display = 'flex';
        summaryRow.style.display = 'flex';
        
        // Set hint with quantity
        const hint = document.getElementById('materialsHint');
        if (hint && window.currentCrewResults) {
            const qty = window.currentCrewResults.input.quantity || 0;
            const unit = window.currentCrewResults.item.unit || 'وحدة';
            hint.textContent = `للكمية: ${qty} ${unit}`;
        }
    } else {
        section.style.display = 'none';
        subtotalRow.style.display = 'none';
        summaryRow.style.display = 'none';
        document.getElementById('materialsCost').value = '';
    }
    
    calculateTotalCost();
}

// Calculate total cost
function calculateTotalCost() {
    let laborTotal = 0;
    let equipmentTotal = 0;
    let materialsTotal = 0;
    
    // Calculate labor costs
    document.querySelectorAll('.labor-price').forEach((input, index) => {
        const price = parseFloat(input.value) || 0;
        const count = parseFloat(input.dataset.count) || 0;
        const days = parseFloat(input.dataset.days) || 0;
        const total = price * count * days;
        
        laborTotal += total;
        
        const calcSpan = document.getElementById(`laborCalc_${index}`);
        if (calcSpan) {
            calcSpan.textContent = `= ${formatCurrency(total)}`;
        }
    });
    
    // Calculate equipment costs
    document.querySelectorAll('.equipment-price').forEach((input, index) => {
        const price = parseFloat(input.value) || 0;
        const count = parseFloat(input.dataset.count) || 0;
        const hours = parseFloat(input.dataset.hours) || 0;
        const total = price * count * hours;
        
        equipmentTotal += total;
        
        const calcSpan = document.getElementById(`equipCalc_${index}`);
        if (calcSpan) {
            calcSpan.textContent = `= ${formatCurrency(total)}`;
        }
    });
    
    // Calculate materials cost
    if (document.getElementById('includeMaterials').checked) {
        materialsTotal = parseFloat(document.getElementById('materialsCost').value) || 0;
    }
    
    // Get modifiers
    const profitMargin = parseFloat(document.getElementById('profitMargin').value) || 0;
    const vatRate = parseFloat(document.getElementById('vatRate').value) || 0;
    
    // Calculate totals
    const baseCost = laborTotal + equipmentTotal + materialsTotal;
    const profitAmount = baseCost * (profitMargin / 100);
    const beforeVat = baseCost + profitAmount;
    const vatAmount = beforeVat * (vatRate / 100);
    const grandTotal = beforeVat + vatAmount;
    
    // Calculate unit price
    const quantity = window.currentCrewResults ? (window.currentCrewResults.input.quantity || 1) : 1;
    const unitPrice = grandTotal / quantity;
    
    // Update UI
    document.getElementById('laborTotalCost').textContent = formatCurrency(laborTotal);
    document.getElementById('equipmentTotalCost').textContent = formatCurrency(equipmentTotal);
    document.getElementById('materialsTotalCost').textContent = formatCurrency(materialsTotal);
    
    document.getElementById('summaryLabor').textContent = formatCurrency(laborTotal);
    document.getElementById('summaryEquipment').textContent = formatCurrency(equipmentTotal);
    document.getElementById('summaryMaterials').textContent = formatCurrency(materialsTotal);
    document.getElementById('summaryBaseCost').textContent = formatCurrency(baseCost);
    
    document.getElementById('profitPercent').textContent = profitMargin;
    document.getElementById('summaryProfit').textContent = formatCurrency(profitAmount);
    document.getElementById('summaryBeforeVat').textContent = formatCurrency(beforeVat);
    
    document.getElementById('vatPercent').textContent = vatRate;
    document.getElementById('summaryVat').textContent = formatCurrency(vatAmount);
    
    document.getElementById('summaryGrandTotal').textContent = formatCurrency(grandTotal);
    // Update New Overall Cost Row
    const overallCostElem = document.getElementById('summaryOverallCost');
    if(overallCostElem) overallCostElem.textContent = formatCurrency(grandTotal);
    
    document.getElementById('summaryUnitPrice').innerHTML = `${formatCurrency(unitPrice)}/<span id="unitLabel">${window.currentCrewResults?.item?.unit || 'وحدة'}</span>`;
    
    // Store current data
    currentCostData = {
        laborTotal,
        equipmentTotal,
        materialsTotal,
        baseCost,
        profitMargin,
        profitAmount,
        beforeVat,
        vatRate,
        vatAmount,
        grandTotal,
        unitPrice
    };
}

// Format currency with selected symbol
function formatCurrency(value) {
    const lang = window.currentLang || 'ar';
    let symbol;
    
    if (selectedCurrency === 'OTHER' && customCurrencySymbol) {
        symbol = customCurrencySymbol;
    } else {
        symbol = currencySymbols[selectedCurrency]?.[lang] || currencySymbols[selectedCurrency]?.ar || 'ج.م.';
    }
    
    return new Intl.NumberFormat(lang === 'ar' ? 'ar-EG' : 'en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value) + ' ' + symbol;
}

// Get currency symbol based on current selection
function getCurrencySymbol() {
    const lang = window.currentLang || 'ar';
    if (selectedCurrency === 'OTHER' && customCurrencySymbol) {
        return customCurrencySymbol;
    }
    return currencySymbols[selectedCurrency]?.[lang] || currencySymbols[selectedCurrency]?.ar || 'ج.م.';
}

// Get currency unit with time period (day/hour)
function getCurrencyUnit(period) {
    const lang = window.currentLang || 'ar';
    const symbol = getCurrencySymbol();
    
    if (period === 'day') {
        return lang === 'ar' ? `${symbol}/يوم` : `${symbol}/Day`;
    } else if (period === 'hour') {
        return lang === 'ar' ? `${symbol}/ساعة` : `${symbol}/Hour`;
    }
    return symbol;
}

// Update all unit labels when currency changes
function updateCurrencyUnits() {
    // Update labor units
    document.querySelectorAll('.labor-unit').forEach(el => {
        el.textContent = getCurrencyUnit('day');
    });
    
    // Update equipment units
    document.querySelectorAll('.equipment-unit').forEach(el => {
        el.textContent = getCurrencyUnit('hour');
    });
}

// Initialize currency selector
function initCurrencySelector() {
    const currencySelect = document.getElementById('currencySelect');
    const customInput = document.getElementById('customCurrency');
    
    if (currencySelect) {
        currencySelect.addEventListener('change', function() {
            selectedCurrency = this.value;
            
            if (selectedCurrency === 'OTHER') {
                customInput.classList.remove('hidden');
                customInput.focus();
            } else {
                customInput.classList.add('hidden');
                customCurrencySymbol = '';
            }
            
            updateCurrencyUnits();
            calculateTotalCost();
        });
    }
    
    if (customInput) {
        customInput.addEventListener('input', function() {
            customCurrencySymbol = this.value.trim();
            updateCurrencyUnits();
            calculateTotalCost();
        });
    }
}

// Call init when DOM is ready
document.addEventListener('DOMContentLoaded', initCurrencySelector);

// Save prices to local storage
function savePricesToStorage() {
    const prices = {
        labor: {},
        equipment: {},
        profitMargin: parseFloat(document.getElementById('profitMargin').value) || 15,
        vatRate: parseFloat(document.getElementById('vatRate').value) || 14
    };
    
    // Save labor prices
    document.querySelectorAll('.labor-price').forEach(input => {
        const position = input.dataset.position;
        const price = parseFloat(input.value) || 0;
        if (price > 0) {
            prices.labor[position] = price;
        }
    });
    
    // Save equipment prices
    document.querySelectorAll('.equipment-price').forEach(input => {
        const position = input.dataset.position;
        const price = parseFloat(input.value) || 0;
        if (price > 0) {
            prices.equipment[position] = price;
        }
    });
    
    localStorage.setItem('csi_saved_prices', JSON.stringify(prices));
    
    // Show success message
    showSuccessMessage(t('pricesSaved'));
}

// Load saved prices from local storage
function loadSavedPrices() {
    const savedPrices = localStorage.getItem('csi_saved_prices');
    if (!savedPrices) return;
    
    try {
        const prices = JSON.parse(savedPrices);
        
        // Load labor prices
        document.querySelectorAll('.labor-price').forEach(input => {
            const position = input.dataset.position;
            if (prices.labor && prices.labor[position]) {
                input.value = prices.labor[position];
            }
        });
        
        // Load equipment prices
        document.querySelectorAll('.equipment-price').forEach(input => {
            const position = input.dataset.position;
            if (prices.equipment && prices.equipment[position]) {
                input.value = prices.equipment[position];
            }
        });
        
        // Load modifiers
        if (prices.profitMargin !== undefined) {
            document.getElementById('profitMargin').value = prices.profitMargin;
        }
        if (prices.vatRate !== undefined) {
            document.getElementById('vatRate').value = prices.vatRate;
        }
        
        // Recalculate
        calculateTotalCost();
        
        showSuccessMessage(t('pricesLoaded'));
    } catch (e) {
        console.error('Error loading saved prices:', e);
    }
}

// Clear all prices and reset to defaults
function clearAllPrices() {
    // Clear all labor price inputs
    document.querySelectorAll('.labor-price').forEach(input => {
        input.value = '';
    });
    
    // Clear all equipment price inputs
    document.querySelectorAll('.equipment-price').forEach(input => {
        input.value = '';
    });
    
    // Clear materials cost
    const materialsCost = document.getElementById('materialsCost');
    if (materialsCost) materialsCost.value = '';
    
    // Reset modifiers to defaults
    const profitMargin = document.getElementById('profitMargin');
    const vatRate = document.getElementById('vatRate');
    if (profitMargin) profitMargin.value = '15';
    if (vatRate) vatRate.value = '14';
    
    // Clear saved prices from localStorage
    localStorage.removeItem('csi_saved_prices');
    
    // Recalculate
    calculateTotalCost();
    
    showSuccessMessage(t('pricesCleared'));
}

// Show success message
function showSuccessMessage(message) {
    // Remove existing messages
    const existing = document.querySelector('.success-message');
    if (existing) existing.remove();
    
    const msgDiv = document.createElement('div');
    msgDiv.className = 'success-message';
    msgDiv.textContent = '✅ ' + message;
    
    const actions = document.querySelector('.cost-actions');
    if (actions) {
        actions.insertAdjacentElement('afterend', msgDiv);
        
        setTimeout(() => {
            msgDiv.remove();
        }, 3000);
    }
}

// Generate PDF report
function generateCostPDF() {
    // Check if jsPDF is loaded
    if (typeof jspdf === 'undefined' && typeof jsPDF === 'undefined') {
        // Load jsPDF dynamically
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
        script.onload = () => {
            generateCostPDFContent();
        };
        document.head.appendChild(script);
    } else {
        generateCostPDFContent();
    }
}

// Helper to load image
function loadImage(url) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.src = url;
        img.crossOrigin = 'Anonymous';
        img.onload = () => resolve(img);
        img.onerror = () => {
            // If fails, resolve with null so we can continue without image
            console.warn('Failed to load image:', url);
            resolve(null);
        };
    });
}

// Generate PDF Content (Async)
async function generateCostPDFContent() {
    const costSection = document.getElementById('costSection');
    const resultsSection = document.getElementById('resultsSection');
    
    // Hide visibility of specified elements (buttons)
    const elementsToHide = document.querySelectorAll('.cost-actions, .calculate-btn, #showCostBtn');
    elementsToHide.forEach(el => {
        el.setAttribute('data-original-display', el.style.display || '');
        el.style.display = 'none';
    });
    
    try {
        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF('p', 'mm', 'a4');
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = pdf.internal.pageSize.getHeight();
        const margin = 10;
        const headerHeight = 30;
        
        // Load Header Image
        const headerImg = await loadImage('assets/csi_header.png');
        
        // Define Header Drawing Function
        const drawHeader = (doc) => {
            // Header Background (white)
            doc.setFillColor(255, 255, 255);
            doc.rect(0, 0, pdfWidth, headerHeight, 'F');
            
            // Header Image (Left)
            if (headerImg) {
                const imgRatio = headerImg.width / headerImg.height;
                const imgH = 20;
                const imgW = imgH * imgRatio;
                doc.addImage(headerImg, 'PNG', margin, 5, imgW, imgH);
            } else {
                // Fallback text
                doc.setFont('times', 'bold');
                doc.setFontSize(14);
                doc.setTextColor(0, 0, 0);
                doc.text('CSI+Sameh', margin, 18);
            }
            
            // Text "CSI-Calculator" (Right)
            doc.setFont('times', 'bold');
            doc.setFontSize(16);
            doc.setTextColor(0, 0, 0);
            doc.text('CSI-Calculator', pdfWidth - margin, 18, { align: 'right' });
            
            // Separator Line (Purple)
            doc.setDrawColor(102, 126, 234);
            doc.setLineWidth(0.5);
            doc.line(margin, 28, pdfWidth - margin, 28);
        };
        
        // Initialize PDF
        let cursorY = headerHeight + 5;
        drawHeader(pdf);
        
        // ========== PAGE 1: Results Section ==========
        if (resultsSection && resultsSection.style.display !== 'none') {
            const canvas = await html2canvas(resultsSection, {
                scale: 2,
                useCORS: true,
                logging: false,
                backgroundColor: null // Preserve original colors!
            });
            
            const imgWidth = pdfWidth - (margin * 2);
            const imgHeight = (canvas.height * imgWidth) / canvas.width;
            
            const imgData = canvas.toDataURL('image/png');
            pdf.addImage(imgData, 'PNG', margin, cursorY, imgWidth, imgHeight);
            
            cursorY += imgHeight + 5;
        }
        
        // ========== PAGE 2+: Cost Calculator Section (NEW PAGE) ==========
        if (costSection && costSection.style.display !== 'none') {
            // Start Cost Calculator on a NEW PAGE
            pdf.addPage();
            drawHeader(pdf);
            cursorY = headerHeight + 5;
            
            // Capture each child of cost section
            const costChildren = Array.from(costSection.children);
            for (const child of costChildren) {
                if (child.classList.contains('cost-actions') || 
                    child.classList.contains('section-header') === false && 
                    child.style.display === 'none') continue;
                if (child.offsetHeight === 0) continue;
                
                const canvas = await html2canvas(child, {
                    scale: 2,
                    useCORS: true,
                    logging: false,
                    backgroundColor: null // Preserve original colors!
                });
                
                const imgWidth = pdfWidth - (margin * 2);
                const imgHeight = (canvas.height * imgWidth) / canvas.width;
                
                // Check page overflow
                if (cursorY + imgHeight > pdfHeight - margin) {
                    pdf.addPage();
                    drawHeader(pdf);
                    cursorY = headerHeight + 5;
                }
                
                const imgData = canvas.toDataURL('image/png');
                pdf.addImage(imgData, 'PNG', margin, cursorY, imgWidth, imgHeight);
                
                cursorY += imgHeight + 2;
            }
        }
        
        // Save
        const filename = window.currentCrewResults?.item?.description 
            ? `Cost_Report_${window.currentCrewResults.item.description.substring(0, 30)}.pdf`
            : 'Cost_Report.pdf';
        
        pdf.save(filename);
        showSuccessMessage(t('pdfGenerated') || 'تم إنشاء التقرير بنجاح (PDF)!');
        
    } catch (err) {
        console.error('PDF Generation Error:', err);
        showError('فشل في إنشاء ملف PDF');
    } finally {
        // Restore elements
        elementsToHide.forEach(el => {
            el.style.display = el.getAttribute('data-original-display');
        });
    }
}
