document.addEventListener('DOMContentLoaded', () => {
    const uploadBtn = document.getElementById('upload-btn');
    const fileInput = document.getElementById('file-input');
    const browseCreate = document.getElementById('browse-create');
    const createNew = document.getElementById('createNew');

    // Check if upload button and file input exist
    if (uploadBtn && fileInput) {
        uploadBtn.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', async (event) => {
            const file = event.target.files[0];
            if (file) {
                if (file.name.endsWith('.csv')) {
                    const formData = new FormData();
                    formData.append('file', file);

                    try {
                        const response = await fetch('/', {
                            method: 'POST',
                            body: formData,
                        });

                        if (response.redirected) {
                            // Redirect to /data-cleaning
                            window.location.href = response.url;
                        } else {
                            alert('An error occurred while uploading the file.');
                        }
                    } catch (error) {
                        alert('An error occurred while uploading the file.');
                        console.error(error);
                    }
                } else {
                    alert('Please upload a valid .csv file.');
                    fileInput.value = ''; // Reset the input
                }
            }
        });
    } else {
        console.warn("Upload button or file input element not found.");
    }

    // Check if browse-create button exists
    if (browseCreate) {
        browseCreate.addEventListener('click', () => {
            // Redirect to the /browse-file URL
            window.location.href = '/browse-file';
        });
    } else {
        console.warn("Button with ID 'browse-create' not found.");
    }

    // Check if createNew button exists
    if (createNew) {
        createNew.addEventListener('click', () => {
            // Redirect to the /create-new URL
            window.location.href = '/create-new';
        });
    } else {
        console.warn("Button with ID 'createNew' not found.");
    }
});
