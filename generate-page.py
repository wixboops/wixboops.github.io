import json
import hashlib

with open("extracted-data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced URL Validator with Cache</title>
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
        .cached-error {
            opacity: 0.6;
            background: repeating-linear-gradient(
                45deg,
                rgba(239,68,68,0.1),
                rgba(239,68,68,0.1) 10px,
                rgba(0,0,0,0) 10px,
                rgba(0,0,0,0) 20px
            );
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-100">
    <div class="container mx-auto p-4">
        <h1 class="text-3xl font-bold mb-8 text-center text-purple-400">URL Validation System with Cache</h1>
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
                            <span class="font-mono text-sm">{item}</span>
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
    const CACHE_VERSION = 1;
    const CACHE_PREFIX = 'urlValidator::';
    const CACHE_TTL = 3600000; // 1 hour

    function getCacheKey(url) {
        return CACHE_PREFIX + url;
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
                        status: true, // Assume CORS error means valid
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

    async function processUrls() {
        const items = document.querySelectorAll('.url-item');
        
        // First pass: Apply cached results
        items.forEach(item => {
            const hash = item.dataset.hash;
            const cacheKey = getCacheKey(hash);
            const cached = localStorage.getItem(cacheKey);
            const dot = item.querySelector('.status-dot');

            if (cached) {
                const { status } = JSON.parse(cached);
                dot.style.backgroundColor = status ? '#10b981' : '#ef4444';
                if (!status) {
                    item.classList.add('cached-error');
                }
            }
        });

        // Second pass: Validate uncached items
        for (const item of items) {
            const dot = item.querySelector('.status-dot');
            const url = item.dataset.url;
            const hash = item.dataset.hash;
            
            if (!localStorage.getItem(getCacheKey(hash))) {
                dot.style.backgroundColor = '#f59e0b'; // Yellow for checking
                
                try {
                    const isValid = await validateUrl(url, hash);
                    dot.style.backgroundColor = isValid ? '#10b981' : '#ef4444';
                    
                    if (!isValid) {
                        item.classList.add('cached-error');
                    }
                } catch {
                    dot.style.backgroundColor = '#ef4444';
                }
                
                await new Promise(r => setTimeout(r, 200));
            }
        }
    }

    window.addEventListener('DOMContentLoaded', processUrls);
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)
