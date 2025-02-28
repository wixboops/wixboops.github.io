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
        /* Custom scroll animation */
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
                    <li>
                        <a href="{item}" class="block p-2 bg-gray-700 rounded hover:bg-gray-600 transition-colors" target="_blank" rel="noopener noreferrer">
                            {item}
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

        // Scroll animation for seamless looping
        document.addEventListener('scroll', () => {
            const elements = document.querySelectorAll('.scroll-transition');
            elements.forEach(el => {
                const rect = el.getBoundingClientRect();
                const isVisible = rect.top < window.innerHeight && rect.bottom >= 0;
                el.style.opacity = isVisible ? 1 : 0.3;
            });
        });
    </script>
</body>
</html>
"""

# Save the HTML file
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("Page generation completed successfully. File saved as index.html.")
