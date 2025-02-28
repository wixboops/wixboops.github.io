import json
import hashlib
from urllib.parse import urlparse

with open("extracted-data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Validator with Batching</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 10px;
            transition: all 0.3s ease;
        }
        iframe { display: none; }
        .cached-error a {
            opacity: 0.5;
            pointer-events: none;
            text-decoration: line-through;
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-100">
    <div class="container mx-auto p-4">
        <h1 class="text-3xl font-bold mb-8 text-center text-purple-400">Validated Proxy Links</h1>
        <button onclick="clearCache()" class="mb-4 bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded">
            Clear Cache
        </button>
        <div class="space-y-6">
"""

for title, items in data.items():
    html_content += f"""
            <div class="bg-gray-800 rounded-xl p-6 shadow-2xl">
                <h2 class="text-xl font-bold mb-4 text-blue-300">{title}</h2>
                <ul class="space-y-3">
    """
    for item in items:
        url_hash = hashlib.md5(item.encode()).hexdigest()
        html_content += f"""
                    <li class="url-item group" data-url="{item}" data-hash="{url_hash}">
                        <div class="flex items-center p-4 bg-gray-700 rounded-lg hover:bg-gray-600 transition-all">
                            <span class="status-dot bg-gray-500"></span>
                            <a href="{item}" 
                               class="font-mono text-sm hover:text-blue-400 break-all"
                               target="_blank" 
                               rel="noopener noreferrer">
                                {item}
                            </a>
                        </div>
                    </li>
        """
    html_content += """
                </ul>
            </div>
    """

html_content += """
        </div>
    </div>

    <script>
    const CACHE_VERSION = 2;  // Updated version for new validation rules
    const CACHE_PREFIX = 'urlValidator::';
    const CACHE_TTL = 3600000;
    const BATCH_SIZE = 3;
    const DELAY_BETWEEN_CHECKS = 300;

    function getCacheKey(url) {
        return CACHE_PREFIX + url;
    }

    function isBlockedDomain(url) {
        try {
            const { hostname } = new URL(url);
            return hostname.includes('vercel.app');
        } catch {
            return false;
        }
    }

    function clearCache() {
        Object.keys(localStorage).forEach(key => {
            if (key.startsWith(CACHE_PREFIX)) {
                localStorage.removeItem(key);
            }
        });
        window.location.reload();
    }

    async function validateUrl(url, hash) {
        const cacheKey = getCacheKey(hash);
        
        // Immediate block for vercel.app domains
        if (isBlockedDomain(url)) {
            localStorage.setItem(cacheKey, JSON.stringify({
                status: false,
                timestamp: Date.now()
            }));
            return false;
        }

        const cached = localStorage.getItem(cacheKey);        
        if (cached) {
            const { status, timestamp } = JSON.parse(cached);
            if (Date.now() - timestamp < CACHE_TTL) {
                return status;
            }
        }

        return new Promise((resolve) => {
            const iframe = document.createElement('iframe');
            let timeout;

            const cleanup = () => {
                clearTimeout(timeout);
                iframe.remove();
            };

            iframe.onload = () => {
                try {
                    const doc = iframe.contentDocument || iframe.contentWindow.document;
                    const errorElement = doc.getElementById('main-frame-error');
                    const isChromeError = getComputedStyle(doc.documentElement)
                        .backgroundImage.includes('linear-gradient(45deg, #f3f4f6 25%');
                    
                    const isValid = !errorElement && !isChromeError;
                    localStorage.setItem(cacheKey, JSON.stringify({
                        status: isValid,
                        timestamp: Date.now()
                    }));
                    resolve(isValid);
                } catch (error) {
                    localStorage.setItem(cacheKey, JSON.stringify({
                        status: true,
                        timestamp: Date.now()
                    }));
                    resolve(true);
                }
                cleanup();
            };

            iframe.onerror = () => {
                localStorage.setItem(cacheKey, JSON.stringify({
                    status: false,
                    timestamp: Date.now()
                }));
                resolve(false);
                cleanup();
            };

            timeout = setTimeout(() => {
                localStorage.setItem(cacheKey, JSON.stringify({
                    status: false,
                    timestamp: Date.now()
                }));
                resolve(false);
                cleanup();
            }, 4000);

            iframe.src = url;
            document.body.appendChild(iframe);
        });
    }

    async function processBatch(batch) {
        const promises = batch.map((item, index) => 
            new Promise(resolve => 
                setTimeout(async () => {
                    const dot = item.querySelector('.status-dot');
                    const link = item.querySelector('a');
                    const url = item.dataset.url;
                    const hash = item.dataset.hash;

                    if (!localStorage.getItem(getCacheKey(hash))) {
                        try {
                            const isValid = await validateUrl(url, hash);
                            dot.style.backgroundColor = isValid ? '#10b981' : '#ef4444';
                            if (!isValid) {
                                item.classList.add('cached-error');
                                link.removeAttribute('href');
                            }
                        } catch {
                            dot.style.backgroundColor = '#ef4444';
                            item.classList.add('cached-error');
                            link.removeAttribute('href');
                        }
                    }
                    resolve();
                }, index * DELAY_BETWEEN_CHECKS)
            )
        );
        await Promise.all(promises);
    }

    async function processUrls() {
        const items = Array.from(document.querySelectorAll('.url-item'));
        
        // Apply cached results first
        items.forEach(item => {
            const hash = item.dataset.hash;
            const cacheKey = getCacheKey(hash);
            const cached = localStorage.getItem(cacheKey);
            const dot = item.querySelector('.status-dot');
            const link = item.querySelector('a');

            if (cached) {
                const { status } = JSON.parse(cached);
                dot.style.backgroundColor = status ? '#10b981' : '#ef4444';
                if (!status) {
                    item.classList.add('cached-error');
                    link.removeAttribute('href');
                }
            } else if (isBlockedDomain(item.dataset.url)) {
                dot.style.backgroundColor = '#ef4444';
                item.classList.add('cached-error');
                link.removeAttribute('href');
            }
        });

        // Process in batches
        const batches = [];
        for (let i = 0; i < items.length; i += BATCH_SIZE) {
            batches.push(items.slice(i, i + BATCH_SIZE));
        }

        for (const batch of batches) {
            await processBatch(batch);
        }
    }

    window.addEventListener('DOMContentLoaded', processUrls);
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)
