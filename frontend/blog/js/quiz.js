// الاختبارات التفاعلية - Interactive Quiz System

(function() {
    'use strict';
    
    /**
     * Quiz Class
     */
    class Quiz {
        constructor(quizElement) {
            this.quizElement = quizElement;
            this.questions = [];
            this.userAnswers = [];
            this.score = 0;
            
            this.init();
        }
        
        init() {
            this.parseQuestions();
            this.setupEventListeners();
        }
        
        /**
         * قراءة الأسئلة من HTML
         */
        parseQuestions() {
            const questionElements = this.quizElement.querySelectorAll('.quiz-question');
            
            questionElements.forEach((questionEl, index) => {
                const questionText = questionEl.querySelector('p').textContent;
                const options = [];
                const inputs = questionEl.querySelectorAll('input[type="radio"]');
                
                inputs.forEach(input => {
                    const label = input.parentElement;
                    options.push({
                        value: input.value,
                        text: label.textContent.trim(),
                        element: label
                    });
                });
                
                this.questions.push({
                    index: index,
                    text: questionText,
                    options: options,
                    correctAnswer: questionEl.dataset.correct
                });
            });
        }
        
        /**
         * إعداد Event Listeners
         */
        setupEventListeners() {
            const checkButton = this.quizElement.querySelector('.quiz-btn');
            if (checkButton) {
                checkButton.addEventListener('click', () => this.checkAnswers());
            }
        }
        
        /**
         * التحقق من الإجابات
         */
        checkAnswers() {
            this.score = 0;
            this.userAnswers = [];
            
            this.questions.forEach((question, index) => {
                const selectedOption = this.quizElement.querySelector(
                    `input[name="q${index + 1}"]:checked`
                );
                
                if (selectedOption) {
                    const selectedValue = selectedOption.value;
                    this.userAnswers.push(selectedValue);
                    
                    // تمييز الإجابة
                    question.options.forEach(option => {
                        option.element.classList.remove('correct', 'incorrect');
                        
                        if (option.value === question.correctAnswer) {
                            option.element.classList.add('correct');
                            if (selectedValue === question.correctAnswer) {
                                this.score++;
                            }
                        } else if (option.value === selectedValue) {
                            option.element.classList.add('incorrect');
                        }
                    });
                }
            });
            
            this.displayResults();
        }
        
        /**
         * عرض النتائج
         */
        displayResults() {
            const resultDiv = this.quizElement.querySelector('.quiz-result');
            if (!resultDiv) return;
            
            const percentage = Math.round((this.score / this.questions.length) * 100);
            const isRTL = document.documentElement.dir === 'rtl';
            
            let message = '';
            let className = '';
            
            if (percentage >= 80) {
                message = isRTL ? 
                    '🎉 ممتاز! لديك فهم ممتاز للموضوع!' : 
                    '🎉 Excellent! You have great understanding!';
                className = 'success';
            } else if (percentage >= 60) {
                message = isRTL ? 
                    '👍 جيد! يمكنك المراجعة لتحسين النتيجة.' : 
                    '👍 Good! You can review to improve.';
                className = 'success';
            } else {
                message = isRTL ? 
                    '📖 يُنصح بقراءة المقال مرة أخرى بتمعن.' : 
                    '📖 We recommend re-reading the article carefully.';
                className = 'failure';
            }
            
            const scoreText = isRTL ? 
                `النتيجة: ${this.score} من ${this.questions.length}` :
                `Score: ${this.score} out of ${this.questions.length}`;
            
            resultDiv.innerHTML = `
                <div class="quiz-score">${percentage}%</div>
                <p><strong>${scoreText}</strong></p>
                <p>${message}</p>
            `;
            
            resultDiv.className = `quiz-result ${className} visible`;
        }
    }
    
    /**
     * تهيئة جميع الاختبارات في الصفحة
     */
    function initQuizzes() {
        const quizElements = document.querySelectorAll('.article-quiz');
        quizElements.forEach(quizElement => {
            new Quiz(quizElement);
        });
    }
    
    /**
     * إنشاء Checklist تفاعلي
     */
    function initChecklists() {
        const checklists = document.querySelectorAll('.printable-checklist');
        
        checklists.forEach(checklist => {
            checklist.querySelectorAll('input[type="checkbox"]').forEach((checkbox, index) => {
                checkbox.id = `check-${Date.now()}-${index}`;
                
                const label = checkbox.nextElementSibling;
                if (label && label.tagName === 'LABEL') {
                    label.setAttribute('for', checkbox.id);
                }
                
                // حفظ الحالة في localStorage
                const storageKey = `checklist-${window.location.pathname}-${index}`;
                const savedState = localStorage.getItem(storageKey);
                
                if (savedState === 'true') {
                    checkbox.checked = true;
                }
                
                checkbox.addEventListener('change', function() {
                    localStorage.setItem(storageKey, this.checked);
                });
            });
            
            // زر الطباعة
            const printBtn = checklist.querySelector('.print-btn');
            if (printBtn) {
                printBtn.addEventListener('click', function() {
                    window.print();
                });
            }
        });
    }
    
    // التهيئة عند تحميل الصفحة
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initQuizzes();
            initChecklists();
        });
    } else {
        initQuizzes();
        initChecklists();
    }
})();
