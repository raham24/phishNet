let activeTabId = null;

chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({lastProtectionState: 'Not Protected'});
});

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({not1button: 'enabled'});
});

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({not2button: 'enabled'});
});

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({not3button: 'enabled'});
});

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({user: '1'});
});


chrome.tabs.onActivated.addListener(activeInfo => {
  activeTabId = activeInfo.tabId;
  chrome.tabs.get(activeTabId, tab => {
    activeTabUrl = tab.url;
    console.log(`Tab changed: ${activeTabUrl}`);
    checkLastProtectionState().then((isProtected) => {
        if (isProtected) {
            checkURL(activeTabUrl);
        }
      });
  });
});


chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (tabId === activeTabId && changeInfo.url) {
    activeTabUrl = changeInfo.url;
    console.log(`URL changed: ${activeTabUrl}`);
    checkLastProtectionState().then((isProtected) => {
        if (isProtected) {
          checkURL(activeTabUrl);
        }
      });
  }
});


function checkLastProtectionState() {
    return new Promise((resolve, reject) => {
      chrome.storage.sync.get('lastProtectionState', (result) => {
        if (chrome.runtime.lastError) {
          reject(chrome.runtime.lastError);
        } else {
          const lastProtectionState = result['lastProtectionState'];
          if (lastProtectionState === 'Protected') {
            resolve(true);
          } else {
            resolve(false);
          }
        }
      });
    });
}


function checkURL(activeTabUrl) {

  chrome.storage.sync.get('user', function(data) {
      let user_id = data.user;
      let Data = JSON.stringify({url: activeTabUrl, user: user_id});
      console.log('Data:', Data);  // Log the data
      console.log('User:', );  // Log the data
      fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: Data,
    })
    .then(response => response.json())
    .then(Data => {
        let prediction = Data.prediction;
        if (prediction === "Website Whitelisted") {
          chrome.storage.sync.get('not1button', function(Data) {
            if (Data.not1button === "enabled") {
              createNotification(prediction);
            }
          });
        }
        if (prediction === "Phishing Website") {
          chrome.storage.sync.get('not2button', function(Data) {
            if (Data.not2button === "enabled") {
              createNotification(prediction);
            }
          });
        }
        if (prediction === "Safe Website") {
          chrome.storage.sync.get('not3button', function(Data) {
            if (Data.not3button === "enabled") {
              createNotification(prediction);
            }
          });
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    });
    
}

function createNotification(message) {
    let options = {
        type: "basic",
        iconUrl: "PhishNET.png",
        title: "My Notification",
        message: message
    };

    chrome.notifications.create('notificationId', options, function(notificationId) {
        setTimeout(function(){
            chrome.notifications.clear(notificationId);
        }, 5000); // The notification will close after 5 seconds
    });
}


