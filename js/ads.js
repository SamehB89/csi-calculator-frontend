// ========================================
// Google AdSense Integration
// Replace YOUR_PUBLISHER_ID and SLOT_IDs after approval
// ========================================

// Initialize AdSense
function initAdsense() {
    // This will be populated after AdSense approval
    console.log('AdSense: Ready for integration');
}

// Insert responsive ad
function insertAd(containerId, slotId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    // Placeholder until AdSense approval
    container.innerHTML = `
        <div class="ad-placeholder" style="
            background: linear-gradient(135deg, #667eea22, #764ba222);
            border: 2px dashed var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
        ">
            <p>📢 Ad Space</p>
            <small>Support us by allowing ads</small>
        </div>
    `;
    
    // After AdSense approval, replace with:
    /*
    container.innerHTML = `
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-YOUR_PUBLISHER_ID"
             data-ad-slot="${slotId}"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
    `;
    (adsbygoogle = window.adsbygoogle || []).push({});
    */
}

// Insert in-article ad
function insertInArticleAd(containerId) {
    insertAd(containerId, 'IN_ARTICLE_SLOT_ID');
}

// Insert sidebar ad
function insertSidebarAd(containerId) {
    insertAd(containerId, 'SIDEBAR_SLOT_ID');
}

// Auto-insert ads when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Find all ad containers and populate
    document.querySelectorAll('[data-ad-slot]').forEach(container => {
        const slotType = container.getAttribute('data-ad-slot');
        insertAd(container.id, slotType);
    });
});

// Export for external use
window.CSI_Ads = {
    init: initAdsense,
    insertAd: insertAd,
    insertInArticleAd: insertInArticleAd,
    insertSidebarAd: insertSidebarAd
};
