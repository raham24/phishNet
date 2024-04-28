document.getElementById('back-button-stats').addEventListener('click', function() {
    window.location.href = 'popup.html';
});

document.addEventListener("DOMContentLoaded",showPieChart)
document.addEventListener("DOMContentLoaded",updatestats())
document.addEventListener("DOMContentLoaded",updatelist())


function updatestats() {
  let safe = 0;
  let phish = 0;
  let user = 2;
  
  fetch('http://localhost:5000/getsafe', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({user: user}),
  })
  .then(response => response.json())
  .then(data => {
      safe = data.safe;
      phish = data.phish;
      showPieChart(safe,phish);
  })
  .catch((error) => {
      console.error('Error:', error);
  });

} 

function updatelist() {
  let user = 2;
  fetch('http://localhost:5000/updatelist', {
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
      document.getElementById('stat-list').value = wlText;
  })
  .catch((error) => {
      console.error('Error:', error);
  });
}

function showPieChart(safe,phish) {

  let sliceA={size: safe, color: "green"};
  let sliceB={size: phish, color: "red"};

  const values = [sliceA.size, sliceB.size];

  const total = values.reduce((acc,val)=> acc+val, 0);

  let startAngle = 0;

  const canvas = document.getElementById("pie-chart");
  const ctx = canvas.getContext("2d");
  
  const radius = canvas.width / 2.5; 
  const centerX = canvas.width / 2.5; 

  values.forEach((value,index) => {
    const angle=(value/total) * Math.PI * 2;

    //actual drawing
    ctx.beginPath();
    ctx.moveTo(centerX, canvas.height / 2);
    ctx.arc(
      centerX,
      canvas.height / 2,
      radius,
      startAngle,
      startAngle + angle
    );
    ctx.closePath();
    ctx.fillStyle = index === 0 ? sliceA.color : sliceB.color;
    ctx.fill();

    startAngle += angle;
  });
}
