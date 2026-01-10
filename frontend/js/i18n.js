// ========================================
// Language Toggle and i18n Support
// ========================================

const translations = {
    ar: {
        // Navbar
        home: 'الرئيسية',
        crewCalculator: 'حاسبة فريق العمل',
        aiPlanner: 'مساعد الذكاء',
        evmCalculator: 'حاسبة EVM',
        blog: 'دليل التشغيل+مقالات فنية',
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
        calculateBtn: 'احسب متطلبات الفريق والمدة الزمنية للنشاط',

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
        
        // Quick Search
        quickSearchPlaceholder: 'اكتب وصف العنصر باللغة الانجليزية (Item Description) مثل Raft, Column, Plaster... الخ',
        orSelectFromSections: 'أو اختر من الأقسام',
        
        inputPlaceholder: 'Type a message...',
        
        // Cost Calculator
        calculateDetailedCost: 'احسب التكلفة التفصيلية',
        costCalculatorTitle: '💰 حساب التكلفة التفصيلية',
        enterMarketPrices: 'أدخل الأسعار الفعلية من السوق المحلي',
        laborCostTitle: '👷 تكلفة العمالة',
        laborCostNote: 'أدخل سعر اليوم الواحد لكل نوع عامل',
        equipmentCostTitle: '🚜 تكلفة المعدات',
        equipmentCostNote: 'أدخل سعر الساعة الواحدة لكل معدة',
        materialsTitle: '📦 إضافة تكلفة المواد الخام (اختياري)',
        materialsNote: 'أدخل تكلفة المواد الخام للكمية الإجمالية',
        materialsInputLabel: 'تكلفة المواد الإجمالية',
        modifiersTitle: '📊 هامش الربح والضرائب',
        profitMarginLabel: 'هامش الربح (%)',
        vatRateLabel: 'ضريبة القيمة المضافة (%)',
        costSummaryTitle: '🧾 ملخص التكلفة التقديري',
        summaryLabor: 'تكلفة العمالة',
        summaryEquipment: 'تكلفة المعدات',
        summaryMaterials: 'تكلفة المواد',
        summaryBaseCost: 'التكلفة الأساسية',
        summaryProfit: 'هامش الربح',
        summaryBeforeVat: 'الإجمالي قبل الضريبة',
        summaryVat: 'ضريبة القيمة المضافة',
        summaryOverallCost: 'التكلفة الإجمالية',
        grandTotal: 'الإجمالي النهائي',
        unitPrice: 'سعر الوحدة',
        savePrices: 'حفظ الأسعار',
        loadPrices: 'استرجاع الأسعار',
        exportPDF: 'تصدير PDF',
        pricesSaved: 'تم حفظ الأسعار بنجاح!',
        pricesLoaded: 'تم استرجاع الأسعار المحفوظة!',
        
        // Currency
        currencyLabel: 'العملة',
        currencyEGP: 'جنيه مصري (ج.م.)',
        currencyUSD: 'دولار أمريكي ($)',
        currencyEUR: 'يورو (€)',
        currencyGBP: 'جنيه إسترليني (£)',
        currencyCNY: 'يوان صيني (¥)',
        currencySAR: 'ريال سعودي (ر.س.)',
        currencyKWD: 'دينار كويتي (د.ك.)',
        currencyQAR: 'ريال قطري (ر.ق.)',
        currencyOther: 'عملة',
        pdfGenerated: 'تم إنشاء التقرير بنجاح (PDF)!',
        
        // Subtotals
        laborSubtotal: 'إجمالي تكلفة العمالة:',
        equipmentSubtotal: 'إجمالي تكلفة المعدات:',
        materialsSubtotal: 'إجمالي تكلفة المواد:',
        clearPrices: 'مسح الأسعار',
        pricesCleared: 'تم مسح الأسعار بنجاح!',
        
        // AI Planner
        experimentalWarning: 'تحت الإنشاء - تجريبي',
        
        // Landing Page
        heroTitle: 'خطّط مشروعك باحترافية',
        heroSubtitle: 'احسب احتياجات فريق العمل • المدة الزمنية • التكلفة التفصيلية للعناصر الإنشائية باستخدام نظام CSI العالمي',
        startNow: 'ابدأ الآن',
        knowMore: 'اعرف المزيد',
        whyUseUs: 'لماذا تستخدم CSI Calculator؟',
        benefitPlanningTitle: 'تخطيط احترافي',
        benefitPlanningDesc: 'احصل على تركيبة فريق العمل المثالية ومعدلات الإنتاج لكل عنصر إنشائي',
        benefitCostingTitle: 'تسعير دقيق',
        benefitCostingDesc: 'احسب التكلفة التفصيلية للعمالة والمعدات بناءً على أسعارك المحلية',
        benefitTimeTitle: 'توفير الوقت',
        benefitTimeDesc: 'احصل على نتائج فورية بدلاً من ساعات البحث في المراجع والجداول',
        howItWorks: 'كيف يعمل؟',
        step1Title: 'اختر القسم الرئيسي',
        step1Desc: '16 قسم رئيسي للعناصر الإنشائية',
        step2Title: 'حدد القسم الفرعي',
        step2Desc: 'تصنيفات تفصيلية لكل قسم',
        step3Title: 'اختر العنصر',
        step3Desc: 'وصف دقيق للعنصر المطلوب',
        step4Title: 'أدخل الكمية',
        step4Desc: 'واحصل على النتائج فوراً',
        exampleTitle: 'مثال عملي: أساسات اللبشة',
        walkthroughHeader: 'رحلة حساب تكلفة أساسات خرسانية',
        walkthroughSubheader: 'شاهد كيف يمكنك الوصول للنتائج في ثوانٍ',
        mainDivisionLabel: 'القسم الرئيسي',
        subDiv1Label: 'القسم الفرعي الأول',
        subDiv2Label: 'القسم الفرعي الثاني',
        itemLabel: 'وصف العنصر',
        tryNow: 'جرّب بنفسك الآن',
        ctaTitle: 'جاهز للبدء؟',
        ctaSubtitle: 'ابدأ بحساب احتياجات مشروعك الآن مجاناً',
        startCalculating: 'ابدأ الحساب'
    },
    en: {
        // Navbar
        home: 'Home',
        crewCalculator: 'Crew Calculator',
        aiPlanner: 'AI Chat Wizard',
        evmCalculator: 'EVM Calculator',
        blog: 'Manual+Knowledge Bites',
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
        // Updated translation as requested
        calculateBtn: 'Calculate Crew Requirements & Activity Duration',

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
        
        // Quick Search
        quickSearchPlaceholder: 'Write Item Description',
        orSelectFromSections: 'Or Select from Sections',
        
        // Cost Calculator
        calculateDetailedCost: 'Calculate Detailed Cost',
        costCalculatorTitle: '💰 Cost Calculator',
        enterMarketPrices: 'Enter actual local market prices',
        laborCostTitle: '👷 Labor Cost',
        laborCostNote: 'Enter daily rate for each worker type',
        equipmentCostTitle: '🚜 Equipment Cost',
        equipmentCostNote: 'Enter hourly rate for each equipment',
        materialsTitle: '📦 Add Raw Materials Cost (Optional)',
        materialsNote: 'Enter total materials cost for the required quantity',
        materialsInputLabel: 'Total Materials Cost',
        modifiersTitle: '📊 Profit Margin & Taxes',
        profitMarginLabel: 'Profit Margin (%)',
        vatRateLabel: 'VAT Rate (%)',
        costSummaryTitle: '🧾 Estimated Cost Summary',
        summaryLabor: 'Labor Cost',
        summaryEquipment: 'Equipment Cost',
        summaryMaterials: 'Materials Cost',
        summaryBaseCost: 'Base Cost',
        summaryProfit: 'Profit Margin',
        summaryBeforeVat: 'Total Before Tax',
        summaryVat: 'VAT',
        summaryOverallCost: 'Overall Cost',
        grandTotal: 'Grand Total',
        unitPrice: 'Unit Price',
        savePrices: 'Save Prices',
        loadPrices: 'Load Prices',
        exportPDF: 'Export PDF',
        pricesSaved: 'Prices saved successfully!',
        pricesLoaded: 'Saved prices loaded successfully!',

        // Currency
        currencyLabel: 'Currency',
        currencyEGP: 'Egyptian Pound (EGP)',
        currencyUSD: 'US Dollar ($)',
        currencyEUR: 'Euro (€)',
        currencyGBP: 'British Pound (£)',
        currencyCNY: 'Chinese Yuan (¥)',
        currencySAR: 'Saudi Riyal (SAR)',
        currencyKWD: 'Kuwaiti Dinar (KWD)',
        currencyQAR: 'Qatari Riyal (QAR)',
        currencyOther: 'Currency',
        pdfGenerated: 'Report generated successfully (PDF)!',
        
        // Subtotals
        laborSubtotal: 'Labor Total Cost:',
        equipmentSubtotal: 'Equipment Total Cost:',
        materialsSubtotal: 'Materials Total Cost:',
        clearPrices: 'Clear Prices',
        pricesCleared: 'Prices cleared successfully!',

        // AI Planner
        experimentalWarning: 'Under Construction - Experimental',
        
        // Landing Page
        heroTitle: 'Plan Your Project Professionally',
        heroSubtitle: 'Calculate crew requirements • Duration • Detailed costs for construction elements using the international CSI system',
        startNow: 'Start Now',
        knowMore: 'Know More',
        whyUseUs: 'Why Use CSI Calculator?',
        benefitPlanningTitle: 'Professional Planning',
        benefitPlanningDesc: 'Get the ideal crew composition and production rates for each construction element',
        benefitCostingTitle: 'Accurate Costing',
        benefitCostingDesc: 'Calculate detailed labor and equipment costs based on your local prices',
        benefitTimeTitle: 'Save Time',
        benefitTimeDesc: 'Get instant results instead of hours searching through references and tables',
        howItWorks: 'How It Works?',
        step1Title: 'Select Main Division',
        step1Desc: '16 main construction divisions',
        step2Title: 'Choose Sub-Division',
        step2Desc: 'Detailed classifications for each',
        step3Title: 'Pick the Item',
        step3Desc: 'Precise item description',
        step4Title: 'Enter Quantity',
        step4Desc: 'And get instant results',
        exampleTitle: 'Practical Example: Raft Foundation',
        walkthroughHeader: 'Journey to Calculate Foundation Costs',
        walkthroughSubheader: 'See how you can get results in seconds',
        mainDivisionLabel: 'Main Division',
        subDiv1Label: 'Sub-Division 1',
        subDiv2Label: 'Sub-Division 2',
        itemLabel: 'Item Description',
        tryNow: 'Try It Yourself Now',
        ctaTitle: 'Ready to Start?',
        ctaSubtitle: 'Start calculating your project needs now for free',
        startCalculating: 'Start Calculating'
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
