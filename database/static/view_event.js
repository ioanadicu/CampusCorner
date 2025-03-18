
function viewEvent(description) {
    fetch(`/event`)
        .then(response => response.text())  // We expect HTML content in response
        .then(eventHtml => {
            // Inject the event HTML into the pop-up container
            document.getElementById("event-info").innerHTML = eventHtml;
            let event_properties = description.split(",");
            const descriptionElement = document.getElementById("description");
            // Now, update the pop-up description and show the pop-up
            for (let i = 0; i < 3; i++) {
                const newDiv = document.createElement("div");
                // Set some content for the new div
                newDiv.textContent = event_properties[i];
                // Append the new div to the parent div
                descriptionElement.appendChild(newDiv);
            }
        });
}