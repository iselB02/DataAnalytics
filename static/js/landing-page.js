document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('uploadModal');
    const uploadSelect = document.getElementById('uploadSelect');
    const closeModal = document.querySelector('.close');
    const dropZone = document.querySelector('.drop-zone');
    const fileInput = document.getElementById('file-input');
    const tableBody = document.getElementById('tableBody');
    const createReportButton = document.getElementById('createReportButton');

    let userInteractedWithUpload = false;

    // Open Modal When Upload Option is Selected
    uploadSelect.addEventListener('change', function () {
        if (['csv', 'xls', 'xlsx'].includes(this.value)) {
            modal.style.display = 'flex'; // Show modal
        }
        userInteractedWithUpload = true; // Mark that the user interacted with the upload dropdown
    });

    // Close Modal When Close Button is Clicked
    closeModal.addEventListener('click', function () {
        modal.style.display = 'none'; // Hide modal
    });

    // Close Modal When Clicking Outside of Modal Content
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none'; // Hide modal
        }
    });

    // Drop Zone: Simulate File Input Click on Drop Zone Click
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag-and-Drop Functionality for Drop Zone
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over'); // Highlight drop zone
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over'); // Remove highlight
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over'); // Remove highlight
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]); // Handle the uploaded file
        }
    });

    // Handle File Input Change Event
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        handleFileUpload(file); // Handle the uploaded file
    });

    // Handle File Upload
    function handleFileUpload(file) {
        if (!file) return;

        const fileName = file.name;
        const fileType = file.type || fileName.split('.').pop();
        const filePath = URL.createObjectURL(file);
        const timestamp = new Date().toLocaleString();

        // Add File to the Table
        const newRow = tableBody.insertRow();
        newRow.innerHTML = `
            <td>${fileName}</td>
            <td>${fileType}</td>
            <td><a href="${filePath}" target="_blank">View File</a></td>
            <td>${timestamp}</td>
        `;

        // Save to Local Storage
        saveFileToLocalStorage({
            name: fileName,
            type: fileType,
            path: filePath,
            timestamp: timestamp,
        });

        // Close Modal After File Upload
        modal.style.display = 'none';
    }

    // Save File Data to Local Storage
    function saveFileToLocalStorage(fileData) {
        let files = JSON.parse(localStorage.getItem('uploadedFiles') || '[]');
        files.push(fileData);
        localStorage.setItem('uploadedFiles', JSON.stringify(files));
    }

    // Load Files from Local Storage on Page Load
    function loadFilesFromLocalStorage() {
        const files = JSON.parse(localStorage.getItem('uploadedFiles') || '[]');
        files.forEach((file) => {
            const newRow = tableBody.insertRow();
            newRow.innerHTML = `
                <td>${file.name}</td>
                <td>${file.type}</td>
                <td><a href="${file.path}" target="_blank">View File</a></td>
                <td>${file.timestamp}</td>
            `;
        });
    }

    // Create Blank Report Functionality
    createReportButton.addEventListener('click', function () {
        window.location.href = '/report'; // Redirect to the blank report page
    });

    // Load Files When Page Loads
    loadFilesFromLocalStorage();
});
