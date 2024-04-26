document.getElementById('protection-button').addEventListener('click', () => {
  const statusText = document.getElementById('status-text');
  const buttonPos = document.getElementById('protection-button');

  if (statusText.textContent === 'Not Protected') {
      statusText.textContent = 'Protected';
      buttonPos.classList.add('checked');
      statusText.style.color = 'green';
      chrome.storage.sync.set({lastProtectionState: 'Protected', color: 'green'});
  } else {
      statusText.textContent = 'Not Protected';
      buttonPos.classList.remove('checked');
      statusText.style.color = 'red';
      chrome.storage.sync.set({lastProtectionState: 'Not Protected', color: 'red'});
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const statusText = document.getElementById('status-text');
  const buttonPos = document.getElementById('protection-button');

  chrome.storage.sync.get(['lastProtectionState', 'color'], function(data) {
    statusText.textContent = data.lastProtectionState;
    if (data.lastProtectionState === 'Protected') {
        buttonPos.classList.add('checked');
    } else {
        buttonPos.classList.remove('checked');
    }
    // Set the color after the text content has been updated
    statusText.style.color = data.color;
  });
});


document.getElementById('stats-button').addEventListener('click', function() {
  window.location.href = 'stats.html';
});

document.getElementById('logout-button').addEventListener('click', function() {
  window.location.href = 'LoginPage.html';
});

document.getElementById('whitelist-button').addEventListener('click', function() {
  window.location.href = 'wl.html';
});

document.getElementById('settings-button').addEventListener('click', function() {
  window.location.href = 'settings.html';
});

function createNotification(message) {
  let options = {
      type: "basic",
      iconUrl: "PhishNET.png", // replace with your icon
      title: "My Notification",
      message: message
  };

  chrome.notifications.create('notificationId', options, function(notificationId) {
      setTimeout(function(){
          chrome.notifications.clear(notificationId);
      }, 5000); // The notification will close after 5 seconds
  });
}
function checkURL(activeTabUrl) {
  // Check the 'status-text' element
  let statusText = document.getElementById('status-text').textContent;
  if (statusText === 'Protected') {
      let data = JSON.stringify({url: activeTabUrl});
      console.log('Data:', data);  // Log the data
      fetch('http://localhost:5000/predict', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: data,
      })
      .then(response => response.json())
      .then(data => {
          let prediction = data.prediction;
          // Update the 'url-stat' text with the prediction
          document.getElementById('url-stat').textContent = prediction;
      })
      .catch((error) => {
          console.error('Error:', error);
      });
  }
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Message received'); // Add this line
  console.log(request.activeTabUrl)
  if (request.activeTabUrl) {
    document.getElementById('url-stat').textContent = prediction;
  }
});