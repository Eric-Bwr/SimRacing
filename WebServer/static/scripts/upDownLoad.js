document.getElementById('fileUpload').addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        // Handle the uploaded file here
        console.log('File uploaded:', file.name);

        // You can send the file to your backend using AJAX or Socket.io
        // Example with Socket.io:
        const reader = new FileReader();
        reader.onload = function(event) {
            const fileContent = event.target.result;
            // Emit the file content to the server
            socket.emit('fileUpload', { fileName: file.name, data: fileContent });
        };
        reader.readAsText(file);
    }
});

document.getElementById('downloadButton').addEventListener('click', function() {
    const fileName = 'data.txt'; // You can set this dynamically
    const data = 'Your data here...'; // Replace this with the data you want to download

    const blob = new Blob([data], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = fileName;

    document.body.appendChild(a);
    a.click();

    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
});
