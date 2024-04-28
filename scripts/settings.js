const buttonPos = document.getElementById('not1button');
const button2Pos = document.getElementById('not2button');
const button3Pos = document.getElementById('not3button');

document.getElementById('not1button').addEventListener('click', () => {
    if (buttonPos.classList.contains('checked')) {
        buttonPos.classList.remove('checked');
        chrome.storage.sync.set({not1button: 'disabled'});
    } else {
        buttonPos.classList.add('checked');
        chrome.storage.sync.set({not1button: 'enabled'});
    }
});

document.getElementById('not2button').addEventListener('click', () => {
    if (button2Pos.classList.contains('checked')) {
        button2Pos.classList.remove('checked');
        chrome.storage.sync.set({not2button: 'disabled'});
    } else {
        button2Pos.classList.add('checked');
        chrome.storage.sync.set({not2button: 'enabled'});
    }
});

document.getElementById('not3button').addEventListener('click', () => {
    if (button3Pos.classList.contains('checked')) {
        button3Pos.classList.remove('checked');
        chrome.storage.sync.set({not3button: 'disabled'});
    } else {
        button3Pos.classList.add('checked');
        chrome.storage.sync.set({not3button: 'enabled'});
    }
});


document.getElementById('back-button-stats').addEventListener('click', function() {
    window.location.href = 'PopUp.html';
});
  

document.addEventListener('DOMContentLoaded', () => {
    state = chrome.storage.sync.get('not1button', function(data){
        if (data.not1button === 'enabled') {
            buttonPos.classList.add('checked');
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    state = chrome.storage.sync.get('not2button', function(data){
        if (data.not2button === 'enabled') {
            button2Pos.classList.add('checked');
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    state = chrome.storage.sync.get('not3button', function(data){
        if (data.not3button === 'enabled') {
            button3Pos.classList.add('checked');
        }
    });
});