// Particle Network Background
const canvas = document.getElementById("bg");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];
for (let i = 0; i < 80; i++) {
  particles.push({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    dx: (Math.random() - 0.5) * 0.5,
    dy: (Math.random() - 0.5) * 0.5,
    radius: 2
  });
}

function drawParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "red";

  particles.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    ctx.fill();

    // Move
    p.x += p.dx;
    p.y += p.dy;

    if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
    if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
  });

  // Connect particles
  ctx.strokeStyle = "rgba(255,0,0,0.3)";
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      let dx = particles[i].x - particles[j].x;
      let dy = particles[i].y - particles[j].y;
      let dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 120) {
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.stroke();
      }
    }
  }

  requestAnimationFrame(drawParticles);
}
drawParticles();


// --- System Stats ---
async function updateStats() {
  try {
    const data = await window.pywebview.api.get_system_info();

    document.getElementById("cpu").innerText = data.cpu + " %";
    document.getElementById("ram").innerText = data.ram + " %";
    document.getElementById("disk").innerText = data.disk + " %";
    document.getElementById("battery").innerText = 
        (data.battery !== null ? data.battery + " %" : "N/A");

  } catch (err) {
    console.error("Error fetching system stats:", err);
  }
}

// --- Local Time (separate from stats) ---
function updateLocalTime() {
  const now = new Date();
  const timeStr = now.toLocaleTimeString("en-GB"); // HH:MM:SS
  document.getElementById("time").textContent = "TIME " + timeStr;
}

// Update stats every 2 sec
setInterval(updateStats, 2000);

// Update time every 1 sec
setInterval(updateLocalTime, 1000);
