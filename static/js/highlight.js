document.addEventListener("DOMContentLoaded", () => {
    // Select all navigation links
    const navLinks = document.querySelectorAll(".nav-content"); // Use querySelectorAll for multiple elements

    // Get the current path
    const currentPath = window.location.pathname;

    // Loop through links and add 'active' class to the matching href
    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
});
