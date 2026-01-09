// CSI Crew Calculator - Service Worker
// Enables offline support and PWA functionality

const CACHE_NAME = 'csi-calculator-v3';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/crew-calculator.html',
    '/ai-planner.html',
    '/privacy.html',
    '/terms.html',
    '/css/theme.css',
    '/css/style.css',
    '/css/crew-calculator.css',
    '/css/landing.css',
    '/css/legal.css',
    '/js/app.js',
    '/js/i18n.js',
    '/assets/csi_logo_v2.png',
    '/assets/engineer_character.png',
    '/assets/csi_hierarchy.png',
    '/assets/benefits_icons.png',
    '/manifest.json'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
    console.log('[SW] Installing service worker...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[SW] Caching static assets');
                return cache.addAll(STATIC_ASSETS);
            })
            .catch((err) => {
                console.log('[SW] Cache error:', err);
            })
    );
    self.skipWaiting();
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating service worker...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        console.log('[SW] Deleting old cache:', cache);
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch event - Network First Strategy (Always get latest version)
self.addEventListener('fetch', (event) => {
    // Skip API requests - always fetch from network
    if (event.request.url.includes('/api/')) {
        return;
    }
    
    event.respondWith(
        // Try network first
        fetch(event.request)
            .then((networkResponse) => {
                // Cache successful GET requests
                if (event.request.method === 'GET' && networkResponse.status === 200) {
                    const responseClone = networkResponse.clone();
                    caches.open(CACHE_NAME)
                        .then((cache) => {
                            cache.put(event.request, responseClone);
                        });
                }
                return networkResponse;
            })
            .catch(() => {
                // Network failed, fallback to cache
                return caches.match(event.request)
                    .then((cachedResponse) => {
                        if (cachedResponse) {
                            return cachedResponse;
                        }
                        // Return offline page if available
                        if (event.request.mode === 'navigate') {
                            return caches.match('/index.html');
                        }
                    });
            })
    );
});

// Handle push notifications (for future use)
self.addEventListener('push', (event) => {
    const options = {
        body: event.data ? event.data.text() : 'New update available!',
        icon: '/assets/icon-192.png',
        badge: '/assets/icon-72.png',
        vibrate: [100, 50, 100]
    };
    
    event.waitUntil(
        self.registration.showNotification('CSI Crew Calculator', options)
    );
});
