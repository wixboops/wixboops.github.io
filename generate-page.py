import json

with open("extracted-data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced URL Validator</title>
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
        .error-pattern { background-image: linear-gradient(45deg, #f3f4f6 25%, transparent 25%), linear-gradient(-45deg, #f3f4f6 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #f3f4f6 75%), linear-gradient(-45deg, transparent 75%, #f3f4f6 75%); }
    </style>
</head>
<body class="bg-gray-900 text-gray-100">
    <div class="container mx-auto p-4">
        <h1 class="text-3xl font-bold mb-8 text-center text-purple-400">URL Validation System</h1>
        <div class="space-y-6">
"""

for title, items in data.items():
    html_content += f"""
            <div class="bg-gray-800 rounded-xl p-6 shadow-2xl">
                <h2 class="text-xl font-bold mb-4 text-blue-300">{title}</h2>
                <ul class="space-y-3">
    """
    for item in items:
        html_content += f"""
                    <li class="url-item group" data-url="{item}">
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
    async function validateUrl(url) {
        return new Promise((resolve) => {
            const iframe = document.createElement('iframe');
            let timeout;
            
            const cleanup = () => {
                clearTimeout(timeout);
                iframe.remove();
            };

            iframe.onload = () => {
                try {
                    // Check for Chrome's specific error page elements
                    const doc = iframe.contentDocument || iframe.contentWindow.document;
                    const errorElement = doc.getElementById('main-frame-error');
                    const errorStyles = window.getComputedStyle(doc.documentElement);
                    
                    // Detect Chrome error page background pattern
                    const isChromeError = errorStyles.backgroundImage.includes('linear-gradient(45deg, #f3f4f6 25%');
                    
                    resolve(!errorElement && !isChromeError);
                } catch (error) {
                    // Cross-origin block indicates actual page loaded
                    resolve(true);
                }
                cleanup();
            };

            iframe.onerror = () => {
                resolve(false);
                cleanup();
            };

            // 4-second timeout for validation
            timeout = setTimeout(() => {
                resolve(false);
                cleanup();
            }, 4000);

            iframe.src = url;
            document.body.appendChild(iframe);
        });
    }

    async function processUrls() {
        const items = document.querySelectorAll('.url-item');
        
        for (const item of items) {
            const dot = item.querySelector('.status-dot');
            const url = item.dataset.url;
            
            dot.style.backgroundColor = '#f59e0b'; // Yellow for checking
            
            try {
                const isValid = await validateUrl(url);
                dot.style.backgroundColor = isValid ? '#10b981' : '#ef4444';
                
                if (!isValid) {
                    item.classList.add('error-pattern', 'opacity-50');
                    setTimeout(() => {
                        item.style.display = 'none';
                    }, 2000);
                }
            } catch {
                dot.style.backgroundColor = '#ef4444';
            }
            
            await new Promise(r => setTimeout(r, 200));
        }
    }

    window.addEventListener('DOMContentLoaded', processUrls);
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)
