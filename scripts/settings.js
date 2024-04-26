const buttonPos = document.getElementById('not1-button');
const button2Pos = document.getElementById('not2-button');
const button3Pos = document.getElementById('not3-button');
  

document.getElementById('not1-button').addEventListener('click', () => {
    if (buttonPos.classList.contains('checked')) {
        buttonPos.classList.remove('checked');
    } else {
        buttonPos.classList.add('checked');
    }
});

document.getElementById('not2-button').addEventListener('click', () => {
    if (button2Pos.classList.contains('checked')) {
        button2Pos.classList.remove('checked');
    } else {
        button2Pos.classList.add('checked');
    }
});

document.getElementById('not3-button').addEventListener('click', () => {
    if (button3Pos.classList.contains('checked')) {
        button3Pos.classList.remove('checked');
    } else {
        button3Pos.classList.add('checked');
    }
});


document.getElementById('back-button-stats').addEventListener('click', function() {
    window.location.href = 'PopUp.html';
});
  