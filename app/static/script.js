$(document).ready(function () {
    const scrapeForm = $("#scrape-form");
    const scrapedResultsContainer = $("#scraped-data");
    const downloadJsonButton = $("#download-json");
    const downloadCsvButton = $("#download-csv");
    const savedResultsButton = $("#load-saved-results");
    const savedResultsContainer = $("#saved-results-container");

    // Handle scraping form submission
    scrapeForm.on("submit", function (event) {
        event.preventDefault();
        const urlInput = $("#url").val();
        console.log(urlInput);

        $.ajax({
            url: "/scrape",
            method: "POST",
            data: { url: urlInput },
            success: function (response) {
                if (response.data) {
                    const scrapedData = response.data; // Assuming the server sends a 'data' object
                    let displayContent = '<h3>Scraped Data:</h3>';
                    
                    // Display Titles
                    if (scrapedData.titles && scrapedData.titles.length > 0) {
                        displayContent += '<h4>Titles:</h4>';
                        displayContent += '<ul>';
                        scrapedData.titles.forEach(title => {
                            displayContent += `<li>${title}</li>`;
                        });
                        displayContent += '</ul>';
                    }

                    // Display Links
                    if (scrapedData.links && scrapedData.links.length > 0) {
                        displayContent += '<h4>Links:</h4>';
                        displayContent += '<ul>';
                        scrapedData.links.forEach(link => {
                            displayContent += `<li><a href="${link}" target="_blank">${link}</a></li>`;
                        });
                        displayContent += '</ul>';
                    }

                    // Display Images
                    if (scrapedData.images && scrapedData.images.length > 0) {
                        displayContent += '<h4>Images:</h4>';
                        scrapedData.images.forEach(image => {
                            displayContent += `<div><img src="${image}" alt="Image" style="max-width: 100%; height: auto;"></div>`;
                        });
                    }

                    // Insert the scraped data into the container
                    scrapedResultsContainer.html(displayContent);
                } else {
                    scrapedResultsContainer.html("<p>No data found or scraping failed.</p>");
                }
            },
            error: function (xhr) {
                console.error("Error during scraping:", xhr.responseText);
                scrapedResultsContainer.html("<p>Error occurred while scraping the website.</p>");
            },
        });
    });

    // Download JSON
    downloadJsonButton.on("click", function () {
        const urlInput = $("#url").val();

        $.ajax({
            url: "/download/json",
            method: "POST",
            data: { url: urlInput },
            xhrFields: { responseType: "blob" },
            success: function (blob) {
                const downloadUrl = URL.createObjectURL(blob);
                const a = $("<a>")
                    .attr("href", downloadUrl)
                    .attr("download", "scraped_data.json")
                    .appendTo("body");
                a[0].click();
                a.remove();
            },
            error: function (xhr) {
                console.error("Error downloading JSON:", xhr.responseText);
            },
        });
    });

    // Download CSV
    downloadCsvButton.on("click", function () {
        const urlInput = $("#url").val();

        $.ajax({
            url: "/download/csv",
            method: "POST",
            data: { url: urlInput },
            xhrFields: { responseType: "blob" },
            success: function (blob) {
                const downloadUrl = URL.createObjectURL(blob);
                const a = $("<a>")
                    .attr("href", downloadUrl)
                    .attr("download", "scraped_data.csv")
                    .appendTo("body");
                a[0].click();
                a.remove();
            },
            error: function (xhr) {
                console.error("Error downloading CSV:", xhr.responseText);
            },
        });
    });

    // Load saved results
    savedResultsButton.on("click", function () {
        $.ajax({
            url: "/saved_results",
            method: "GET",
            success: function (data) {
                if (data.success && data.saved_results.length > 0) {
                    savedResultsContainer.html(
                        data.saved_results
                            .map((result) => {
                                return ` 
                                    <div>
                                        <p><strong>URL:</strong> <a href="${result.url}" target="_blank">${result.url}</a></p>
                                        <p><strong>Timestamp:</strong> ${result.timestamp}</p>
                                    </div>
                                `;
                            })
                            .join("")
                    );
                } else {
                    savedResultsContainer.html("<p>No saved results available.</p>");
                }
            },
            error: function (xhr) {
                console.error("Error loading saved results:", xhr.responseText);
                savedResultsContainer.html("<p>Error loading saved results.</p>");
            },
        });
    });
});
