// ========================================
// Google AdSense Integration
// COMPLIANT WITH ADSENSE POLICIES
// Publisher ID: ca-pub-5429423113977975
// ========================================

// Configure AdSense with exclusion zones
function initAdsense() {
    console.log('✅ AdSense Auto ads initialized with policy compliance');
    console.log('Publisher ID: ca-pub-5429423113977975');
    
    // Auto ads script is already loaded in HTML <head>
    // Configure exclusion zones to prevent ads near navigation
    configureAdExclusions();
}

// Configure ad exclusion zones to comply with navigation policy
function configureAdExclusions() {
    // Mark navigation and interactive elements as exclusion zones
    const exclusionSelectors = [
        '.navbar',
        '.nav-links',
        'header',
        '.hero-buttons',
        '.cta-button',
        '.walkthrough-cta',
        '.btn',
        'button'
    ];
    
    exclusionSelectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            // Mark elements to avoid ad placement
            element.setAttribute('data-ad-exclude', 'true');
            element.style.setProperty('--ad-exclude', 'true');
        });
    });
    
    console.log('🚫 Ad exclusion zones configured for navigation elements');
}

// Optional: Manual ad insertion for specific placements
// Only use when explicitly placing ads with proper labeling
function insertManualAd(containerId, slotId) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.warn(`Ad container "${containerId}" not found`);
        return;
    }
    
    // Ensure container has proper styling
    container.classList.add('ad-container');
    
    // For future manual ad units, uncomment and add slot ID:
    /*
    container.innerHTML = `
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-5429423113977975"
             data-ad-slot="${slotId}"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
    `;
    (adsbygoogle = window.adsbygoogle || []).push({});
    console.log(`✅ Manual ad inserted in container: ${containerId}`);
    */
}

// Monitor Auto Ads placement and ensure compliance
function monitorAdPlacement() {
    // Check for ads that might be too close to navigation
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.classList && node.classList.contains('adsbygoogle')) {
                    validateAdPosition(node);
                }
            });
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Validate that ads are not placed near navigation
function validateAdPosition(adElement) {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    const navbarRect = navbar.getBoundingClientRect();
    const adRect = adElement.getBoundingClientRect();
    
    // Minimum required distance (20px)
    const MIN_DISTANCE = 20;
    
    const distance = adRect.top - (navbarRect.top + navbarRect.height);
    
    if (distance < MIN_DISTANCE && distance >= 0) {
        console.warn('⚠️ Ad too close to navigation, adjusting...');
        adElement.style.marginTop = `${MIN_DISTANCE - distance + 10}px`;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initAdsense();
    
    // Monitor ad placements after a short delay (let Auto Ads initialize)
    setTimeout(() => {
        monitorAdPlacement();
        console.log('🎯 Ad placement monitoring active');
    }, 2000);
});

// Export for external use
window.CSI_Ads = {
    init: initAdsense,
    insertManualAd: insertManualAd,
    configureExclusions: configureAdExclusions
};

