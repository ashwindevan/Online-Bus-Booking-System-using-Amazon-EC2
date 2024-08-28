document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    
    var formData = new FormData(this); // Get form data
    
    fetch('/verify_otp', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.redirect) {
        window.location.href = data.redirect; // Redirect to the URL provided in the JSON response
      } else {
        console.error('Redirect URL not provided in the response');
      }
    })
    .catch(error => console.error('Error:', error));
  });