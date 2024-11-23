document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".cleaning-selections button");
    const tools = document.querySelectorAll(".cleaning-tool > div");

    // Set default display for the 'missing-val' tool
    const defaultTool = document.getElementById("missing-val");
    tools.forEach(tool => {
        tool.style.display = tool === defaultTool ? "flex" : "none";
    });

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            // Hide all tools
            tools.forEach(tool => (tool.style.display = "none"));

            // Get the tool ID from the button's data-tool attribute
            const toolId = button.getAttribute("data-tool");

            // Show the selected tool
            const selectedTool = document.getElementById(toolId);
            if (selectedTool) {
                selectedTool.style.display = "flex";
            }
        });
    });
});
