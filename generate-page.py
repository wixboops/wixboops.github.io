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
    <title>Interactive Dropdown Menu</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .scroll-transition {
            transition: opacity 0.5s ease-in-out;
        }
        .scroll-transition:hover {
            opacity: 1 !important;
        }
    </style>
</head>
<body class="bg-gray-900 text-white">
    <div class="container mx-auto p-4">
        <h1 class="text-4xl font-bold text-center mb-8">Interactive Dropdown Menu</h1>
        <div class="space-y-4">
"""

# Add buttons and dropdowns for each title
for title, items in data.items():
    html_content += f"""
            <div class="bg-gray-800 p-4 rounded-lg shadow-lg">
                <button onclick="toggleDropdown('{title}')" class="w-full text-left text-xl font-semibold focus:outline-none">
                    {title}
                </button>
                <ul id="{title}" class="mt-2 space-y-2 hidden">
    """
    for item in items:
        html_content += f"""
                    <li id="li-{item}" class="url-item">
                        <a href="{item}" class="block p-2 bg-gray-700 rounded hover:bg-gray-600 transition-colors" target="_blank" rel="noopener noreferrer">
                            {item}
                            <span id="status-{item}" class="ml-2"></span>
                        </a>
                    </li>
        """
    html_content += """
                </ul>
            </div>
    """

# Close the HTML content
html_content += """
        </div>
    </div>

    <script>
        // Toggle dropdown visibility
        function toggleDropdown(id) {
            const dropdown = document.getElementById(id);
            dropdown.classList.toggle('hidden');
        }

        // Check if a URL is reachable
        async function checkUrlReachability(url) {
            try {
                const response = await fetch(url, {
                    method: 'HEAD', // Lightweight check (no need to download content)
                    mode: 'no-cors' // Bypass CORS restrictions for simple reachability
                });
                return true;
            } catch (error) {
                return false;
            }
        }

        // Update UI based on URL status
        async function updateUrlStatus(url) {
            const isReachable = await checkUrlReachability(url);
            const statusElement = document.getElementById(`status-${url}`);
            const liElement = document.getElementById(`li-${url}`);

            if (isReachable) {
                statusElement.textContent = '✓';
                statusElement.classList.add('text-green-400');
            } else {
                statusElement.textContent = '✕';
                statusElement.classList.add('text-red-400');
                setTimeout(() => {
                    liElement.remove(); // Remove unreachable URLs after 2 seconds
                }, 2000);
            }
        }

        // Process URLs in batches (3 at a time)
        async function processUrls() {
            const urlElements = document.querySelectorAll('.url-item');
            const maxConcurrentChecks = 3;
            
            for (let i = 0; i < urlElements.length; i += maxConcurrentChecks) {
                const batch = Array.from(urlElements).slice(i, i + maxConcurrentChecks);
                await Promise.all(
                    batch.map(li => {
                        const url = li.querySelector('a').href;
                        return updateUrlStatus(url);
                    })
                );
                await new Promise(resolve => setTimeout(resolve, 200)); // 0.2s delay
            }
        }

        // Start processing URLs
        processUrls();
    </script>
</body>
</html>
"""

# Save the HTML file
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("Page generation completed successfully. File saved as index.html.")
