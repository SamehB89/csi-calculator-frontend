// ========================================
// Language Toggle and i18n Support
// ========================================

const translations = {
    ar: {
        // Navbar
        home: 'الرئيسية',
        crewCalculator: 'حاسبة فريق العمل',
        aiPlanner: 'مساعد الذكاء',
        plannerTitle: '🤖 مساعد التخطيط الذكي',
        welcomeMsg: 'مرحبًا! أنا مساعد الذكاء. اكتب العمل المطلوب (مثال: أساسات منفصلة 100 م³ خرسانة) وسأقترح الأنشطة والمدة وفرق العمل.',
        searchPlaceholder: 'اكتب رسالتك...',

        // Browse Page
        browseTitle: 'قاعدة بيانات البناء CSI',
        searchPlaceholder: 'ابحث عن العناصر...',
        allDivisions: 'كل الأقسام الرئيسية',
        selectSub1: 'اختر القسم الفرعي الأول',
        selectSub2: 'اختر القسم الفرعي الثاني',
        searchBtn: 'بحث',
        divisions: 'الأقسام',
        items: 'العناصر',
        itemsFound: 'عنصر تم العثور عليه',
        code: 'الكود',
        description: 'الوصف',
        unit: 'الوحدة',
        output: 'الإنتاجية',
        actions: 'إجراءات',
        view: 'عرض',

        // Page Title
        pageTitle: '⚡ حاسبة فريق العمل والإنتاجية',

        // Division Selection Section
        divisionSelection: 'اختيار التقسيم الهرمي',
        divisionSelectionSubtitle: 'اختر التقسيمات للوصول إلى العنصر المطلوب',
        mainDivision: 'القسم الرئيسي (Main Division)',
        subDivision1: 'القسم الفرعي الأول (Sub-Division 1)',
        subDivision2: 'القسم الفرعي الثاني (Sub-Division 2)',
        itemDescription: 'وصف العنصر (Item Description)',

        // Item Details Section
        itemDetails: 'تفاصيل العنصر',
        dailyOutput: 'الإنتاج اليومي',
        manHours: 'ساعات العمل',
        equipHours: 'ساعات المعدات',
        crewStructure: 'تركيبة الفريق',
        crewDetailsTitle: 'تفاصيل أعضاء الفريق',
        crewMember: 'عضو الفريق',
        quantity: 'الكمية',
        descriptionAndRole: 'الوصف والوظيفة',

        // Quantity Input Section
        quantityInput: 'إدخال الكمية',
        requiredQuantity: 'الكمية المطلوبة',
        hoursPerDay: 'ساعات العمل اليومية',
        numberOfCrews: 'عدد فرق العمل',
        calculateBtn: 'احسب متطلبات الفريق',

        // Results Section
        results: 'النتائج والحسابات',
        numberOfCrewsResult: 'عدد فرق العمل',
        totalDailyOutput: 'الإنتاج اليومي الإجمالي',
        totalDays: 'إجمالي الأيام',
        totalManHours: 'ساعات العمل الإجمالية',
        totalEquipHours: 'ساعات المعدات الإجمالية',
        totalLabor: 'إجمالي العمالة',
        laborBreakdown: 'تفصيل فريق العمالة',
        equipmentBreakdown: 'تفصيل المعدات',
        position: 'الوظيفة',
        count: 'العدد',
        totalHours: 'إجمالي الساعات',
        equipment: 'المعدة',
        operatingHours: 'ساعات التشغيل',

        // Units
        crew: 'فريق',
        day: 'يوم',
        hour: 'ساعة',
        worker: 'عامل',
        perDay: '/يوم',
        perUnit: '/وحدة',
        hourPerDay: 'ساعة/يوم',

        // Placeholders
        selectMainDivision: '-- اختر القسم الرئيسي --',
        selectSubDivision1: '-- اختر القسم الفرعي الأول --',
        selectSubDivision2: '-- اختر القسم الفرعي الثاني --',
        selectItem: '-- اختر وصف العنصر --',
        enterQuantity: 'أدخل الكمية',

        // Errors
        invalidQuantity: 'الرجاء إدخال كمية صحيحة',
        invalidCrews: 'عدد فرق العمل يجب أن يكون واحد على الأقل',
        noItemSelected: 'لم يتم اختيار عنصر',
        noCrewData: 'لا توجد بيانات فريق متاحة',
        
        // AI Planner
        experimentalWarning: 'تحت الإنشاء - تجريبي'
    },
    en: {
        // Navbar
        home: 'Home',
        crewCalculator: 'Crew Calculator',
        aiPlanner: 'AI Chat Wizard',
        plannerTitle: '🤖 AI Construction Wizard',
        welcomeMsg: 'Hello! I am your AI assistant. Describe the work (e.g., Isolated foundations 100 m3 concrete) and I’ll propose tasks, duration, and crews.',
        searchPlaceholder: 'Type your message...',

        // Browse Page
        browseTitle: 'CSI Construction Database',
        searchPlaceholder: 'Search items...',
        allDivisions: 'All Divisions',
        selectSub1: 'Select Sub-Division 1',
        selectSub2: 'Select Sub-Division 2',
        searchBtn: 'Search',
        divisions: 'Divisions',
        items: 'Items',
        itemsFound: 'items found',
        code: 'Code',
        description: 'Description',
        unit: 'Unit',
        output: 'Output',
        actions: 'Actions',
        view: 'View',

        // Page Title
        pageTitle: '⚡ Crew & Productivity Calculator',

        // Division Selection Section
        divisionSelection: 'Division Selection',
        divisionSelectionSubtitle: 'Select divisions to reach the desired item',
        mainDivision: 'Main Division',
        subDivision1: 'Sub-Division 1',
        subDivision2: 'Sub-Division 2',
        itemDescription: 'Item Description',

        // Item Details Section
        itemDetails: 'Item Details',
        dailyOutput: 'Daily Output',
        manHours: 'Man Hours',
        equipHours: 'Equipment Hours',
        crewStructure: 'Crew Structure',
        crewDetailsTitle: 'Crew Member Details',
        crewMember: 'Crew Member',
        quantity: 'Quantity',
        descriptionAndRole: 'Description and Role',

        // Quantity Input Section
        quantityInput: 'Quantity Input',
        requiredQuantity: 'Required Quantity',
        hoursPerDay: 'Hours Per Day',
        numberOfCrews: 'Number of Crews',
        calculateBtn: 'Calculate Crew Requirements',

        // Results Section
        results: 'Results & Calculations',
        numberOfCrewsResult: 'Number of Crews',
        totalDailyOutput: 'Total Daily Output',
        totalDays: 'Total Days',
        totalManHours: 'Total Man Hours',
        totalEquipHours: 'Total Equipment Hours',
        totalLabor: 'Total Labor',
        laborBreakdown: 'Labor Crew Breakdown',
        equipmentBreakdown: 'Equipment Breakdown',
        position: 'Position',
        count: 'Count',
        totalHours: 'Total Hours',
        equipment: 'Equipment',
        operatingHours: 'Operating Hours',

        // Units
        crew: 'Crew',
        day: 'Day',
        hour: 'Hour',
        worker: 'Worker',
        perDay: '/Day',
        perUnit: '/Unit',
        hourPerDay: 'Hour/Day',

        // Placeholders
        selectMainDivision: '-- Select Main Division --',
        selectSubDivision1: '-- Select Sub-Division 1 --',
        selectSubDivision2: '-- Select Sub-Division 2 --',
        selectItem: '-- Select Item Description --',
        enterQuantity: 'Enter Quantity',

        // Errors
        invalidQuantity: 'Please enter a valid quantity',
        invalidCrews: 'Number of crews must be at least 1',
        noItemSelected: 'No item selected',
        noCrewData: 'No crew data available',
        
        // AI Planner
        experimentalWarning: 'Under Construction - Experimental'
    }
};

// Current language (default: Arabic)
window.currentLang = localStorage.getItem('csi_lang') || 'ar';

// Toggle between Arabic and English
function toggleLanguage() {
    window.currentLang = window.currentLang === 'ar' ? 'en' : 'ar';
    localStorage.setItem('csi_lang', window.currentLang);
    applyLanguage();
}

// Apply language to the entire page
function applyLanguage() {
    // Update HTML attributes
    document.documentElement.lang = currentLang;
    document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';

    // Update language toggle button
    const langIcon = document.getElementById('langIcon');
    if (langIcon) {
        langIcon.textContent = currentLang === 'ar' ? 'EN' : 'AR';
    }

    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[currentLang][key]) {
            // For input elements, only update if it's not an input/textarea
            if (element.tagName !== 'INPUT' && element.tagName !== 'TEXTAREA') {
                element.textContent = translations[currentLang][key];
            } else {
                element.placeholder = translations[currentLang][key];
            }
        }
    });

    // Update all input placeholders with data-i18n-placeholder
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        if (translations[currentLang][key]) {
            element.placeholder = translations[currentLang][key];
        }
    });

    // Update select options
    updateSelectOptions();
}

// Update dropdown placeholder options
function updateSelectOptions() {
    // Calculator Page Dropdowns
    const mainDiv = document.getElementById('mainDivision');
    const sub1Div = document.getElementById('subDivision1');
    const sub2Div = document.getElementById('subDivision2');
    const itemDesc = document.getElementById('itemDescription');

    // Index Page Dropdowns
    const divFilter = document.getElementById('division-filter');
    const sub1Filter = document.getElementById('subdiv1-filter');
    const sub2Filter = document.getElementById('subdiv2-filter');

    // Update Calculator Placeholders
    if (mainDiv && mainDiv.options[0]) mainDiv.options[0].text = translations[currentLang].selectMainDivision;
    if (sub1Div && sub1Div.options[0]) sub1Div.options[0].text = translations[currentLang].selectSubDivision1;
    if (sub2Div && sub2Div.options[0]) sub2Div.options[0].text = translations[currentLang].selectSubDivision2;
    if (itemDesc && itemDesc.options[0]) itemDesc.options[0].text = translations[currentLang].selectItem;

    // Update Index Page Placeholders
    if (divFilter && divFilter.options[0]) divFilter.options[0].text = translations[currentLang].allDivisions;
    if (sub1Filter && sub1Filter.options[0]) sub1Filter.options[0].text = translations[currentLang].selectSub1;
    if (sub2Filter && sub2Filter.options[0]) sub2Filter.options[0].text = translations[currentLang].selectSub2;
}

// Get translated text
function t(key) {
    return translations[currentLang][key] || key;
}

// Apply language on page load
document.addEventListener('DOMContentLoaded', () => {
    applyLanguage();
});
