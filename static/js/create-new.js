document.getElementById('excelButton').addEventListener('click', function() {
    document.getElementById('excelPopup').style.display = 'block';
});

// Add a close button to the popup (recommended)
document.getElementById('excelPopup').addEventListener('click', function(event) {
  if (event.target.id === 'excelPopup') {  //only closes if you click on background
    this.style.display = 'none';
  }
})