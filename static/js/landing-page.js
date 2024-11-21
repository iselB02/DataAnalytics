// Get references to elements
const uploadBtn = document.getElementById('upload-btn');
const fileInput = document.getElementById('file-input');

// Trigger the file input click when the button is clicked
uploadBtn.addEventListener('click', () => {
    fileInput.click();
});

// Handle file input change
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        if (file.name.endsWith('.csv')) {
            alert(`File uploaded: ${file.name}`);
            // Perform additional actions with the file (e.g., upload to server)
        } else {
            alert('Please upload a valid .csv file.');
            fileInput.value = ''; // Reset the input
        }
    }
});
