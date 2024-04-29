document.getElementById('back-button').addEventListener('click', function() {
  window.location.href = 'popup.html';
});

document.getElementById('submit-button').addEventListener('click', function() {
  var url = document.getElementById('whitelist-inp').value;
  addwl(url);
  document.getElementById('whitelist-inp').value = '';
});

document.getElementById('remove-button').addEventListener('click', function() {
  var url = document.getElementById('whitelist-inp').value;
  rmurl(url);
  document.getElementById('whitelist-inp').value = '';
});

function addwl(url) {
  if (!url) {
    alert('URL is empty. Please enter a URL.');
    return;
  }

  
  let urlFormat = /^https?:\/\/www\.[\w.-]+(\.[\w.-]+)+$/;
  if (!urlFormat.test(url)) {
    alert('Invalid input. Please enter a URL in this format:\nhttps://www.google.com');
    return;
  }
  chrome.storage.sync.get('user', function(data) {
    let user = data.user;
    var addedUrl = '';
    fetch('http://localhost:5000/addwl', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({user: user, url: url}),
    })
    .then(response => response.json())
    .then(data => {
        addedUrl = data.final;
        alert(url + ' was added to the Whitelist');
        updateWL();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
  });
  
}

function rmurl(url) {
  if (!url) {
    alert('URL is empty. Please enter a URL.');
    return;
  }

  
  let urlFormat = /^https?:\/\/www\.[\w.-]+(\.[\w.-]+)+$/;
  if (!urlFormat.test(url)) {
    alert('Invalid input. Please enter a URL in this format:\nhttps://www.google.com');
    return;
  }


  chrome.storage.sync.get ('user', function(data) {
    
    let user = data.user;
    fetch('http://localhost:5000/rmwl', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({user: user, url: url}),
    })
    .then(response => response.json())
    .then(data => {
        var rmurl = data.final;
        if (!rmurl){
          alert('Error removing URL');
        }
        alert(url + ' was removed from the Whitelist');
        updateWL();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
  });
}

document.addEventListener("DOMContentLoaded",updateWL())

function updateWL() {

  chrome.storage.sync.get('user', function(data) {
    let user = data.user;
    fetch('http://localhost:5000/test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({user: user}),
    })
    .then(response => response.json())
    .then(user => {
        var wl = user.wltest;
        var wlText = wl.join('\n');
        document.getElementById('wl-list').value = wlText;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
  });
}

