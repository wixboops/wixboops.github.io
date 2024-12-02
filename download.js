document.getElementById('downloadButton').addEventListener('click', function() {
    // Replace 'your-file-path-here.exe' with the actual path to your downloadable file
    const fileUrl = 'wix.txt';
    
    // Create a temporary anchor element
    const link = document.createElement('a');
    
    // Set the href to the file URL
    link.href = fileUrl;
    
    // Set the download attribute with a filename
    link.download = 'WIX-Executor.exe';
    
    // Append to the body
    document.body.appendChild(link);
    
    // Trigger the download
    link.click();
    
    // Remove the link from the document
    document.body.removeChild(link);
});
