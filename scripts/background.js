let activeTabId = null;

chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({lastProtectionState: 'Not Protected'});
});

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({phishingNotification: 'enabled'});
});

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({safeNotification: 'enabled'});
});

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({wlNotification: 'enabled'});
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
        createNotification(prediction);
    })
    .catch((error) => {
        console.error('Error:', error);
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


