import json
import hashlib
from urllib.parse import urlparse

# Add domains to this list that should always be blocked
BLOCKED_DOMAINS = [
    "vercel.app",
    "dock1.com",
    "585.eu",
    "cissp.or.id"
]

with open("extracted-data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Link Validator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .status-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 10px;
            transition: all 0.3s ease;
        }}
        iframe {{ display: none; }}
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

html_content += f"""
        </div>
    </div>

    <script>
    const BLOCKED_DOMAINS = {json.dumps(BLOCKED_DOMAINS)};
    const CACHE_VERSION = 3;
    const CACHE_PREFIX = 'urlValidator::';
    const CACHE_TTL = 3600000;
    const BATCH_SIZE = 3;
    const DELAY_BETWEEN_CHECKS = 300;

    function getCacheKey(url) {{
        return CACHE_PREFIX + url;
    }}

    function isBlockedDomain(url) {{
        try {{
            const hostname = new URL(url).hostname;
            return BLOCKED_DOMAINS.some(domain => hostname.includes(domain));
        }} catch {{
            return false;
        }}
    }}

    function clearCache() {{
        Object.keys(localStorage).forEach(key => {{
            if (key.startsWith(CACHE_PREFIX)) {{
                localStorage.removeItem(key);
            }}
        }});
        window.location.reload();
    }}

    async function validateUrl(url, hash) {{
        const cacheKey = getCacheKey(hash);
        
        if (isBlockedDomain(url)) {{
            localStorage.setItem(cacheKey, JSON.stringify({{
                status: false,
                timestamp: Date.now()
            }}));
            return false;
        }}

        const cached = localStorage.getItem(cacheKey);        
        if (cached) {{
            const {{ status, timestamp }} = JSON.parse(cached);
            if (Date.now() - timestamp < CACHE_TTL) {{
                return status;
            }}
        }}

        return new Promise((resolve) => {{
            const iframe = document.createElement('iframe');
            let timeout;

            const cleanup = () => {{
                clearTimeout(timeout);
                iframe.remove();
            }};

            iframe.onload = () => {{
                try {{
                    const doc = iframe.contentDocument || iframe.contentWindow.document;
                    const errorElement = doc.getElementById('main-frame-error');
                    const isChromeError = getComputedStyle(doc.documentElement)
                        .backgroundImage.includes('linear-gradient(45deg, #f3f4f6 25%');
                    
                    const isValid = !errorElement && !isChromeError;
                    localStorage.setItem(cacheKey, JSON.stringify({{
                        status: isValid,
                        timestamp: Date.now()
                    }}));
                    resolve(isValid);
                }} catch (error) {{
                    localStorage.setItem(cacheKey, JSON.stringify({{
                        status: true,
                        timestamp: Date.now()
                    }}));
                    resolve(true);
                }}
                cleanup();
            }};

            iframe.onerror = () => {{
                localStorage.setItem(cacheKey, JSON.stringify({{
                    status: false,
                    timestamp: Date.now()
                }}));
                resolve(false);
                cleanup();
            }};

            timeout = setTimeout(() => {{
                localStorage.setItem(cacheKey, JSON.stringify({{
                    status: false,
                    timestamp: Date.now()
                }}));
                resolve(false);
                cleanup();
            }}, 4000);

            iframe.src = url;
            document.body.appendChild(iframe);
        }});
    }}

    async function processBatch(batch) {{
        const promises = batch.map((item, index) => 
            new Promise(resolve => 
                setTimeout(async () => {{
                    const url = item.dataset.url;
                    const hash = item.dataset.hash;

                    try {{
                        const isValid = await validateUrl(url, hash);
                        if (!isValid) {{
                            item.remove();
                        }}
                    }} catch {{
                        item.remove();
                    }}
                    resolve();
                }}, index * DELAY_BETWEEN_CHECKS)
            )
        );
        await Promise.all(promises);
    }}

    async function processUrls() {{
        // Remove blocked domains immediately
        document.querySelectorAll('.url-item').forEach(item => {{
            if (isBlockedDomain(item.dataset.url)) {{
                item.remove();
            }}
        }});

        // Remove cached invalid items
        document.querySelectorAll('.url-item').forEach(item => {{
            const hash = item.dataset.hash;
            const cacheKey = getCacheKey(hash);
            const cached = localStorage.getItem(cacheKey);
            
            if (cached) {{
                const {{ status }} = JSON.parse(cached);
                if (!status) {{
                    item.remove();
                }}
            }}
        }});

        // Process remaining valid items in batches
        const items = Array.from(document.querySelectorAll('.url-item'));
        const batches = [];
        for (let i = 0; i < items.length; i += BATCH_SIZE) {{
            batches.push(items.slice(i, i + BATCH_SIZE));
        }}

        for (const batch of batches) {{
            await processBatch(batch);
            await new Promise(r => setTimeout(r, DELAY_BETWEEN_CHECKS));
        }}
    }}

    window.addEventListener('DOMContentLoaded', processUrls);
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)
