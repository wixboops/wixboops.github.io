import json

with open("extracted-data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proxy Validation System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .status-dot { 
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        .checking { background: #94a3b8; }
        .valid { background: #10b981; }
        .invalid { background: #ef4444; }
        iframe { display: none; }
    </style>
</head>
<body class="bg-gray-900 text-gray-100">
    <div class="container mx-auto p-4">
        <h1 class="text-3xl font-bold mb-6 text-center">Proxy Server Status</h1>
        <div class="space-y-4">
"""

for title, items in data.items():
    html_content += f"""
            <div class="bg-gray-800 rounded-lg p-4 shadow-xl">
                <h2 class="text-xl font-semibold mb-2">{title}</h2>
                <ul class="space-y-2">
    """
    for idx, item in enumerate(items):
        html_content += f"""
                    <li class="proxy-item" data-url="{item}">
                        <div class="flex items-center p-3 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors">
                            <span class="status-dot checking"></span>
                            <span class="url">{item}</span>
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
    async function validateProxy(url) {
        return new Promise((resolve) => {
            const iframe = document.createElement('iframe');
            let timeoutId;

            const cleanup = () => {
                clearTimeout(timeoutId);
                iframe.remove();
            };

            // First check: Basic iframe load
            iframe.onload = () => {
                cleanup();
                // Secondary check: API endpoint verification
                fetch('https://httpbin.org/get', { 
                    mode: 'no-cors',
                    headers: { 'Target-URL': url }
                })
                .then(() => resolve(true))
                .catch(() => resolve(false));
            };

            iframe.onerror = () => {
                cleanup();
                resolve(false);
            };

            timeoutId = setTimeout(() => {
                cleanup();
                resolve(false);
            }, 5000);

            iframe.src = url;
            document.body.appendChild(iframe);
        });
    }

    async function checkProxies() {
        const proxies = Array.from(document.querySelectorAll('.proxy-item'));
        
        for (const proxy of proxies) {
            const dot = proxy.querySelector('.status-dot');
            const url = proxy.dataset.url;
            
            dot.classList.replace('checking', 'invalid');
            
            try {
                const isValid = await validateProxy(url);
                dot.classList.replace('invalid', isValid ? 'valid' : 'invalid');
                
                if (!isValid) {
                    setTimeout(() => {
                        proxy.style.opacity = '0.3';
                        proxy.style.textDecoration = 'line-through';
                    }, 2000);
                }
            } catch {
                dot.classList.replace('invalid', 'invalid');
            }
            
            await new Promise(r => setTimeout(r, 200));
        }
    }

    window.addEventListener('DOMContentLoaded', checkProxies);
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)
