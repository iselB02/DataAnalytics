document.addEventListener('DOMContentLoaded', () => {
  const addRowButton = document.getElementById('add-row');
  const dataTable = document.getElementById('data-table').getElementsByTagName('tbody')[0];

  addRowButton.addEventListener('click', () => {
      const newRow = dataTable.insertRow();
      const deleteCell = newRow.insertCell();
      const deleteButton = document.createElement('button');
      deleteButton.textContent = 'X';
      deleteButton.classList.add('delete-row');
      deleteCell.appendChild(deleteButton);
      deleteButton.addEventListener('click', () => {
          dataTable.deleteRow(newRow.rowIndex);
      });

      // Add input cells for each column
      const columnCount = dataTable.rows[0].cells.length -1; //Subtract the delete column
      for (let i = 1; i <= columnCount; i++) {
          const cell = newRow.insertCell();
          const input = document.createElement('input');
          input.type = 'text';
          cell.appendChild(input);
      }
  });


  //Event Listener for deleting existing rows:
  dataTable.addEventListener('click', function(event){
      if(event.target.classList.contains('delete-row')){
          event.target.parentNode.parentNode.remove();
      }
  })


  document.getElementById('auto-create-report').addEventListener('click', () => {
      //Here you'd add your code to process the data and generate a report.
      //This would typically involve sending data to a server-side script.
      alert("Report creation logic not implemented yet."); // Placeholder
  });

  document.getElementById('cancel').addEventListener('click', () => {
      // Add your cancel logic here (e.g., clear the table or redirect).
      alert("Cancel logic not implemented yet."); // Placeholder
  });
});