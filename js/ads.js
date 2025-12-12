// ========================================
// Google AdSense Integration
// Auto ads are enabled in AdSense dashboard
// Publisher ID: ca-pub-5429423113977975
// ========================================

// Initialize AdSense (Auto ads handle everything automatically)
function initAdsense() {
    console.log('✅ AdSense Auto ads initialized');
    console.log('Publisher ID: ca-pub-5429423113977975');
    
    // Auto ads script is already loaded in HTML <head>
    // No manual intervention needed - Google handles ad placement
}

// Optional: Manual ad insertion for specific placements
function insertManualAd(containerId, slotId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
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
    */
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initAdsense();
    
    // Auto ads will place ads automatically
    // No need to manually insert ads when Auto ads is ON
    console.log('🎯 Waiting for Auto ads to load...');
});

// Export for external use
window.CSI_Ads = {
    init: initAdsense,
    insertManualAd: insertManualAd
};
