/**
 * Quick Search Manager
 * Handles instant item search functionality
 */

class QuickSearchManager {
    constructor(apiBase) {
        this.API_BASE = apiBase;
        this.searchInput = null;
        this.searchResults = null;
        this.clearBtn = null;
        this.allItems = [];
        this.debounceTimer = null;
        this.currentHighlightIndex = -1;
        
        this.init();
    }
    
    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }
    
    setup() {
        // Get DOM elements
        this.searchInput = document.getElementById('quickSearchInput');
        this.searchResults = document.getElementById('searchResults');
        this.clearBtn = document.getElementById('clearSearch');
        
        if (!this.searchInput || !this.searchResults) {
            console.warn('Quick search elements not found in DOM');
            return;
        }
        
        // Load search index
        this.loadSearchIndex();
        
        // Attach event listeners
        this.attachEventListeners();
    }
    
    attachEventListeners() {
        // Search input
        this.searchInput.addEventListener('input', (e) => {
            this.handleSearch(e.target.value);
        });
        
        // Keyboard navigation
        this.searchInput.addEventListener('keydown', (e) => {
            this.handleKeyboard(e);
        });
        
        // Clear button
        this.clearBtn.addEventListener('click', () => {
            this.clearSearch();
        });
        
        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-box-wrapper')) {
                this.hideResults();
            }
        });
    }
    
    async loadSearchIndex() {
        // No need to preload - we'll search on-demand using /api/items
        console.log('🔍 Quick Search ready (using server-side search)');
        this.searchReady = true;
    }
    
    handleSearch(query) {
        clearTimeout(this.debounceTimer);
        
        if (query.length < 2) {
            this.hideResults();
            this.clearBtn.style.display = 'none';
            return;
        }
        
        this.clearBtn.style.display = 'block';
        
        // Show loading state
        this.showLoading();
        
        // Debounce search (300ms after typing stops)
        this.debounceTimer = setTimeout(() => {
            this.performSearch(query);
        }, 300);
    }
    
    async performSearch(query) {
        try {
            // Use existing /api/items endpoint with query parameter
            const response = await fetch(`${this.API_BASE}/items?q=${encodeURIComponent(query)}&limit=15`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            const items = data.items || [];
            
            // Transform items to search result format
            const results = items.map(item => ({
                code: item.full_code,
                name_ar: item.description,
                name_en: '',
                division: item.main_div_name || '',
                subdivision1: item.sub_div1_name || '',
                subdivision2: item.sub_div2_name || '',
                unit: item.unit || ''
            }));
            
            // Store for item selection
            this.allItems = results;
            
            this.displayResults(results, query);
            
        } catch (error) {
            console.error('❌ Search failed:', error);
            this.searchResults.innerHTML = `
                <div class="no-results">
                    <p>❌ حدث خطأ في البحث</p>
                    <p>جرب مرة أخرى أو استخدم القوائم أدناه</p>
                </div>
            `;
            this.showResults();
        }
    }
    
    normalizeArabic(text) {
        // Normalize Arabic text (remove diacritics, normalize alef)
        return text
            .replace(/[ًٌٍَُِّْٰ]/g, '') // Remove tashkeel
            .replace(/[أإآ]/g, 'ا') // Normalize alef
            .replace(/ة/g, 'ه') // Normalize taa marbuta
            .replace(/ى/g, 'ي'); // Normalize alef maksura
    }
    
    showLoading() {
        this.searchResults.innerHTML = `
            <div class="search-loading">
                <div class="search-loading-spinner"></div>
                <span>جاري البحث...</span>
            </div>
        `;
        this.showResults();
    }
    
    displayResults(results, query) {
        this.currentHighlightIndex = -1;
        
        if (results.length === 0) {
            this.searchResults.innerHTML = `
                <div class="no-results">
                    <p>❌ لم يتم العثور على نتائج لـ "${this.escapeHtml(query)}"</p>
                    <p>جرب البحث بكلمات أخرى أو استخدم القوائم أدناه</p>
                </div>
            `;
        } else {
            this.searchResults.innerHTML = results.map((item, index) => this.renderResultItem(item, index)).join('');
            
            // Add click handlers
            this.attachResultClickHandlers();
        }
        
        this.showResults();
    }
    
    renderResultItem(item, index) {
        // Build breadcrumb path
        const pathParts = [];
        if (item.division) pathParts.push(item.division);
        if (item.subdivision1) pathParts.push(item.subdivision1);
        if (item.subdivision2) pathParts.push(item.subdivision2);
        
        const pathHtml = pathParts.length > 0 
            ? `<div class="result-path">
                ${pathParts.map((part, i) => `
                    <span class="result-path-item">
                        ${this.truncate(part, 40)}
                        ${i < pathParts.length - 1 ? '<span class="result-path-sep">→</span>' : ''}
                    </span>
                `).join('')}
            </div>`
            : '';
        
        return `
            <div class="search-result-item" data-code="${this.escapeHtml(item.code)}" data-index="${index}" tabindex="0">
                <div class="result-title">${this.escapeHtml(item.name_ar || item.name_en)}</div>
                ${pathHtml}
            </div>
        `;
    }
    
    attachResultClickHandlers() {
        const items = this.searchResults.querySelectorAll('.search-result-item');
        items.forEach(el => {
            el.addEventListener('click', () => {
                this.selectItem(el.dataset.code);
            });
            
            el.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    this.selectItem(el.dataset.code);
                }
            });
        });
    }
    
    async selectItem(code) {
        console.log(`🔍 Selected item: ${code}`);
        
        // Hide search results
        this.hideResults();
        this.clearSearch();
        
        // Find the item in our index
        const item = this.allItems.find(i => i.code === code);
        if (!item) {
            console.error('Item not found:', code);
            return;
        }
        
        // Populate dropdowns sequentially
        await this.populateDropdownsFromItem(item);
        
        // Scroll to item details
        setTimeout(() => {
            const itemDetails = document.getElementById('itemDetailsSection');
            if (itemDetails) {
                itemDetails.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }, 500);
    }
    
    async populateDropdownsFromItem(item) {
        const mainDiv = document.getElementById('mainDivision');
        const subDiv1 = document.getElementById('subDivision1');
        const subDiv2 = document.getElementById('subDivision2');
        const itemDesc = document.getElementById('itemDescription');
        
        // Set main division
        if (item.division && mainDiv) {
            // Find matching option by text content
            const option = Array.from(mainDiv.options).find(opt => 
                opt.textContent.includes(item.division)
            );
            if (option) {
                mainDiv.value = option.value;
                mainDiv.dispatchEvent(new Event('change'));
                
                // Wait for sub1 to load
                await this.waitFor(200);
            }
        }
        
        // Set subdivision 1
        if (item.subdivision1 && subDiv1) {
            await this.waitFor(100);
            const option = Array.from(subDiv1.options).find(opt => 
                opt.textContent.includes(item.subdivision1)
            );
            if (option) {
                subDiv1.value = option.value;
                subDiv1.dispatchEvent(new Event('change'));
                
                // Wait for sub2 to load
                await this.waitFor(200);
            }
        }
        
        // Set subdivision 2
        if (item.subdivision2 && subDiv2) {
            await this.waitFor(100);
            const option = Array.from(subDiv2.options).find(opt => 
                opt.textContent.includes(item.subdivision2)
            );
            if (option) {
                subDiv2.value = option.value;
                subDiv2.dispatchEvent(new Event('change'));
                
                // Wait for items to load
                await this.waitFor(200);
            }
        }
        
        // Set final item
        if (item.code && itemDesc) {
            await this.waitFor(100);
            itemDesc.value = item.code;
            itemDesc.dispatchEvent(new Event('change'));
        }
    }
    
    waitFor(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    handleKeyboard(e) {
        const items = this.searchResults.querySelectorAll('.search-result-item');
        
        if (items.length === 0) return;
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.currentHighlightIndex = Math.min(this.currentHighlightIndex + 1, items.length - 1);
                this.updateHighlight(items);
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                this.currentHighlightIndex = Math.max(this.currentHighlightIndex - 1, -1);
                this.updateHighlight(items);
                break;
                
            case 'Enter':
                e.preventDefault();
                if (this.currentHighlightIndex >= 0) {
                    const code = items[this.currentHighlightIndex].dataset.code;
                    this.selectItem(code);
                }
                break;
                
            case 'Escape':
                e.preventDefault();
                this.hideResults();
                break;
        }
    }
    
    updateHighlight(items) {
        items.forEach((item, index) => {
            if (index === this.currentHighlightIndex) {
                item.classList.add('result-highlighted');
                item.scrollIntoView({ block: 'nearest' });
            } else {
                item.classList.remove('result-highlighted');
            }
        });
    }
    
    clearSearch() {
        this.searchInput.value = '';
        this.hideResults();
        this.clearBtn.style.display = 'none';
        this.currentHighlightIndex = -1;
    }
    
    showResults() {
        this.searchResults.style.display = 'block';
    }
    
    hideResults() {
        this.searchResults.style.display = 'none';
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text || '';
        return div.innerHTML;
    }
    
    truncate(text, maxLength) {
        if (!text || text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
}

// Initialize when script loads
let quickSearchManager = null;

// Check if we're on the crew calculator page
if (window.location.pathname.includes('crew-calculator')) {
    // Wait for API_BASE to be defined
    const initQuickSearch = () => {
        if (typeof API_BASE !== 'undefined') {
            quickSearchManager = new QuickSearchManager(API_BASE);
            console.log('🔍 Quick Search initialized');
        } else {
            // Retry after a short delay
            setTimeout(initQuickSearch, 100);
        }
    };
    
    initQuickSearch();
}
