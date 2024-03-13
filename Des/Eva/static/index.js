


document.querySelector(".start").addEventListener('click', function() {
    // Send an HTTP request to the Flask server when button is clicked
    fetch('/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.text())
    .then(data => {
        console.log(data); // Log the response from the server
        // Handle the response if needed
    })
    .catch(error => {
        console.error('Error:', error);
    });
});