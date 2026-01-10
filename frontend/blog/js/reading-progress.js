// شريط تقدم القراءة - Reading Progress Bar

(function() {
    'use strict';
    
    /**
     * إنشاء شريط التقدم
     */
    function createProgressBar() {
        // إنشاء HTML للشريط
        const progressHTML = `
            <div class="progress-container">
                <div class="progress-bar" id="readingProgressBar"></div>
            </div>
            <div class="reading-time-indicator" id="readingTimeIndicator">
                <span class="icon">📖</span>
                <span class="text"></span>
                <span class="percentage">0%</span>
            </div>
        `;
        
        document.body.insertAdjacentHTML('afterbegin', progressHTML);
    }
    
    /**
     * تحديث شريط التقدم
     */
    function updateProgress() {
        const progressBar = document.getElementById('readingProgressBar');
        const indicator = document.getElementById('readingTimeIndicator');
        
        if (!progressBar) return;
        
        // حساب نسبة التقدم
        const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        
        // تحديث عرض الشريط
        progressBar.style.width = scrolled + '%';
        
        // إضافة class complete عند الوصول للنهاية
        if (scrolled >= 99) {
            progressBar.classList.add('complete');
        } else {
            progressBar.classList.remove('complete');
        }
        
        // تحديث مؤشر الوقت
        if (indicator) {
            updateTimeIndicator(indicator, scrolled);
        }
    }
    
    /**
     * تحديث مؤشر وقت القراءة
     */
    function updateTimeIndicator(indicator, scrolled) {
        const percentage = Math.round(scrolled);
        const isRTL = document.documentElement.dir === 'rtl';
        
        // إظهار المؤشر عند البدء بالقراءة
        if (scrolled > 5) {
            indicator.classList.add('visible');
        } else {
            indicator.classList.remove('visible');
        }
        
        // تحديث النص
        const text = indicator.querySelector('.text');
        const percentageSpan = indicator.querySelector('.percentage');
        
        if (percentage >= 100) {
            text.textContent = isRTL ? 'تم الانتهاء!' : 'Completed!';
            percentageSpan.textContent = '✓';
        } else {
            text.textContent = isRTL ? 'تقدم القراءة:' : 'Reading:';
            percentageSpan.textContent = percentage + '%';
        }
    }
    
    /**
     * حساب وقت القراءة المقدر
     */
    function calculateReadingTime() {
        const article = document.querySelector('.article-body');
        if (!article) return 0;
        
        const text = article.textContent;
        const wordsPerMinute = 200; // معدل القراءة العادي
        const wordCount = text.trim().split(/\s+/).length;
        const readingTime = Math.ceil(wordCount / wordsPerMinute);
        
        return readingTime;
    }
    
    /**
     * تحديث وقت القراءة في الصفحة
     */
    function updateReadingTimeDisplay() {
        const readingTimeElement = document.querySelector('.article-read-time');
        if (!readingTimeElement) return;
        
        const minutes = calculateReadingTime();
        const isRTL = document.documentElement.dir === 'rtl';
        
        if (isRTL) {
            readingTimeElement.textContent = `${minutes} دقيقة`;
        } else {
            readingTimeElement.textContent = `${minutes} min read`;
        }
    }
    
    // التهيئة عند تحميل الصفحة
    function init() {
        createProgressBar();
        updateReadingTimeDisplay();
        updateProgress();
        
        // تحديث عند السكرول
        let ticking = false;
        window.addEventListener('scroll', function() {
            if (!ticking) {
                window.requestAnimationFrame(function() {
                    updateProgress();
                    ticking = false;
                });
                ticking = true;
            }
        });
        
        // تحديث عند تغيير حجم النافذة
        window.addEventListener('resize', updateProgress);
    }
    
    // تشغيل عند تحميل الصفحة
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
