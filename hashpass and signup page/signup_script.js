document.addEventListener('DOMContentLoaded', function() {
    // Attach click event listener to signup button
    document.getElementById('button-signup').addEventListener('click', function() {
      // Get input values
      var name = document.getElementById('name').value;
      var username = document.getElementById('new-username').value;
      var password = document.getElementById('new-password').value;
      
      // Dummy check for input fields (replace this with actual validation)
      if (name.trim() === "" || username.trim() === "" || password.trim() === "") {
        alert("Please enter all required fields.");
        return;
      }
  
      // Example redirect after successful signup:
      window.location.href = "loginPage.html";
    });
  });
  