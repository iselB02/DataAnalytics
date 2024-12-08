document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('uploadModal');
    const uploadSelect = document.getElementById('uploadSelect');
    const createSelect = document.getElementById('createSelect');
    const closeModal = document.querySelector('.close');
    const dropZone = document.querySelector('.drop-zone');
    const fileInput = document.getElementById('file-input');
    const tableBody = document.getElementById('tableBody');

    // File Upload Functionality
    function handleFileUpload(file) {
        if (!file) return;

        const fileName = file.name;
        const fileType = file.type || fileName.split('.').pop();
        const filePath = URL.createObjectURL(file);
        const timestamp = new Date().toLocaleString();

        // Add file to table
        const newRow = tableBody.insertRow();
        newRow.innerHTML = `
            <td>${fileName}</td>
            <td>${fileType}</td>
            <td>${filePath}</td>
            <td>${timestamp}</td>
        `;

        // Save to local storage
        saveFileToLocalStorage({
            name: fileName,
            type: fileType,
            path: filePath,
            timestamp: timestamp
        });

        // Close modal
        modal.style.display = 'none';
    }

    // Local Storage Management
    function saveFileToLocalStorage(fileData) {
        let files = JSON.parse(localStorage.getItem('uploadedFiles') || '[]');
        files.push(fileData);
        localStorage.setItem('uploadedFiles', JSON.stringify(files));
    }

    function loadFilesFromLocalStorage() {
        const files = JSON.parse(localStorage.getItem('uploadedFiles') || '[]');
        files.forEach(file => {
            const newRow = tableBody.insertRow();
            newRow.innerHTML = `
                <td>${file.name}</td>
                <td>${file.type}</td>
                <td>${file.path}</td>
                <td>${file.timestamp}</td>
            `;
        });
    }

    // File Creation Functionality
    createSelect.addEventListener('change', function() {
        const fileType = this.value;
        const content = generateSampleContent(fileType);
        const blob = new Blob([content], { type: getContentType(fileType) });
        const filename = `sample_file.${fileType}`;

        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    });

    function generateSampleContent(fileType) {
        switch(fileType) {
            case 'pdf':
                return 'Sample PDF Content';
            case 'csv':
                return 'Name,Age,City\nJohn Doe,30,New York\nJane Smith,25,San Francisco';
            case 'xls':
                return 'Sample Excel Content';
            default:
                return 'Sample File Content';
        }
    }

    function getContentType(fileType) {
        switch(fileType) {
            case 'pdf': return 'application/pdf';
            case 'csv': return 'text/csv';
            case 'xls': return 'application/vnd.ms-excel';
            default: return 'text/plain';
        }
    }

    // Modal and File Selection
    uploadSelect.addEventListener('change', function () {
        if (['csv', 'xls', 'xlsx'].includes(this.value)) {
            modal.style.display = 'flex';
        }
    });

    // Close modal when the close button is clicked
    closeModal.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    // Close modal when clicking outside the modal content
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Drag and Drop Functionality
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        handleFileUpload(file);
    });

    // Load existing files when page loads
    loadFilesFromLocalStorage();
});