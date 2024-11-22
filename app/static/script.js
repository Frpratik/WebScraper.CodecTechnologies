// Script for client-side interactivity
document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll(".delete-btn");
    deleteButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            if (!confirm("Are you sure you want to delete this result?")) {
                event.preventDefault();
            }
        });
    });

    const scrapeForm = document.querySelector("#scrape-form");
    scrapeForm.addEventListener("submit", () => {
        alert("Scraping started! This may take a few moments.");
    });
});
