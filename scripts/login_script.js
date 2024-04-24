document.addEventListener('DOMContentLoaded', function() {
  // Attach click event listener to login button
  document.getElementById('loginButton').addEventListener('click', function() {
    // Get input values
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    
    // Dummy check for username and password (replace this with actual validation)
    if (username.trim() === "" || password.trim() === "") {
      alert("Please enter both username and password.");
      return;
    }

    // Dummy check for login (replace this with actual authentication logic)
    if (username === "username" && password === "password") {
      alert("Login successful!");
      // Redirect to dashboard or another page upon successful login
      window.location.href = "PopUp.html";
    } else {
      alert("Invalid username or password.");
    }
  });
});