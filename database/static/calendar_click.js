function handleButtonClick(){
    let link = document.getElementById("cal_link").value
    

    // Send an AJAX request to Flask to store the value
    fetch('/calendar_link', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'cal_link': link })
    })
    .then(response => {
        if (response.status === 204) {
            console.log("Calendar link saved successfully!");
            showPopUp('/calendar');  // Redirect or handle the response
        } else {
            console.error("Error saving calendar link!");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}