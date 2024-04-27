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


  console.log(url);
  let user = 2;
  fetch('http://localhost:5000/addwl', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({user: user, url: url}),
  })
  .then(response => response.json())
  .then(data => {
      var addedUrl = data.addwl;
  })
  .catch((error) => {
      console.error('Error:', error);
  });
  console.log('URL added to whitelist:', url);
  alert("URL whitelisted!");
  updateWL();
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


  console.log(url);
  let user = 2;
  fetch('http://localhost:5000/rmwl', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({user: user, url: url}),
  })
  .then(response => response.json())
  .then(data => {
      var rmurl = data.rmwl;
      if (!rmurl){
        alert('Error removing URL');
      }
      alert(rmurl + ' was removed from the Whitelist');
      console.log(data);
  })
  .catch((error) => {
      console.error('Error:', error);
  });
  console.log('URL removed from the whitelist:', url);
  updateWL();
}

document.addEventListener("DOMContentLoaded",updateWL())

function updateWL() {
  let user = 2;
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
      wl.forEach(item => {
          console.log(item); // item is a string
      });
      var wlText = wl.join('\n');
      document.getElementById('wl-list').value = wlText;
  })
  .catch((error) => {
      console.error('Error:', error);
  });
}

