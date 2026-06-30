from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    # Ponemos todo el diseño de la página web dentro de esta variable de Python
    html_content = """
   <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fútbol Cabezones - ¡Poderes y Goles!</title>
    <style>
        body {
            margin: 0; padding: 0; background: radial-gradient(circle, #1a2a40, #0a0f18);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100vh; color: white; overflow: hidden;
        }
        h1 { margin: 0 0 10px 0; text-shadow: 0px 4px 10px rgba(0, 191, 255, 0.6); font-size: 32px; text-transform: uppercase; letter-spacing: 3px; }
        #top-bar {
            display: flex; align-items: center; justify-content: center; gap: 20px;
            margin-bottom: 15px; background: linear-gradient(180deg, #333, #111);
            padding: 10px 40px; border-radius: 15px; border: 2px solid #555; box-shadow: 0 8px 15px rgba(0,0,0,0.8);
        }
        .score-team { font-size: 26px; font-weight: 900; width: 120px; text-align: center; text-shadow: 2px 2px 0px #000; }
        .score-number { font-size: 36px; font-weight: bold; padding: 0 20px; text-shadow: 0 0 10px rgba(255,255,255,0.5); }
        #timer-box {
            background: linear-gradient(180deg, #ffea00, #b3a400); color: #000;
            padding: 5px 20px; border-radius: 8px; font-size: 26px; font-weight: 900;
            border: 2px solid #fff; box-shadow: inset 0 0 5px rgba(0,0,0,0.5);
        }
        #game-container { position: relative; }
        canvas { border: 5px solid #bdc3c7; box-shadow: 0px 15px 40px rgba(0,0,0,0.9); border-radius: 12px; background: #000; }
        .overlay {
            position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(5px);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            border-radius: 12px; z-index: 10;
        }
        .menu-box {
            background: linear-gradient(135deg, rgba(40,40,40,0.9), rgba(20,20,20,0.9));
            padding: 40px; border-radius: 15px; border: 2px solid rgba(255,255,255,0.2);
            text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        }
        .menu-box h2 { margin-top: 0; color: #f1c40f; text-shadow: 2px 2px 0 #000; }
        select { padding: 12px; font-size: 16px; margin: 10px; border-radius: 8px; background: #ecf0f1; font-weight: bold; cursor: pointer; }
        button {
            padding: 15px 30px; font-size: 18px; font-weight: bold; background: linear-gradient(180deg, #2ecc71, #27ae60);
            color: white; border: 2px solid #2ecc71; border-radius: 8px; cursor: pointer; margin-top: 20px; text-transform: uppercase;
        }
        button:hover { transform: scale(1.05); box-shadow: 0 0 15px rgba(46, 204, 113, 0.6); }
        .controls-hint { margin-top: 20px; display: flex; gap: 50px; font-size: 14px; background: rgba(255,255,255,0.05); padding: 12px 25px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); }
    </style>
</head>
<body>

    <h1>🏆 Fútbol Cabezones HD 🏆</h1>
    
    <div id="top-bar">
        <div class="score-team" id="name1" style="color: #ff4d4d;">P1</div>
        <div class="score-number" id="score1">0</div>
        <div id="timer-box">90</div>
        <div class="score-number" id="score2">0</div>
        <div class="score-team" id="name2" style="color: #3399ff;">P2</div>
    </div>
    
    <div id="game-container">
        <canvas id="gameCanvas" width="800" height="400"></canvas>
        
        <div id="menu-overlay" class="overlay">
            <div class="menu-box">
                <h2>SELECCIONA TU EQUIPO</h2>
                <div>
                    <label style="color: #ff6b6b; font-weight: bold; font-size: 18px;">Jugador 1:</label>
                    <select id="team1-select"></select>
                </div>
                <div style="margin-top: 15px;">
                    <label style="color: #48dbfb; font-weight: bold; font-size: 18px;">Jugador 2:</label>
                    <select id="team2-select"></select>
                </div>
                <button onclick="startGame()">¡JUGAR PARTIDO!</button>
            </div>
        </div>

        <div id="game-over-overlay" class="overlay" style="display: none;">
            <div class="menu-box">
                <h2 id="winner-text" style="font-size: 36px; color: #f1c40f;">¡TIEMPO FINALIZADO!</h2>
                <button onclick="showMenu()">Volver al Menú</button>
            </div>
        </div>
    </div>

    <div class="controls-hint">
        <div><strong style="color:#ff6b6b">P1:</strong> A / D (Mover) | W (Saltar) | <b style="color:#f1c40f">ESPACIO (Patear)</b></div>
        <div><strong style="color:#48dbfb">P2:</strong> ← / → (Mover) | ↑ (Saltar) | <b style="color:#f1c40f">↓ (Patear)</b></div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const teams = {
            "Ecuador": ["#ffdd00", "#002366", "#ed1c24"], "Argentina": ["#75AADB", "#ffffff", "#75AADB"],
            "Brasil": ["#009c3b", "#ffdf00", "#002776"], "España": ["#aa151b", "#f1bf00", "#aa151b"],
            "Francia": ["#002395", "#ffffff", "#ed2939"], "Alemania": ["#000000", "#dd0000", "#ffce00"],
            "México": ["#006847", "#ffffff", "#ce1126"], "Italia": ["#009246", "#ffffff", "#ce2b37"]
        };

        const select1 = document.getElementById("team1-select");
        const select2 = document.getElementById("team2-select");
        for(let t in teams) {
            select1.innerHTML += `<option value="${t}">${t}</option>`; select2.innerHTML += `<option value="${t}">${t}</option>`;
        }
        select1.value = "Ecuador"; select2.value = "Brasil";

        let gameState = "menu"; // menu, playing, gameover
        let timeLeft = 90; let lastTime = 0;
        let score1 = 0; let score2 = 0;
        let goalTimer = 0; let lastScorer = 0;

        const gravity = 0.65; const friction = 0.82; const groundY = 340; 
        const goalWidth = 65; const goalHeight = 145;

        // Base de jugadores
        class Player {
            constructor(x, colorTheme) {
                this.x = x; this.y = 200; this.vx = 0; this.vy = 0; this.radius = 40;
                this.isGrounded = false; this.baseSpeed = 6.5; this.baseJump = 13;
                this.speed = 6.5; this.jumpForce = 13;
                this.faceRight = (x < 400); this.isKicking = false; this.kickTimer = 0;
                this.team = colorTheme; this.powerTimer = 0; this.activePower = null;
            }
        }

        const p1 = new Player(180, teams["Ecuador"]);
        const p2 = new Player(620, teams["Brasil"]);
        
        const ball = { x: 400, y: 100, vx: 0, vy: 0, baseRadius: 15, radius: 15, rotation: 0, powerTimer: 0 };
        let powerUps = [];

        const POWER_TYPES = [
            { type: 'SPEED', emoji: '⚡', color: '#f1c40f' },
            { type: 'JUMP', emoji: '🦘', color: '#2ecc71' },
            { type: 'FREEZE', emoji: '🧊', color: '#3498db' },
            { type: 'GIANT', emoji: '⚽', color: '#e74c3c' }
        ];

        const keys = {};
        window.addEventListener("keydown", e => { keys[e.code] = true; if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) e.preventDefault(); });
        window.addEventListener("keyup", e => keys[e.code] = false);

        function showMenu() {
            gameState = "menu";
            document.getElementById("game-over-overlay").style.display = "none"; document.getElementById("menu-overlay").style.display = "flex";
        }

        function startGame() {
            p1.team = teams[select1.value]; p2.team = teams[select2.value];
            document.getElementById("name1").innerText = select1.value.substring(0,3).toUpperCase();
            document.getElementById("name2").innerText = select2.value.substring(0,3).toUpperCase();
            score1 = 0; score2 = 0; timeLeft = 90; powerUps = []; goalTimer = 0;
            updateScoreUI(); document.getElementById("menu-overlay").style.display = "none";
            resetPositions(1); gameState = "playing"; lastTime = Date.now();
        }

        function endGame() {
            gameState = "gameover";
            let t = score1 > score2 ? `${select1.value.toUpperCase()} GANA!` : score2 > score1 ? `${select2.value.toUpperCase()} GANA!` : "¡EMPATE!";
            document.getElementById("winner-text").innerText = t; document.getElementById("game-over-overlay").style.display = "flex";
        }

        function updateScoreUI() {
            document.getElementById("score1").innerText = score1; document.getElementById("score2").innerText = score2; document.getElementById("timer-box").innerText = timeLeft;
        }

        function resetPositions(scorer) {
            p1.x = 180; p1.y = groundY - p1.radius; p1.vx = 0; p1.vy = 0; p1.activePower = null; p1.powerTimer = 0;
            p2.x = 620; p2.y = groundY - p2.radius; p2.vx = 0; p2.vy = 0; p2.activePower = null; p2.powerTimer = 0;
            ball.x = 400; ball.y = 100; ball.vx = scorer === 1 ? -3 : 3; ball.vy = -6; ball.radius = ball.baseRadius; ball.powerTimer = 0; ball.rotation = 0;
            powerUps = []; goalTimer = 0;
        }

        function triggerGoal(scorer) {
            lastScorer = scorer;
            goalTimer = 100; // Unos segundos de celebración
        }

        function spawnPowerUp() {
            if(powerUps.length >= 2) return; // Máximo 2 en pantalla
            let type = POWER_TYPES[Math.floor(Math.random() * POWER_TYPES.length)];
            let xPos = Math.random() * (canvas.width - 200) + 100; // Evitar que caigan en los arcos
            powerUps.push({ x: xPos, y: -30, vy: 0, radius: 20, ...type });
        }

        function applyPower(player, opponent, pu) {
            if (pu.type === 'GIANT') {
                ball.radius = 35; ball.powerTimer = 400; // Balón gigante
            } else {
                player.activePower = pu.type;
                player.powerTimer = 350; // Duración del poder
                if (pu.type === 'FREEZE') {
                    opponent.activePower = 'FROZEN';
                    opponent.powerTimer = 200; // Congelado por menos tiempo
                }
            }
        }

        function update() {
            if (gameState !== "playing") return;

            // Lógica de "GOOOL"
            if (goalTimer > 0) {
                goalTimer--;
                if (goalTimer === 1) resetPositions(lastScorer);
                return; // Pausar físicas
            }

            // Reloj
            let now = Date.now();
            if (now - lastTime >= 1000) {
                timeLeft--; lastTime = now; document.getElementById("timer-box").innerText = timeLeft;
                if (timeLeft <= 0) endGame();
            }

            // --- GESTIÓN DE PODERES ---
            if (Math.random() < 0.004) spawnPowerUp(); // Spawn aleatorio

            // Resetear stats de jugadores
            [p1, p2].forEach(p => {
                p.speed = p.baseSpeed; p.jumpForce = p.baseJump;
                if(p.powerTimer > 0) {
                    p.powerTimer--;
                    if (p.activePower === 'SPEED') p.speed = 12;
                    if (p.activePower === 'JUMP') p.jumpForce = 20;
                    if (p.activePower === 'FROZEN') { p.speed = 0; p.jumpForce = 0; p.vx = 0; }
                    if (p.powerTimer <= 0) p.activePower = null;
                }
            });

            // Gestón poder del balón
            if(ball.powerTimer > 0) {
                ball.powerTimer--;
                if(ball.powerTimer <= 0) ball.radius = ball.baseRadius;
            }

            // Mover y recolectar cajas de poder
            for(let i = powerUps.length - 1; i >= 0; i--) {
                let pu = powerUps[i];
                pu.vy += gravity * 0.5; pu.y += pu.vy;
                if (pu.y > groundY - pu.radius) pu.y = groundY - pu.radius;

                let d1 = Math.sqrt((p1.x - pu.x)**2 + (p1.y - pu.y)**2);
                let d2 = Math.sqrt((p2.x - pu.x)**2 + (p2.y - pu.y)**2);

                if (d1 < p1.radius + pu.radius) { applyPower(p1, p2, pu); powerUps.splice(i, 1); continue; }
                if (d2 < p2.radius + pu.radius) { applyPower(p2, p1, pu); powerUps.splice(i, 1); continue; }
            }

            // Controles P1 (Ignorar si está congelado)
            if (p1.activePower !== 'FROZEN') {
                if (keys["KeyA"]) { p1.vx = -p1.speed; p1.faceRight = false; }
                else if (keys["KeyD"]) { p1.vx = p1.speed; p1.faceRight = true; }
                else p1.vx *= friction;
                if (keys["KeyW"] && p1.isGrounded) { p1.vy = -p1.jumpForce; p1.isGrounded = false; }
                if (keys["Space"] && !p1.isKicking) { p1.isKicking = true; p1.kickTimer = 12; }
            }

            // Controles P2
            if (p2.activePower !== 'FROZEN') {
                if (keys["ArrowLeft"]) { p2.vx = -p2.speed; p2.faceRight = false; }
                else if (keys["ArrowRight"]) { p2.vx = p2.speed; p2.faceRight = true; }
                else p2.vx *= friction;
                if (keys["ArrowUp"] && p2.isGrounded) { p2.vy = -p2.jumpForce; p2.isGrounded = false; }
                if (keys["ArrowDown"] && !p2.isKicking) { p2.isKicking = true; p2.kickTimer = 12; }
            }

            // Físicas Jugadores
            [p1, p2].forEach(p => {
                if (p.isKicking) { p.kickTimer--; if (p.kickTimer <= 0) p.isKicking = false; }
                p.vy += gravity; p.x += p.vx; p.y += p.vy;

                if (p.y + p.radius > groundY) { p.y = groundY - p.radius; p.vy = 0; p.isGrounded = true; }
                if (p.x - p.radius < goalWidth) p.x = goalWidth + p.radius;
                if (p.x + p.radius > canvas.width - goalWidth) p.x = canvas.width - goalWidth - p.radius;
            });

            // Físicas Balón
            // Si el balón es gigante, es un poco más pesado
            let ballGrav = ball.radius > 20 ? gravity * 0.8 : gravity * 0.65;
            ball.vy += ballGrav; 
            ball.x += ball.vx; ball.y += ball.vy;
            ball.rotation += ball.vx * (ball.radius > 20 ? 0.02 : 0.05);

            if (ball.y + ball.radius > groundY) { ball.y = groundY - ball.radius; ball.vy = -ball.vy * 0.75; ball.vx *= 0.97; }
            if (ball.y - ball.radius < 0) { ball.y = ball.radius; ball.vy = -ball.vy * 0.75; }

            // Rebote Largueros
            if (ball.x - ball.radius <= goalWidth && ball.y >= groundY - goalHeight - 5 && ball.y <= groundY - goalHeight + 5) {
                ball.vy = -Math.abs(ball.vy) * 0.8; ball.y = groundY - goalHeight - ball.radius;
            }
            if (ball.x + ball.radius >= canvas.width - goalWidth && ball.y >= groundY - goalHeight - 5 && ball.y <= groundY - goalHeight + 5) {
                ball.vy = -Math.abs(ball.vy) * 0.8; ball.y = groundY - goalHeight - ball.radius;
            }

            // --- DETECCIÓN DE GOLES ---
            if (ball.x < goalWidth && ball.y > groundY - goalHeight + ball.radius) { score2++; updateScoreUI(); triggerGoal(2); return; }
            if (ball.x > canvas.width - goalWidth && ball.y > groundY - goalHeight + ball.radius) { score1++; updateScoreUI(); triggerGoal(1); return; }

            if (ball.x - ball.radius < 0) { ball.x = ball.radius; ball.vx = -ball.vx * 0.75; }
            if (ball.x + ball.radius > canvas.width) { ball.x = canvas.width - ball.radius; ball.vx = -ball.vx * 0.75; }

            // Colisiones Jugador vs Balón
            [p1, p2].forEach(p => {
                let dx = ball.x - p.x; let dy = ball.y - p.y; let dist = Math.sqrt(dx * dx + dy * dy);

                if (p.isKicking) {
                    let footX = p.x + (p.faceRight ? 35 : -35); let footY = p.y + p.radius - 5;
                    let fDist = Math.sqrt((ball.x - footX)**2 + (ball.y - footY)**2);
                    
                    if (fDist < p.radius + ball.radius) {
                        let kickPower = ball.radius > 20 ? 12 : 16; // Cuesta más patear la bola gigante
                        ball.vx = p.faceRight ? kickPower : -kickPower; ball.vy = -9;
                        p.isKicking = false; return;
                    }
                }

                if (dist < p.radius + ball.radius) {
                    let nx = dx / dist, ny = dy / dist;
                    ball.x = p.x + nx * (p.radius + ball.radius); ball.y = p.y + ny * (p.radius + ball.radius);
                    let speed = Math.min(Math.sqrt(ball.vx * ball.vx + ball.vy * ball.vy) + 1.5, 13);
                    ball.vx = nx * speed + p.vx * 0.5; ball.vy = ny * speed + p.vy * 0.5;
                }
            });
        }

        // --- FUNCIONES DE DIBUJADO ---
        function drawStadium() {
            let sky = ctx.createLinearGradient(0, 0, 0, groundY); sky.addColorStop(0, "#0b1b36"); sky.addColorStop(1, "#1e437a");
            ctx.fillStyle = sky; ctx.fillRect(0, 0, canvas.width, groundY);
            ctx.fillStyle = "#0a111a"; ctx.fillRect(0, groundY - 200, canvas.width, 200);
            
            for (let i = 0; i < 400; i++) {
                let px = (Math.sin(i * 98) * 0.5 + 0.5) * canvas.width;
                let py = (Math.cos(i * 45) * 0.5 + 0.5) * 180 + (groundY - 190);
                ctx.fillStyle = i % 4 === 0 ? "#f1c40f" : (i % 3 === 0 ? "#e74c3c" : "#ecf0f1");
                ctx.globalAlpha = Math.random() * 0.5 + 0.5;
                ctx.beginPath(); ctx.arc(px, py, 1.5, 0, Math.PI*2); ctx.fill();
            }
            ctx.globalAlpha = 1.0;
            ctx.fillStyle = "rgba(255, 255, 255, 0.08)";
            ctx.beginPath(); ctx.moveTo(50, 0); ctx.lineTo(350, groundY); ctx.lineTo(-100, groundY); ctx.fill();
            ctx.beginPath(); ctx.moveTo(750, 0); ctx.lineTo(900, groundY); ctx.lineTo(450, groundY); ctx.fill();

            for (let i = 0; i < canvas.width; i += 50) {
                ctx.fillStyle = (i / 50) % 2 === 0 ? "#1d8a2a" : "#229e31"; ctx.fillRect(i, groundY, 50, canvas.height - groundY);
            }
            ctx.fillStyle = "rgba(255,255,255,0.85)"; ctx.fillRect(canvas.width / 2 - 3, groundY, 6, canvas.height - groundY);
            ctx.fillRect(0, groundY, canvas.width, 4); 
        }

        function drawGoal(isLeft) {
            ctx.fillStyle = "rgba(0,0,0,0.3)"; ctx.fillRect(isLeft ? 10 : canvas.width - goalWidth - 10, groundY, goalWidth, 10);
            ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"; ctx.lineWidth = 1;
            let startX = isLeft ? 0 : canvas.width - goalWidth;
            for (let i = groundY - goalHeight; i <= groundY; i += 12) { ctx.beginPath(); ctx.moveTo(startX, i); ctx.lineTo(startX + goalWidth, i); ctx.stroke(); }
            for (let i = startX; i <= startX + goalWidth; i += 12) { ctx.beginPath(); ctx.moveTo(i, groundY - goalHeight); ctx.lineTo(i, groundY); ctx.stroke(); }

            let grad = ctx.createLinearGradient(startX, 0, startX + 10, 0); grad.addColorStop(0, "#ffffff"); grad.addColorStop(1, "#aaaaaa");
            ctx.strokeStyle = grad; ctx.lineWidth = 8; ctx.lineCap = "round"; ctx.beginPath();
            if (isLeft) { ctx.moveTo(0, groundY - goalHeight); ctx.lineTo(goalWidth, groundY - goalHeight); ctx.lineTo(goalWidth, groundY); } 
            else { ctx.moveTo(canvas.width, groundY - goalHeight); ctx.lineTo(canvas.width - goalWidth, groundY - goalHeight); ctx.lineTo(canvas.width - goalWidth, groundY); }
            ctx.stroke();
        }

        function drawCabezon(p) {
            ctx.fillStyle = "rgba(0,0,0,0.4)"; ctx.beginPath(); ctx.ellipse(p.x, groundY, p.radius * 0.8, p.radius * 0.2, 0, 0, Math.PI * 2); ctx.fill(); // Sombra

            ctx.save();
            ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2); ctx.clip();
            
            // Si está congelado, pintar de azul celeste
            if(p.activePower === 'FROZEN') {
                ctx.fillStyle = "#81ecec"; ctx.fillRect(p.x - p.radius, p.y - p.radius, p.radius * 2, p.radius * 2);
            } else {
                ctx.fillStyle = "#f1c27d"; ctx.fillRect(p.x - p.radius, p.y - p.radius, p.radius * 2, p.radius * 2);
                ctx.fillStyle = "#3e2723"; ctx.fillRect(p.x - p.radius, p.y - p.radius, p.radius * 2, p.radius * 0.4);
                let jerseyY = p.y + p.radius * 0.1; let bandHeight = (p.radius * 0.9) / p.team.length;
                for(let i=0; i < p.team.length; i++) { ctx.fillStyle = p.team[i]; ctx.fillRect(p.x - p.radius, jerseyY + (bandHeight * i), p.radius * 2, bandHeight + 1); }
            }
            ctx.restore();

            ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2); ctx.lineWidth = 3; ctx.strokeStyle = "#111"; ctx.stroke();
            
            // Ojos
            ctx.beginPath(); let eyeOffsetX = p.faceRight ? 12 : -12; ctx.arc(p.x + eyeOffsetX, p.y - 8, 7, 0, Math.PI * 2); ctx.fillStyle = "#fff"; ctx.fill(); ctx.stroke();
            ctx.beginPath(); let pupilOffsetX = p.faceRight ? 15 : -15; ctx.arc(p.x + pupilOffsetX, p.y - 8, 3, 0, Math.PI * 2); ctx.fillStyle = "#000"; ctx.fill();
            
            // Sonrisa o Cara Congelada
            ctx.beginPath();
            let faceX = p.faceRight ? 12 : -12;
            if(p.activePower === 'FROZEN') {
                ctx.arc(p.x + faceX, p.y + 8, 3, 0, Math.PI * 2, false); ctx.fillStyle = "#fff"; ctx.fill(); // Boca abierta de frío
            } else {
                ctx.arc(p.x + faceX, p.y + 5, 5, 0, Math.PI, false); ctx.strokeStyle = "#000"; ctx.lineWidth = 2; ctx.stroke();
            }

            // Botín
            ctx.beginPath(); let footBaseX = p.faceRight ? 10 : -34; if (p.isKicking) footBaseX += p.faceRight ? 24 : -24;
            ctx.roundRect(p.x + footBaseX, p.y + p.radius - 2, 24, 14, 7);
            ctx.fillStyle = p.activePower === 'FROZEN' ? "#00cec9" : p.team[0]; 
            ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = "#111"; ctx.stroke();

            // Icono de poder activo flotando arriba
            if(p.activePower && p.activePower !== 'FROZEN') {
                ctx.font = "20px Arial";
                let emoji = POWER_TYPES.find(pw => pw.type === p.activePower).emoji;
                ctx.fillText(emoji, p.x - 10, p.y - p.radius - 10);
            }
        }

        function drawBall() {
            ctx.fillStyle = "rgba(0,0,0,0.4)"; ctx.beginPath(); ctx.ellipse(ball.x, groundY, ball.radius * 0.8, ball.radius * 0.2, 0, 0, Math.PI * 2); ctx.fill();
            ctx.save(); ctx.translate(ball.x, ball.y); ctx.rotate(ball.rotation);
            ctx.beginPath(); ctx.arc(0, 0, ball.radius, 0, Math.PI * 2);
            ctx.fillStyle = ball.radius > 20 ? "#ffcccc" : "#f5f6fa"; // Se pone roja si es gigante
            ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = "#2f3640"; ctx.stroke();
            
            ctx.fillStyle = "#2f3640"; ctx.beginPath();
            for(let i=0; i<5; i++) {
                let angle = i * (Math.PI * 2 / 5) - Math.PI/2;
                let px = Math.cos(angle) * ball.radius * 0.4; let py = Math.sin(angle) * ball.radius * 0.4;
                if(i===0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
            }
            ctx.closePath(); ctx.fill();

            for(let i=0; i<5; i++) {
                let angle = i * (Math.PI * 2 / 5) - Math.PI/2;
                ctx.beginPath(); ctx.moveTo(Math.cos(angle) * ball.radius * 0.4, Math.sin(angle) * ball.radius * 0.4);
                ctx.lineTo(Math.cos(angle) * ball.radius, Math.sin(angle) * ball.radius); ctx.stroke();
            }
            ctx.restore();
        }

        function drawPowerUps() {
            powerUps.forEach(pu => {
                ctx.fillStyle = pu.color;
                ctx.beginPath(); ctx.roundRect(pu.x - pu.radius, pu.y - pu.radius, pu.radius*2, pu.radius*2, 5); ctx.fill();
                ctx.lineWidth = 2; ctx.strokeStyle = "#fff"; ctx.stroke();
                ctx.font = "24px Arial"; ctx.fillStyle = "#fff"; ctx.fillText(pu.emoji, pu.x - 12, pu.y + 8);
            });
        }

        function drawGoalCelebration() {
            if (goalTimer > 0) {
                ctx.save();
                ctx.translate(canvas.width / 2, canvas.height / 2 - 50);
                
                // Animación de pulso
                let scale = 1 + Math.sin(goalTimer * 0.2) * 0.15;
                ctx.scale(scale, scale);

                ctx.font = "bold 70px Impact";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";

                // Contorno y sombra
                ctx.lineWidth = 8;
                ctx.strokeStyle = "#000";
                ctx.strokeText("¡GOOOOOOOL!", 0, 0);

                // Relleno con degradado
                let grad = ctx.createLinearGradient(0, -30, 0, 30);
                grad.addColorStop(0, "#ffea00");
                grad.addColorStop(1, "#ff5e00");
                ctx.fillStyle = grad;
                ctx.fillText("¡GOOOOOOOL!", 0, 0);

                ctx.restore();
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawStadium();
            drawGoal(true); drawGoal(false);

            if(gameState === "playing" || gameState === "gameover") {
                drawPowerUps();
                drawCabezon(p1);
                drawCabezon(p2);
                drawBall();
                drawGoalCelebration();
            }
        }

        function gameLoop() { update(); draw(); requestAnimationFrame(gameLoop); }
        gameLoop();
    </script>
</body>
</html>
    """
    return html_content
