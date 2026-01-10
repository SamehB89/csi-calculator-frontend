// EVM Calculator Logic

let performanceChart = null;
let sCurveChart = null;

function calculateEVM() {
    // Get input values
    const pv = parseFloat(document.getElementById('pv').value);
    const ev = parseFloat(document.getElementById('ev').value);
    const ac = parseFloat(document.getElementById('ac').value);
    const bac = parseFloat(document.getElementById('bac').value);
    const duration = parseFloat(document.getElementById('duration').value);
    const elapsed = parseFloat(document.getElementById('elapsed').value);
    
    // Validation
    if (isNaN(pv) || isNaN(ev) || isNaN(ac)) {
        alert('الرجاء إدخال القيم الأساسية (PV, EV, AC)');
        return;
    }
    
    if (pv <= 0 || ev < 0 || ac <= 0) {
        alert('القيم يجب أن تكون أكبر من صفر');
        return;
    }
    
    // Calculate variance indices
    const cv = ev - ac; // Cost Variance
    const sv = ev - pv; // Schedule Variance
    const cpi = ev / ac; // Cost Performance Index
    const spi = ev / pv; // Schedule Performance Index
    
    // Calculate forecasts
    let eac, etc, vac, tcpi;
    if (!isNaN(bac) && bac > 0) {
        eac = bac / cpi; // Estimate at Completion
        etc = eac - ac; // Estimate to Complete
        vac = bac - eac; // Variance at Completion
        
        // TCPI - To-Complete Performance Index
        const remainingWork = bac - ev;
        const remainingBudget = bac - ac;
        tcpi = remainingWork / remainingBudget;
    }
    
    // Calculate schedule performance
    let estimatedDuration, scheduleVarianceDays;
    if (!isNaN(duration) && !isNaN(elapsed) && duration > 0 && elapsed > 0) {
        estimatedDuration = duration / spi;
        scheduleVarianceDays = duration - estimatedDuration;
    }
    
    // Display results
    displayResults({
        cv, sv, cpi, spi,
        eac, etc, vac, tcpi,
        pv, ev, ac, bac,
        estimatedDuration, scheduleVarianceDays,
        duration, elapsed
    });
    
    // Show charts
    document.getElementById('chartsSection').style.display = 'block';
    createCharts({
        cv, sv, cpi, spi,
        pv, ev, ac, bac
    });
}

function displayResults(metrics) {
    const resultsDiv = document.getElementById('results');
    const isRTL = document.documentElement.dir === 'rtl';
    
    let html = '';
    
    // Cost Variance
    html += createResultItem(
        'CV - انحراف التكلفة',
        formatCurrency(metrics.cv),
        getVarianceStatus(metrics.cv, 'variance'),
        getVarianceInterpretation(metrics.cv, 'cost')
    );
    
    // Schedule Variance
    html += createResultItem(
        'SV - انحراف الجدول الزمني',
        formatCurrency(metrics.sv),
        getVarianceStatus(metrics.sv, 'variance'),
        getVarianceInterpretation(metrics.sv, 'schedule')
    );
    
    // Cost Performance Index
    html += createResultItem(
        'CPI - مؤشر أداء التكلفة',
        metrics.cpi.toFixed(3),
        getIndexStatus(metrics.cpi),
        getIndexInterpretation(metrics.cpi, 'cost')
    );
    
    // Schedule Performance Index
    html += createResultItem(
        'SPI - مؤشر أداء الجدول',
        metrics.spi.toFixed(3),
        getIndexStatus(metrics.spi),
        getIndexInterpretation(metrics.spi, 'schedule')
    );
    
    // Estimate at Completion
    if (metrics.eac) {
        html += createResultItem(
            'EAC - التقدير عند الإنجاز',
            formatCurrency(metrics.eac),
            getEACStatus(metrics.eac, metrics.bac),
            `التكلفة المتوقعة النهائية للمشروع`
        );
    }
    
    // Estimate to Complete
    if (metrics.etc) {
        html += createResultItem(
            'ETC - التقدير للإكمال',
            formatCurrency(metrics.etc),
            'status-info',
            `التكلفة المتوقعة لإكمال المشروع`
        );
    }
    
    // Variance at Completion
    if (metrics.vac) {
        html += createResultItem(
            'VAC - الانحراف عند الإنجاز',
            formatCurrency(metrics.vac),
            getVarianceStatus(metrics.vac, 'variance'),
            getVACInterpretation(metrics.vac)
        );
    }
    
    // TCPI
    if (metrics.tcpi) {
        html += createResultItem(
            'TCPI - مؤشر الأداء المطلوب للإكمال',
            metrics.tcpi.toFixed(3),
            getTCPIStatus(metrics.tcpi, metrics.cpi),
            getTCPIInterpretation(metrics.tcpi, metrics.cpi)
        );
    }
    
    // Schedule forecast
    if (metrics.estimatedDuration) {
        const unit = document.getElementById('unit').value;
        const unitLabel = unit === 'days' ? 'يوم' : (unit === 'weeks' ? 'أسبوع' : 'شهر');
        
        html += createResultItem(
            'المدة المتوقعة للإنجاز',
            `${metrics.estimatedDuration.toFixed(1)} ${unitLabel}`,
            getScheduleStatus(metrics.scheduleVarianceDays),
            `الفرق: ${Math.abs(metrics.scheduleVarianceDays).toFixed(1)} ${unitLabel} ${metrics.scheduleVarianceDays >= 0 ? 'توفير' : 'تأخير'}`
        );
    }
    
    resultsDiv.innerHTML = html;
}

function createResultItem(title, value, statusClass, interpretation) {
    return `
        <div class="result-item">
            <h3>${title}</h3>
            <div class="result-value">${value}</div>
            <div class="result-interpretation ${statusClass}">
                ${interpretation}
            </div>
        </div>
    `;
}

function formatCurrency(value) {
    if (value >= 0) {
        return new Intl.NumberFormat('ar-EG').format(value);
    } else {
        return `(${new Intl.NumberFormat('ar-EG').format(Math.abs(value))})`;
    }
}

function getVarianceStatus(value, type) {
    if (value > 0) return 'status-good';
    if (value >= -0.1 * Math.abs(value)) return 'status-warning';
    return 'status-danger';
}

function getIndexStatus(value) {
    if (value >= 1.0) return 'status-good';
    if (value >= 0.9) return 'status-warning';
    return 'status-danger';
}

function getEACStatus(eac, bac) {
    if (eac <= bac) return 'status-good';
    if (eac <= bac * 1.1) return 'status-warning';
    return 'status-danger';
}

function getScheduleStatus(variance) {
    if (variance >= 0) return 'status-good';
    if (variance >= -0.1) return 'status-warning';
    return 'status-danger';
}

function getTCPIStatus(tcpi, cpi) {
    if (tcpi <= cpi) return 'status-good';
    if (tcpi <= cpi * 1.1) return 'status-warning';
    return 'status-danger';
}

function getVarianceInterpretation(value, type) {
    const absValue = Math.abs(value);
    const typeAr = type === 'cost' ? 'التكلفة' : 'الجدول الزمني';
    
    if (value > 0) {
        return `✅ ممتاز! توفير في ${typeAr}`;
    } else if (value === 0) {
        return `⚪ ${typeAr} مطابق للخطة`;
    } else if (absValue <= 0.05 * absValue) {
        return `⚠️ انحراف بسيط في ${typeAr}`;
    } else {
        return `❌ انحراف كبير في ${typeAr} - يتطلب إجراءات تصحيحية`;
    }
}

function getIndexInterpretation(value, type) {
    const typeAr = type === 'cost' ? 'التكلفة' : 'الجدول';
    
    if (value >= 1.0) {
        const percentage = ((value - 1) * 100).toFixed(1);
        return `✅ أداء ممتاز! ${percentage}% أفضل من ${typeAr} المخطط`;
    } else if (value >= 0.9) {
        const percentage = ((1 - value) * 100).toFixed(1);
        return `⚠️ أداء مقبول - ${percentage}% أقل من ${typeAr} المخطط`;
    } else {
        const percentage = ((1 - value) * 100).toFixed(1);
        return `❌ أداء ضعيف - ${percentage}% أقل من ${typeAr} المخطط - يتطلب تدخل فوري`;
    }
}

function getVACInterpretation(vac) {
    if (vac > 0) {
        return `✅ المشروع متوقع أن ينتهي بتوفير في الميزانية`;
    } else if (vac === 0) {
        return `⚪ المشروع متوقع أن ينتهي بنفس الميزانية المخططة`;
    } else {
        return `❌ المشروع متوقع أن يتجاوز الميزانية المخططة`;
    }
}

function getTCPIInterpretation(tcpi, cpi) {
    if (tcpi <= cpi) {
        return `✅ الأداء الحالي كافٍ لإنهاء المشروع ضمن الميزانية`;
    } else if (tcpi <= cpi * 1.1) {
        return `⚠️ يتطلب تحسين طفيف في الأداء`;
    } else if (tcpi > 1) {
        return `❌ يتطلب تحسين كبير جداً في الأداء - قد يكون غير واقعي`;
    } else {
        return `❌ يتطلب تحسين ملحوظ في الأداء`;
    }
}

function createCharts(metrics) {
    // Destroy existing charts
    if (performanceChart) {
        performanceChart.destroy();
    }
    if (sCurveChart) {
        sCurveChart.destroy();
    }
    
    // Performance Chart
    const perfCtx = document.getElementById('performanceChart').getContext('2d');
    performanceChart = new Chart(perfCtx, {
        type: 'bar',
        data: {
            labels: ['CPI', 'SPI'],
            datasets: [{
                label: 'مؤشرات الأداء',
                data: [metrics.cpi, metrics.spi],
                backgroundColor: [
                    metrics.cpi >= 1 ? 'rgba(76, 175, 80, 0.8)' : 'rgba(244, 67, 54, 0.8)',
                    metrics.spi >= 1 ? 'rgba(76, 175, 80, 0.8)' : 'rgba(244, 67, 54, 0.8)'
                ],
                borderColor: [
                    metrics.cpi >= 1 ? 'rgb(76, 175, 80)' : 'rgb(244, 67, 54)',
                    metrics.spi >= 1 ? 'rgb(76, 175, 80)' : 'rgb(244, 67, 54)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'مؤشرات الأداء (يجب أن تكون >= 1.0)',
                    font: {
                        size: 16,
                        family: 'Inter'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        drawBorder: true,
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(2);
                        }
                    }
                }
            }
        }
    });
    
    // S-Curve Chart
    const sCurveCtx = document.getElementById('sCurveChart').getContext('2d');
    sCurveChart = new Chart(sCurveCtx, {
        type: 'line',
        data: {
            labels: ['البداية', 'الحالي', 'النهاية'],
            datasets: [
                {
                    label: 'القيمة المخططة (PV)',
                    data: [0, metrics.pv, metrics.bac || metrics.pv * 2],
                    borderColor: 'rgb(102, 126, 234)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: false
                },
                {
                    label: 'القيمة المكتسبة (EV)',
                    data: [0, metrics.ev, null],
                    borderColor: 'rgb(76, 175, 80)',
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    tension: 0.4,
                    fill: false
                },
                {
                    label: 'التكلفة الفعلية (AC)',
                    data: [0, metrics.ac, null],
                    borderColor: 'rgb(244, 67, 54)',
                    backgroundColor: 'rgba(244, 67, 54, 0.1)',
                    tension: 0.4,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'منحنى S - تقدم المشروع',
                    font: {
                        size: 16,
                        family: 'Inter'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        callback: function(value) {
                            return new Intl.NumberFormat('ar-EG', {
                                notation: 'compact',
                                compactDisplay: 'short'
                            }).format(value);
                        }
                    }
                }
            }
        }
    });
}

// Print function
function printResults() {
    window.print();
}

// Reset function
function resetCalculator() {
    document.getElementById('pv').value = '';
    document.getElementById('ev').value = '';
    document.getElementById('ac').value = '';
    document.getElementById('bac').value = '';
    document.getElementById('duration').value = '';
    document.getElementById('elapsed').value = '';
    
    document.getElementById('results').innerHTML = `
        <p style="text-align: center; color: var(--text-muted); padding: 2rem;">
            أدخل القيم في الحقول على اليسار واضغط على "احسب المؤشرات"
        </p>
    `;
    
    document.getElementById('chartsSection').style.display = 'none';
    
    if (performanceChart) {
        performanceChart.destroy();
        performanceChart = null;
    }
    if (sCurveChart) {
        sCurveChart.destroy();
        sCurveChart = null;
    }
}
