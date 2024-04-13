chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({lastProtectionState: 'Not Protected'});
  });