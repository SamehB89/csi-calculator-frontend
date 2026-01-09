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
    
    // Initialize all manual ad units on the page
    initializeManualAdUnits();
}

// Initialize all adsbygoogle elements on the page
function initializeManualAdUnits() {
    // Find all uninitialized ad units
    const adUnits = document.querySelectorAll('.adsbygoogle:not([data-adsbygoogle-status])');
    
    if (adUnits.length === 0) {
        console.log('📢 No manual ad units to initialize');
        return;
    }
    
    console.log(`📢 Initializing ${adUnits.length} manual ad unit(s)...`);
    
    // Push each ad unit to AdSense
    adUnits.forEach((adUnit, index) => {
        try {
            (adsbygoogle = window.adsbygoogle || []).push({});
            console.log(`✅ Ad unit ${index + 1} pushed to AdSense queue`);
        } catch (error) {
            console.warn(`⚠️ Error initializing ad unit ${index + 1}:`, error);
        }
    });
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

// Insert a responsive ad unit into a container
function insertResponsiveAd(containerId, slotId, format = 'auto') {
    const container = document.getElementById(containerId);
    if (!container) {
        console.warn(`Ad container "${containerId}" not found`);
        return;
    }
    
    // Ensure container has proper styling
    container.classList.add('ad-container');
    
    // Create the ad unit with responsive settings
    container.innerHTML = `
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-5429423113977975"
             data-ad-slot="${slotId}"
             data-ad-format="${format}"
             data-full-width-responsive="true"></ins>
    `;
    
    // Push to AdSense queue
    try {
        (adsbygoogle = window.adsbygoogle || []).push({});
        console.log(`✅ Responsive ad inserted in container: ${containerId}`);
    } catch (error) {
        console.warn(`⚠️ Error inserting ad in ${containerId}:`, error);
    }
}

// Insert a vertical sidebar ad
function insertSidebarAd(containerId, slotId) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.warn(`Sidebar ad container "${containerId}" not found`);
        return;
    }
    
    container.innerHTML = `
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-5429423113977975"
             data-ad-slot="${slotId}"
             data-ad-format="vertical"
             data-full-width-responsive="false"></ins>
    `;
    
    try {
        (adsbygoogle = window.adsbygoogle || []).push({});
        console.log(`✅ Sidebar ad inserted in container: ${containerId}`);
    } catch (error) {
        console.warn(`⚠️ Error inserting sidebar ad in ${containerId}:`, error);
    }
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
    initializeAdUnits: initializeManualAdUnits,
    insertResponsiveAd: insertResponsiveAd,
    insertSidebarAd: insertSidebarAd,
    configureExclusions: configureAdExclusions
};

