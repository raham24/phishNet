function fetchProtectionStatus() {
    // Use the backend
    fetch('http://endpoint')
      .then(response => response.json())
      .then(data => {
        var checkBox = document.getElementById('toggleSwitch');
        // Assuming the API returns a JSON object with a boolean 'enabled' field
        if (data.enabled) {
          checkBox.classList.add('checked');
        } else {
          checkBox.classList.remove('checked');
        }
      })
      .catch(error => console.error('Error fetching status:', error));
  }
  
  document.addEventListener('DOMContentLoaded', function () {
    var checkBox = document.getElementById('toggleSwitch');
    checkBox.addEventListener('click', function () {
      // This could be improved to send the new status to the backend
      if (checkBox.classList.contains('checked')) {
        checkBox.classList.remove('checked');
      } else {
        checkBox.classList.add('checked');
      }
      // Here you would also make an API call to update the backend
    });
  
    // Get the initial protection status on load
    fetchProtectionStatus();
  });
  