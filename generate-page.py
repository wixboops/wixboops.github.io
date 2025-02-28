import json

# Load the JSON data
with open("extracted-data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Generate the HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Availability Checker</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        iframe {
            display: none !important;
        }
        .fade-in {
            animation: fadeIn 0.3s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
</head>
<body class="bg-gray-900 text-white">
    <div class="container mx-auto p-4">
        <h1 class="text-4xl font-bold text-center mb-8">Proxy List Status Check</h1>
        <div class="space-y-4">
"""

# Add buttons and dropdowns for each title
for title, items in data.items():
    html_content += f"""
            <div class="bg-gray-800 p-4 rounded-lg shadow-lg fade-in">
                <button onclick="toggleDropdown('{title}')" 
                        class="w-full text-left text-xl font-semibold focus:outline-none hover:bg-gray-700 p-2 rounded">
                    {title}
                </button>
                <ul id="{title}" class="mt-2 space-y-2 hidden">
    """
    for item in items:
        html_content += f"""
                    <li id="li-{item}" class="url-item">
                        <div class="flex items-center p-2 bg-gray-700 rounded">
                            <span class="status-indicator w-3 h-3 rounded-full mr-2"></span>
                            <a href="{item}" class="hover:text-blue-400 transition-colors" target="_blank">{item}</a>
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
        async function checkUrlsSequentially() {
            const urlItems = Array.from(document.querySelectorAll('.url-item'));
            
            for (const item of urlItems) {
                const url = item.querySelector('a').href;
                const indicator = item.querySelector('.status-indicator');
                
                await new Promise((resolve) => {
                    const iframe = document.createElement('iframe');
                    iframe.src = url;
                    
                    const cleanup = () => {
                        iframe.remove();
                        setTimeout(resolve, 200); // 0.2s delay between checks
                    };

                    iframe.onload = () => {
                        indicator.classList.add('bg-green-500');
                        cleanup();
                    };
                    
                    iframe.onerror = () => {
                        indicator.classList.add('bg-red-500');
                        setTimeout(() => {
                            item.classList.add('opacity-50', 'line-through');
                        }, 2000);
                        cleanup();
                    };
                    
                    document.body.appendChild(iframe);
                });
            }
        }

        function toggleDropdown(id) {
            const dropdown = document.getElementById(id);
            dropdown.classList.toggle('hidden');
        }

        // Start checking when page loads
        window.addEventListener('DOMContentLoaded', checkUrlsSequentially);
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("Page generation completed successfully. File saved as index.html.")
