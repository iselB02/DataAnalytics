// Create new row
document.getElementById('add-row').addEventListener('click', function() {
  const tableBody = document.querySelector('#data-table tbody');
  const newRow = document.createElement('tr');
  let columns = document.querySelectorAll('#data-table thead th').length;

  newRow.innerHTML = `<td><button class="delete-row">X</button></td>`;
  for (let i = 1; i < columns; i++) {
      newRow.innerHTML += `<td><input type="text"></td>`;
  }

  tableBody.appendChild(newRow);

  // Add delete button functionality for the new row
  newRow.querySelector('.delete-row').addEventListener('click', function() {
      tableBody.removeChild(newRow);
  });
});

// Add new column
document.getElementById('add-column').addEventListener('click', function() {
  const tableHeader = document.querySelector('#data-table thead tr');
  const tableRows = document.querySelectorAll('#data-table tbody tr');

  // Add new column header
  const newHeader = document.createElement('th');
  newHeader.textContent = `Column${tableHeader.children.length}`;
  tableHeader.appendChild(newHeader);

  // Add input cells in each row
  tableRows.forEach(row => {
      const newCell = document.createElement('td');
      newCell.innerHTML = `<input type="text">`;
      row.appendChild(newCell);
  });
});
