document.getElementById('createBtn').addEventListener('click', function() {
    document.getElementById('createModal').style.display = 'block';
});

document.querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('createModal').style.display = 'none';
});

document.getElementById('addTagBtn').addEventListener('click', function() {
    const tagInput = document.createElement('input');
    tagInput.type = 'text';
    tagInput.classList.add('tag-input');
    tagInput.placeholder = 'Enter tag';
    document.getElementById('tagsContainer').appendChild(tagInput);
});

document
