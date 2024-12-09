document.addEventListener('DOMContentLoaded', function() {
    const keywordFilter = document.getElementById('keywordFilter');
    const tableRows = document.querySelectorAll('tbody tr');

    function filterTable() {
        const keyword = keywordFilter.value.toLowerCase();

        tableRows.forEach(row => {
            const nameCell = row.cells[1]; // Assuming 'Name' is the second column (index 1)
            const name = nameCell.textContent.toLowerCase();
            row.style.display = keyword.length === 0 || name.includes(keyword) ? '' : 'none';
        });
    }

    keywordFilter.addEventListener('input', filterTable);
});