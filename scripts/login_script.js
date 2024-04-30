document.addEventListener('DOMContentLoaded', function() {
  // Attach click event listener to login button
  document.getElementById('button-login').addEventListener('click', function() {
    // Get input values
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    
    // Dummy check for username and password (replace this with actual validation)
    if (username.trim() === "" || password.trim() === "") {
      alert("Please enter both username and password.");
      return;
    }
    // Call auth_user function to check if username and password are valid
    auth_user(username,password)
  });
});

function auth_user(username, password) {
  fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({user: username, password: password}),
    })
    .then(response => response.json())
    .then(user => {
        var id = user.result;
        console.log(id);
        if (id == 0) {
          alert("Invalid username or password")
          return;
        } else {
          chrome.storage.sync.set({user: id});
          alert("Login successful!");
          window.location.href = "PopUp.html";
        }
    })
    .catch((error) => {
        console.error('Error:', error);
  });
}