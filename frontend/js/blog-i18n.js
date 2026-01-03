// Blog-specific Language Toggle with Redirection
function toggleLanguage() {
    const currentPath = window.location.pathname;
    const filename = currentPath.split('/').pop();
    let newFilename;

    if (filename.endsWith('-en.html')) {
        // Currently English, switch to Arabic
        // e.g., article-en.html -> article.html
        newFilename = filename.replace('-en.html', '.html');
        localStorage.setItem('csi_lang', 'ar');
    } else {
        // Currently Arabic, switch to English
        // e.g., article.html -> article-en.html
        newFilename = filename.replace('.html', '-en.html');
        localStorage.setItem('csi_lang', 'en');
    }

    // Determine the base path to redirect to
    // If we are at root/blog/index-en.html, we want root/blog/index.html
    // If we are at root/blog/articles/art-en.html, we want root/blog/articles/art.html
    // window.location.href handles relative paths well if we just provide the filename, 
    // BUT we need to be careful if the URL ends in a directory slash.
    
    // Safety check for directory root
    if (!filename || filename === 'blog') {
        // Assuming index page
        if (localStorage.getItem('csi_lang') === 'en') {
            window.location.href = 'index-en.html';
        } else {
            window.location.href = 'index.html';
        }
    } else {
        window.location.href = newFilename;
    }
}

// Ensure the correct language icon is displayed on load
document.addEventListener('DOMContentLoaded', () => {
    const currentLang = localStorage.getItem('csi_lang') || 'ar';
    const langIcon = document.getElementById('langIcon');
    if (langIcon) {
        langIcon.textContent = currentLang === 'ar' ? 'EN' : 'AR';
    }
    
    // Also ensure html lang attribute matches the file content, not just localStorage
    // (The static files already set layout, so this is just a fallback for the button text)
});
