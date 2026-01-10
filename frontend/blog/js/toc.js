// توليد جدول المحتويات تلقائياً - Auto-Generate Table of Contents

(function() {
    'use strict';
    
    /**
     * إنشاء جدول المحتويات من العناوين
     */
    function generateTOC() {
        const article = document.querySelector('.article-body');
        if (!article) return;
        
        const headings = article.querySelectorAll('h2, h3');
        if (headings.length < 3) return; // لا داعي لـ TOC إذا كان هناك أقل من 3 عناوين
        
        const toc = document.createElement('div');
        toc.className = 'table-of-contents';
        toc.id = 'toc';
        
        const isRTL = document.documentElement.dir === 'rtl';
        const tocTitle = isRTL ? '📑 جدول المحتويات' : '📑 Table of Contents';
        
        let tocHTML = `<h3>${tocTitle}</h3><ul>`;
        
        headings.forEach((heading, index) => {
            const id = `section-${index}`;
            heading.id = id;
            
            const level = heading.tagName === 'H2' ? 'toc-level-1' : 'toc-level-2';
            const text = heading.textContent.trim();
            
            tocHTML += `<li class="${level}"><a href="#${id}" data-section="${index}">${text}</a></li>`;
        });
        
        tocHTML += '</ul>';
        toc.innerHTML = tocHTML;
        
        // إدراج TOC قبل أول عنصر في المقال
        const firstChild = article.firstElementChild;
        if (firstChild) {
            article.insertBefore(toc, firstChild);
        }
        
        // إضافة smooth scroll
        setupSmoothScroll(toc);
        
        // إضافة active section highlighting
        setupActiveSection(headings);
    }
    
    /**
     * Smooth scroll للروابط
     */
    function setupSmoothScroll(toc) {
        const links = toc.querySelectorAll('a');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const target = document.querySelector(targetId);
                
                if (target) {
                    const offset = 100; // المسافة من أعلى الشاشة
                    const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    /**
     * تفعيل القسم الحالي في TOC
     */
    function setupActiveSection(headings) {
        const tocLinks = document.querySelectorAll('.table-of-contents a');
        
        function updateActiveSection() {
            let current = '';
            const scrollPos = window.pageYOffset + 150;
            
            headings.forEach((heading, index) => {
                const sectionTop = heading.offsetTop;
                if (scrollPos >= sectionTop) {
                    current = index;
                }
            });
            
            tocLinks.forEach((link, index) => {
                link.classList.remove('active');
                if (index === current) {
                    link.classList.add('active');
                }
            });
        }
        
        window.addEventListener('scroll', updateActiveSection);
        updateActiveSection(); // تشغيل عند التحميل
    }
    
    // تشغيل عند تحميل الصفحة
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', generateTOC);
    } else {
        generateTOC();
    }
})();
