document.getElementById('downloadButton').addEventListener('click', function() {
    // Replace 'your-file-path-here.exe' with the actual path to your downloadable file
    const fileUrl = 'WixBootstrapper-v2.6.exe';
    
    // Create a temporary anchor element
    const link = document.createElement('a');
    
    // Set the href to the file URL
    link.href = fileUrl;
    
    // Set the download attribute with a filename
    link.download = 'WixBootstrapper-v2.6.exe';
    
    // Append to the body
    document.body.appendChild(link);
    
    // Trigger the download
    link.click();
    
    // Remove the link from the document
    document.body.removeChild(link);
});
