document.getElementById('back-button-stats').addEventListener('click', function() {
    window.location.href = 'popup.html';
});

document.addEventListener("DOMContentLoaded",showPieChart)

let safe = 10;
let phish = 1;

function showPieChart() {
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
