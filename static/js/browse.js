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

document.addEventListener('DOMContentLoaded', function() {
    const keywordFilter = document.getElementById('keywordFilter');
    const tableBody = document.querySelector('tbody');
    const data = [ // Example data - replace with your actual data
      { icon: 'file-icon', name: 'My workspace', type: 'Workspace', opened: '10 hours ago', owner: '—', endorsement: '—', sensitivity: '—', location: 'Workspaces' },
      { icon: 'semantic-icon', name: 'cleaned_netflix_titles', type: 'Semantic model', opened: 'a month ago', owner: 'ERIKA BISOY', endorsement: '—', sensitivity: '—', location: 'My workspace' },
      //Add More data as needed.
    ];
  
    function createTableRow(item) {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td><svg class="${item.icon}" viewBox="0 0 16 16">
          </svg></td>
        <td>${item.name}</td>
        <td>${item.type}</td>
        <td>${item.opened}</td>
        <td>${item.owner}</td>
        <td>${item.endorsement}</td>
        <td>${item.sensitivity}</td>
        <td>${item.location}</td>
      `;
      return row;
    }
  
    function renderTable(filteredData) {
      tableBody.innerHTML = ''; // Clear existing rows
      filteredData.forEach(item => tableBody.appendChild(createTableRow(item)));
    }
  
    function filterTable() {
      const keyword = keywordFilter.value.toLowerCase();
      const filteredData = data.filter(item => item.name.toLowerCase().includes(keyword));
      renderTable(filteredData);
    }
  
    renderTable(data); // Initial render
    keywordFilter.addEventListener('input', filterTable);
  });