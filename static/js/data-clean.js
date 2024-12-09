document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".cleaning-selections button");
    const tools = document.querySelectorAll(".cleaning-tool > div");

    // Set default display for the 'missing-val' tool
    const defaultTool = document.getElementById("missing-val");
    tools.forEach(tool => {
        tool.style.display = tool === defaultTool ? "flex" : "none"; // Show 'missing-val' by default
    });

    // Set event listeners for tool selection buttons
    buttons.forEach(button => {
        button.addEventListener("click", () => {
            // Hide all tools first
            tools.forEach(tool => (tool.style.display = "none"));

            // Get the tool ID from the button's data-tool attribute
            const toolId = button.getAttribute("data-tool");

            // Show the selected tool
            const selectedTool = document.getElementById(toolId);
            if (selectedTool) {
                selectedTool.style.display = "flex"; // Display the selected tool
            }
        });
    });

    // Missing Value - Row actions
    document.getElementById("remove-all-rows")?.addEventListener("click", () => {
        const table = document.querySelector("table");
        const rows = table.querySelectorAll("tr");
        rows.forEach(row => row.remove());  // Remove all rows
        alert("All rows removed");
    });

    document.getElementById("remove-rows-column")?.addEventListener("click", () => {
        const columnName = prompt("Enter the column name to remove rows where it's empty:");
        const table = document.querySelector("table");
        const rows = table.querySelectorAll("tr");
        rows.forEach(row => {
            const cells = row.querySelectorAll("td, th");
            const columnIndex = Array.from(cells).findIndex(cell => cell.textContent.trim().toLowerCase() === columnName.toLowerCase());
            if (columnIndex !== -1 && !cells[columnIndex].textContent.trim()) {
                row.remove();  // Remove the row if the specific column is empty
            }
        });
        alert(`Rows in column "${columnName}" with missing values removed`);
    });

    // Missing Value - Column actions
    document.getElementById("remove-column")?.addEventListener("click", () => {
        const columnName = prompt("Enter the column name to remove:");
        const table = document.querySelector("table");
        const headers = table.querySelectorAll("th");
        const columnIndex = Array.from(headers).findIndex(header => header.textContent.trim().toLowerCase() === columnName.toLowerCase());
        if (columnIndex !== -1) {
            const rows = table.querySelectorAll("tr");
            rows.forEach(row => {
                const cells = row.querySelectorAll("td");
                if (cells[columnIndex]) {
                    cells[columnIndex].remove();  // Remove the cell in the given column
                }
            });
            alert(`Column "${columnName}" removed`);
        } else {
            alert(`Column "${columnName}" not found`);
        }
    });

    // Missing Value - Fill actions
    document.getElementById("fill-forward")?.addEventListener("click", () => {
        const table = document.querySelector("table");
        const rows = table.querySelectorAll("tr");
        rows.forEach((row, rowIndex) => {
            const cells = row.querySelectorAll("td");
            cells.forEach((cell, colIndex) => {
                if (!cell.textContent.trim() && rowIndex > 0) {
                    const prevCell = rows[rowIndex - 1].querySelectorAll("td")[colIndex];
                    cell.textContent = prevCell ? prevCell.textContent : ""; // Fill with the previous row's value
                }
            });
        });
        alert("Forward fill applied");
    });

    document.getElementById("fill-backward")?.addEventListener("click", () => {
        const table = document.querySelector("table");
        const rows = table.querySelectorAll("tr");
        for (let rowIndex = rows.length - 1; rowIndex >= 0; rowIndex--) {
            const row = rows[rowIndex];
            const cells = row.querySelectorAll("td");
            cells.forEach((cell, colIndex) => {
                if (!cell.textContent.trim() && rowIndex < rows.length - 1) {
                    const nextCell = rows[rowIndex + 1].querySelectorAll("td")[colIndex];
                    cell.textContent = nextCell ? nextCell.textContent : ""; // Fill with the next row's value
                }
            });
        }
        alert("Backward fill applied");
    });

    // Format buttons
    document.getElementById("uppercase")?.addEventListener("click", () => {
        const table = document.querySelector("table");
        const rows = table.querySelectorAll("tr");
        rows.forEach(row => {
            const cells = row.querySelectorAll("td");
            cells.forEach(cell => {
                cell.textContent = cell.textContent.toUpperCase();
            });
        });
        alert("Text converted to Uppercase");
    });

    document.getElementById("lowercase")?.addEventListener("click", () => {
        const table = document.querySelector("table");
        const rows = table.querySelectorAll("tr");
        rows.forEach(row => {
            const cells = row.querySelectorAll("td");
            cells.forEach(cell => {
                cell.textContent = cell.textContent.toLowerCase();
            });
        });
        alert("Text converted to Lowercase");
    });

    document.getElementById("capitalize")?.addEventListener("click", () => {
        const table = document.querySelector("table");
        const rows = table.querySelectorAll("tr");
        rows.forEach(row => {
            const cells = row.querySelectorAll("td");
            cells.forEach(cell => {
                cell.textContent = cell.textContent.replace(/\b\w/g, char => char.toUpperCase()); // Capitalize each word
            });
        });
        alert("Text capitalized");
    });

    // Remove Duplicates
    document.getElementById("remove-duplicates")?.addEventListener("click", () => {
        const table = document.querySelector("table");
        const rows = table.querySelectorAll("tr");
        const seen = new Set();
        rows.forEach(row => {
            const cells = row.querySelectorAll("td");
            const rowKey = Array.from(cells).map(cell => cell.textContent.trim()).join("|");
            if (seen.has(rowKey)) {
                row.remove();  // Remove duplicate row
            } else {
                seen.add(rowKey);
            }
        });
        alert("Duplicates removed");
    });
});
