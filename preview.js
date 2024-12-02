// preview.js

// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    // Select the main preview image
    const mainPreviewImage = document.getElementById("previewImg");

    // Select all smaller preview images
    const previewImages = document.querySelectorAll(".preview");

    // Loop through each smaller preview image
    previewImages.forEach((preview) => {
        // Add a click event listener to each smaller preview image
        preview.addEventListener("click", () => {
            // Update the main preview image's src to match the clicked image's src
            mainPreviewImage.src = preview.src;

            // Optionally, you can add an active state to highlight the selected image
            previewImages.forEach(img => img.classList.remove("active"));
            preview.classList.add("active");
        });
    });
});
