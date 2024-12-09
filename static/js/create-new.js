document.addEventListener('DOMContentLoaded', () => {
    const addRowButton = document.getElementById('add-row');
    const addColumnButton = document.getElementById('add-column');
    const table = document.getElementById('data-table');
    const tableNameInput = document.getElementById('tableName');
    const previewDiv = document.getElementById('preview');
  
    // Add Row functionality
    addRowButton.addEventListener('click', () => {
        const newRow = document.createElement('tr');
        const rowCount = table.rows.length;
  
        // Create delete button for the first column
        const deleteCell = document.createElement('td');
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'X';
        deleteButton.classList.add('delete-row');
        deleteCell.appendChild(deleteButton);
        newRow.appendChild(deleteCell);
  
        // Add editable cells to the row, including the second column
        for (let i = 1; i < table.rows[0].cells.length; i++) {
            const cell = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'text';
            cell.appendChild(input);
            newRow.appendChild(cell);
        }
  
        // Append the new row to the table
        table.querySelector('tbody').appendChild(newRow);
  
        // Add delete functionality to the new button
        deleteButton.addEventListener('click', () => {
            newRow.remove();
        });
    });
  
    // Add Column functionality
    addColumnButton.addEventListener('click', () => {
        const headers = table.querySelectorAll('th');
        const newColumnHeader = document.createElement('th');
        const input = document.createElement('input');
        input.type = 'text';
        input.classList.add('edit-column');
        input.value = `Column${headers.length + 1}`;
        newColumnHeader.appendChild(input);
  
        // Add a delete button for the column header (now just 'X')
        const deleteColumnHeaderButton = document.createElement('button');
        deleteColumnHeaderButton.textContent = 'X'; // Shortened text
        deleteColumnHeaderButton.classList.add('delete-column');
        newColumnHeader.appendChild(deleteColumnHeaderButton);
  
        table.querySelector('thead').rows[0].appendChild(newColumnHeader);
  
        // Add editable column cells for each row
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            const newCell = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'text';
            newCell.appendChild(input);
            row.appendChild(newCell);
        });
  
        // Handle column header change
        const columnInput = newColumnHeader.querySelector('input');
        columnInput.addEventListener('change', () => {
            const columnIndex = Array.from(table.querySelectorAll('th')).indexOf(newColumnHeader);
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                row.cells[columnIndex].querySelector('input').setAttribute('name', columnInput.value);
            });
        });
  
        // Handle column deletion
        deleteColumnHeaderButton.addEventListener('click', () => {
            // Find the index of the column to be deleted
            const columnIndex = Array.from(table.querySelectorAll('th')).indexOf(newColumnHeader);
  
            // Delete the column header
            newColumnHeader.remove();
  
            // Delete cells from all rows in this column and shift subsequent cells
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                // Remove the cell at the columnIndex
                row.cells[columnIndex].remove();
  
                // Shift all subsequent cells to the left by 1
                for (let i = columnIndex; i < row.cells.length - 1; i++) {
                    row.cells[i].innerHTML = row.cells[i + 1].innerHTML;
                    row.cells[i].querySelector('input').setAttribute('name', row.cells[i + 1].querySelector('input').getAttribute('name'));
                }
                // Remove the last cell as it's now a duplicate
                row.cells[row.cells.length - 1].remove();
            });
        });
    });
  
    // Update preview area
    const updatePreview = () => {
        const data = Array.from(table.rows).map(row => {
            const cells = Array.from(row.cells).map(cell => cell.querySelector('input') ? cell.querySelector('input').value : cell.textContent);
            return cells.join(' | ');
        }).join('<br>');
        previewDiv.innerHTML = data || "No data available";
    };
  
    // Update preview whenever input changes
    table.addEventListener('input', updatePreview);
  });