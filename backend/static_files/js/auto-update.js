// Auto-Update Service Worker
// This file ensures users always get the latest version automatically

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
                console.log('[Auto-Update] Service Worker registered');
                
                // Check for updates every 60 seconds
                setInterval(() => {
                    registration.update();
                }, 60000);
                
                // Auto-reload when new version is available
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    if (newWorker) {
                        newWorker.addEventListener('statechange', () => {
                            if (newWorker.state === 'activated') {
                                // If there's a controller (not first install), reload
                                if (navigator.serviceWorker.controller) {
                                    console.log('[Auto-Update] New version detected! Reloading...');
                                    // Small delay to ensure SW is ready
                                    setTimeout(() => {
                                        window.location.reload();
                                    }, 1000);
                                }
                            }
                        });
                    }
                });
                
                // Also listen for controller change (when SW takes control)
                navigator.serviceWorker.addEventListener('controllerchange', () => {
                    console.log('[Auto-Update] Controller changed, reloading page...');
                    window.location.reload();
                });
            })
            .catch((err) => {
                console.error('[Auto-Update] SW registration failed:', err);
            });
    });
}
