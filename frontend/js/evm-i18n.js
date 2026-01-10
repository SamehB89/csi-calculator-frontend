// EVM Calculator i18n Translations
const evmTranslations = {
    ar: {
        pageTitle: '📊 حاسبة إدارة القيمة المكتسبة (EVM)',
        pageSubtitle: 'احسب جميع مؤشرات أداء المشروع تلقائياً بأقل مدخلات',
        inputsTitle: '🔢 المدخلات',
        resultsTitle: '📈 النتائج',
        pvLabel: 'PV - القيمة المخططة (Planned Value)',
        pvHint: 'قيمة العمل المخطط إنجازه حتى تاريخ اليوم',
        pvPlaceholder: 'مثال: 500000',
        evLabel: 'EV - القيمة المكتسبة (Earned Value)',
        evHint: 'قيمة العمل المنجز فعلياً',
        evPlaceholder: 'مثال: 450000',
        acLabel: 'AC - التكلفة الفعلية (Actual Cost)',
        acHint: 'التكلفة الفعلية للعمل المنجز',
        acPlaceholder: 'مثال: 480000',
        bacLabel: 'BAC - ميزانية المشروع الكلية (Budget at Completion)',
        bacHint: 'إجمالي ميزانية المشروع',
        bacPlaceholder: 'مثال: 1000000',
        durationLabel: 'مدة المشروع الكلية',
        durationPlaceholder: 'مثال: 12',
        elapsedLabel: 'المدة المنقضية',
        elapsedPlaceholder: 'مثال: 6',
        unitLabel: 'الوحدة الزمنية',
        unitDays: 'أيام',
        unitWeeks: 'أسابيع',
        unitMonths: 'أشهر',
        calculateBtn: '🧮 احسب المؤشرات',
        resultsPlaceholder: 'أدخل القيم في الحقول على اليسار واضغط على "احسب المؤشرات"',
        cvTitle: 'CV - انحراف التكلفة',
        svTitle: 'SV - انحراف الجدول الزمني',
        cpiTitle: 'CPI - مؤشر أداء التكلفة',
        spiTitle: 'SPI - مؤشر أداء الجدول',
        eacTitle: 'EAC - التقدير عند الإنجاز',
        etcTitle: 'ETC - التقدير للإكمال',
        vacTitle: 'VAC - الانحراف عند الإنجاز',
        tcpiTitle: 'TCPI - مؤشر الأداء المطلوب للإكمال',
        estDurationTitle: 'المدة المتوقعة للإنجاز',
        chartsTitle: '📊 الرسوم البيانية',
        sCurveTitle: '📉 منحنى S',
        helpTitle: '📚 دليل الاستخدام السريع',
        metricsTitle: 'المؤشرات المحسوبة:',
        readingTitle: 'قراءة النتائج:',
        learnMore: '📖 تعلم المزيد:',
        statusGood: '✅ ممتاز!',
        statusWarning: '⚠️ تحذير',
        statusDanger: '❌ خطر',
        costSaving: 'توفير في التكلفة',
        costOverrun: 'تجاوز في التكلفة',
        scheduleAhead: 'متقدم عن الجدول',
        scheduleBehind: 'متأخر عن الجدول',
        performanceGood: 'أداء جيد',
        performanceAcceptable: 'أداء مقبول',
        performancePoor: 'أداء ضعيف',
        saving: 'توفير',
        delay: 'تأخير',
        validationError: 'الرجاء إدخال القيم الأساسية (PV, EV, AC)',
        valueError: 'القيم يجب أن تكون أكبر من صفر',
        performanceIndicators: 'مؤشرات الأداء (يجب أن تكون >= 1.0)',
        sCurveProgress: 'منحنى S - تقدم المشروع'
    },
    en: {
        pageTitle: '📊 Earned Value Management Calculator (EVM)',
        pageSubtitle: 'Calculate all project performance metrics automatically',
        inputsTitle: '🔢 Inputs',
        resultsTitle: '📈 Results',
        pvLabel: 'PV - Planned Value',
        pvHint: 'Value of work planned to be completed by today',
        pvPlaceholder: 'e.g., 500000',
        evLabel: 'EV - Earned Value',
        evHint: 'Value of work actually completed',
        evPlaceholder: 'e.g., 450000',
        acLabel: 'AC - Actual Cost',
        acHint: 'Actual cost of work completed',
        acPlaceholder: 'e.g., 480000',
        bacLabel: 'BAC - Budget at Completion',
        bacHint: 'Total project budget',
        bacPlaceholder: 'e.g., 1000000',
        durationLabel: 'Total Project Duration',
        durationPlaceholder: 'e.g., 12',
        elapsedLabel: 'Elapsed Duration',
        elapsedPlaceholder: 'e.g., 6',
        unitLabel: 'Time Unit',
        unitDays: 'Days',
        unitWeeks: 'Weeks',
        unitMonths: 'Months',
        calculateBtn: '🧮 Calculate Metrics',
        resultsPlaceholder: 'Enter values in the input fields and click "Calculate Metrics"',
        cvTitle: 'CV - Cost Variance',
        svTitle: 'SV - Schedule Variance',
        cpiTitle: 'CPI - Cost Performance Index',
        spiTitle: 'SPI - Schedule Performance Index',
        eacTitle: 'EAC - Estimate at Completion',
        etcTitle: 'ETC - Estimate to Complete',
        vacTitle: 'VAC - Variance at Completion',
        tcpiTitle: 'TCPI - To-Complete Performance Index',
        estDurationTitle: 'Estimated Duration',
        chartsTitle: '📊 Charts',
        sCurveTitle: '📉 S-Curve',
        helpTitle: '📚 Quick Reference Guide',
        metricsTitle: 'Calculated Metrics:',
        readingTitle: 'Reading Results:',
        learnMore: '📖 Learn More:',
        statusGood: '✅ Excellent!',
        statusWarning: '⚠️ Warning',
        statusDanger: '❌ Critical',
        costSaving: 'Under budget',
        costOverrun: 'Over budget',
        scheduleAhead: 'Ahead of schedule',
        scheduleBehind: 'Behind schedule',
        performanceGood: 'Good performance',
        performanceAcceptable: 'Acceptable performance',
        performancePoor: 'Poor performance',
        saving: 'savings',
        delay: 'delay',
        validationError: 'Please enter basic values (PV, EV, AC)',
        valueError: 'Values must be greater than zero',
        performanceIndicators: 'Performance Indices (should be >= 1.0)',
        sCurveProgress: 'S-Curve - Project Progress'
    }
};

// Get EVM translation
function evmT(key) {
    const lang = window.currentLang || 'ar';
    return evmTranslations[lang][key] || key;
}

// Apply EVM translations
function applyEvmTranslations() {
    const lang = window.currentLang || 'en';
    const t = evmTranslations[lang];
    
    // Update page elements
    document.querySelectorAll('[data-evm-i18n]').forEach(el => {
        const key = el.getAttribute('data-evm-i18n');
        if (t[key]) {
            if (el.tagName === 'INPUT') {
                el.placeholder = t[key];
            } else {
                el.textContent = t[key];
            }
        }
    });
}

// Override the original displayResults to use translations
const originalDisplayResults = typeof displayResults === 'function' ? displayResults : null;

// Listen for language changes
document.addEventListener('DOMContentLoaded', () => {
    applyEvmTranslations();
});
