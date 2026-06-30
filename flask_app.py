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
    <title>Fútbol Cabezones - Gráficos HD</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: radial-gradient(circle, #1a2a40, #0a0f18);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            color: white;
            overflow: hidden;
        }
        h1 {
            margin: 0 0 10px 0;
            text-shadow: 0px 4px 10px rgba(0, 191, 255, 0.6);
            font-size: 32px;
            text-transform: uppercase;
            letter-spacing: 3px;
        }
        #top-bar {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 15px;
            background: linear-gradient(180deg, #333, #111);
            padding: 10px 40px;
            border-radius: 15px;
            border: 2px solid #555;
            box-shadow: 0 8px 15px rgba(0,0,0,0.8);
        }
        .score-team { font-size: 26px; font-weight: 900; width: 120px; text-align: center; text-shadow: 2px 2px 0px #000; }
        .score-number { font-size: 36px; font-weight: bold; padding: 0 20px; text-shadow: 0 0 10px rgba(255,255,255,0.5); }
        #timer-box {
            background: linear-gradient(180deg, #ffea00, #b3a400);
            color: #000;
            padding: 5px 20px;
            border-radius: 8px;
            font-size: 26px;
            font-weight: 900;
            border: 2px solid #fff;
            box-shadow: inset 0 0 5px rgba(0,0,0,0.5);
        }
        
        #game-container {
            position: relative;
        }
        canvas {
            border: 5px solid #bdc3c7;
            box-shadow: 0px 15px 40px rgba(0,0,0,0.9);
            border-radius: 12px;
            background: #000; 
        }

        /* Menús Superpuestos con Glassmorphism */
        .overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(5px);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            z-index: 10;
        }
        .menu-box {
            background: linear-gradient(135deg, rgba(40,40,40,0.9), rgba(20,20,20,0.9));
            padding: 40px;
            border-radius: 15px;
            border: 2px solid rgba(255,255,255,0.2);
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        }
        .menu-box h2 {
            margin-top: 0;
            color: #f1c40f;
            text-shadow: 2px 2px 0 #000;
        }
        select {
            padding: 12px;
            font-size: 16px;
            margin: 10px;
            border-radius: 8px;
            background: #ecf0f1;
            color: #2c3e50;
            font-weight: bold;
            border: 2px solid #bdc3c7;
            cursor: pointer;
        }
        button {
            padding: 15px 30px;
            font-size: 18px;
            font-weight: bold;
            background: linear-gradient(180deg, #2ecc71, #27ae60);
            color: white;
            border: 2px solid #2ecc71;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 20px;
            transition: 0.2s;
            text-transform: uppercase;
        }
        button:hover { 
            transform: scale(1.05); 
            box-shadow: 0 0 15px rgba(46, 204, 113, 0.6);
        }

        .controls-hint {
            margin-top: 20px;
            display: flex;
            gap: 50px;
            font-size: 14px;
            background: rgba(255,255,255,0.05);
            padding: 12px 25px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
        }
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
        <div><strong style="color:#ff6b6b">P1 (Izq):</strong> A / D (Mover) | W (Saltar) | <b style="color:#f1c40f">ESPACIO (Patear)</b></div>
        <div><strong style="color:#48dbfb">P2 (Der):</strong> ← / → (Mover) | ↑ (Saltar) | <b style="color:#f1c40f">↓ (Patear)</b></div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // --- DATOS DE SELECCIONES (Soporte Multicolores/Tricolor) ---
        const teams = {
            "Ecuador": ["#ffdd00", "#002366", "#ed1c24"],
            "Argentina": ["#75AADB", "#ffffff", "#75AADB"],
            "Brasil": ["#009c3b", "#ffdf00", "#002776"],
            "España": ["#aa151b", "#f1bf00", "#aa151b"],
            "Francia": ["#002395", "#ffffff", "#ed2939"],
            "Alemania": ["#000000", "#dd0000", "#ffce00"],
            "México": ["#006847", "#ffffff", "#ce1126"],
            "Italia": ["#009246", "#ffffff", "#ce2b37"]
        };

        const select1 = document.getElementById("team1-select");
        const select2 = document.getElementById("team2-select");
        for(let t in teams) {
            select1.innerHTML += `<option value="${t}">${t}</option>`;
            select2.innerHTML += `<option value="${t}">${t}</option>`;
        }
        select1.value = "Ecuador";
        select2.value = "Brasil";

        // --- ESTADO DEL JUEGO ---
        let gameState = "menu";
        let timeLeft = 90;
        let lastTime = 0;
        let score1 = 0;
        let score2 = 0;

        const gravity = 0.65;
        const friction = 0.82;
        const groundY = 340; 
        const goalWidth = 65;
        const goalHeight = 145;

        const p1 = { x: 180, y: 200, vx: 0, vy: 0, radius: 40, isGrounded: false, speed: 6.5, jumpForce: 13, faceRight: true, isKicking: false, kickTimer: 0, team: teams["Ecuador"] };
        const p2 = { x: 620, y: 200, vx: 0, vy: 0, radius: 40, isGrounded: false, speed: 6.5, jumpForce: 13, faceRight: false, isKicking: false, kickTimer: 0, team: teams["Brasil"] };
        const ball = { x: 400, y: 100, vx: 0, vy: 0, radius: 15, rotation: 0 };

        const keys = {};
        window.addEventListener("keydown", e => {
            keys[e.code] = true;
            if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) e.preventDefault();
        });
        window.addEventListener("keyup", e => keys[e.code] = false);

        function showMenu() {
            gameState = "menu";
            document.getElementById("game-over-overlay").style.display = "none";
            document.getElementById("menu-overlay").style.display = "flex";
        }

        function startGame() {
            let t1 = select1.value; let t2 = select2.value;
            p1.team = teams[t1]; p2.team = teams[t2];
            document.getElementById("name1").innerText = t1.substring(0,3).toUpperCase();
            document.getElementById("name2").innerText = t2.substring(0,3).toUpperCase();

            score1 = 0; score2 = 0; timeLeft = 90;
            updateScoreUI();
            
            document.getElementById("menu-overlay").style.display = "none";
            resetPositions(1);
            
            gameState = "playing";
            lastTime = Date.now();
        }

        function endGame() {
            gameState = "gameover";
            let text = "¡EMPATE!";
            if(score1 > score2) text = `¡${select1.value.toUpperCase()} GANA!`;
            if(score2 > score1) text = `¡${select2.value.toUpperCase()} GANA!`;
            
            document.getElementById("winner-text").innerText = text;
            document.getElementById("game-over-overlay").style.display = "flex";
        }

        function updateScoreUI() {
            document.getElementById("score1").innerText = score1;
            document.getElementById("score2").innerText = score2;
            document.getElementById("timer-box").innerText = timeLeft;
        }

        function resetPositions(scorer) {
            p1.x = 180; p1.y = groundY - p1.radius; p1.vx = 0; p1.vy = 0;
            p2.x = 620; p2.y = groundY - p2.radius; p2.vx = 0; p2.vy = 0;
            ball.x = 400; ball.y = 100; ball.vx = scorer === 1 ? -3 : 3; ball.vy = -6; ball.rotation = 0;
        }

        function update() {
            if (gameState !== "playing") return;

            let now = Date.now();
            if (now - lastTime >= 1000) {
                timeLeft--; lastTime = now;
                document.getElementById("timer-box").innerText = timeLeft;
                if (timeLeft <= 0) endGame();
            }

            // Controles P1
            if (keys["KeyA"]) { p1.vx = -p1.speed; p1.faceRight = false; }
            else if (keys["KeyD"]) { p1.vx = p1.speed; p1.faceRight = true; }
            else p1.vx *= friction;
            if (keys["KeyW"] && p1.isGrounded) { p1.vy = -p1.jumpForce; p1.isGrounded = false; }
            if (keys["Space"] && !p1.isKicking) { p1.isKicking = true; p1.kickTimer = 12; }

            // Controles P2
            if (keys["ArrowLeft"]) { p2.vx = -p2.speed; p2.faceRight = false; }
            else if (keys["ArrowRight"]) { p2.vx = p2.speed; p2.faceRight = true; }
            else p2.vx *= friction;
            if (keys["ArrowUp"] && p2.isGrounded) { p2.vy = -p2.jumpForce; p2.isGrounded = false; }
            if (keys["ArrowDown"] && !p2.isKicking) { p2.isKicking = true; p2.kickTimer = 12; }

            // Físicas Jugadores
            [p1, p2].forEach(p => {
                if (p.isKicking) { p.kickTimer--; if (p.kickTimer <= 0) p.isKicking = false; }
                p.vy += gravity; p.x += p.vx; p.y += p.vy;

                if (p.y + p.radius > groundY) { p.y = groundY - p.radius; p.vy = 0; p.isGrounded = true; }
                if (p.x - p.radius < goalWidth) p.x = goalWidth + p.radius;
                if (p.x + p.radius > canvas.width - goalWidth) p.x = canvas.width - goalWidth - p.radius;
            });

            // Físicas Balón
            ball.vy += gravity * 0.65; 
            ball.x += ball.vx; ball.y += ball.vy;
            ball.rotation += ball.vx * 0.05; // Rotación realista

            if (ball.y + ball.radius > groundY) { ball.y = groundY - ball.radius; ball.vy = -ball.vy * 0.75; ball.vx *= 0.97; }
            if (ball.y - ball.radius < 0) { ball.y = ball.radius; ball.vy = -ball.vy * 0.75; }

            // Rebote Largueros
            if (ball.x - ball.radius <= goalWidth && ball.y >= groundY - goalHeight - 5 && ball.y <= groundY - goalHeight + 5) {
                ball.vy = -Math.abs(ball.vy) * 0.8; ball.y = groundY - goalHeight - ball.radius;
            }
            if (ball.x + ball.radius >= canvas.width - goalWidth && ball.y >= groundY - goalHeight - 5 && ball.y <= groundY - goalHeight + 5) {
                ball.vy = -Math.abs(ball.vy) * 0.8; ball.y = groundY - goalHeight - ball.radius;
            }

            // Goles
            if (ball.x < goalWidth && ball.y > groundY - goalHeight) { score2++; updateScoreUI(); resetPositions(2); }
            if (ball.x > canvas.width - goalWidth && ball.y > groundY - goalHeight) { score1++; updateScoreUI(); resetPositions(1); }

            if (ball.x - ball.radius < 0) { ball.x = ball.radius; ball.vx = -ball.vx * 0.75; }
            if (ball.x + ball.radius > canvas.width) { ball.x = canvas.width - ball.radius; ball.vx = -ball.vx * 0.75; }

            // Colisiones Jugador vs Balón
            [p1, p2].forEach(p => {
                let dx = ball.x - p.x;
                let dy = ball.y - p.y;
                let dist = Math.sqrt(dx * dx + dy * dy);

                // Lógica Patada Fuerte
                if (p.isKicking) {
                    let footX = p.x + (p.faceRight ? 35 : -35);
                    let footY = p.y + p.radius - 5;
                    let fDist = Math.sqrt(Math.pow(ball.x - footX, 2) + Math.pow(ball.y - footY, 2));
                    
                    if (fDist < p.radius + ball.radius) {
                        ball.vx = p.faceRight ? 16 : -16; ball.vy = -9;
                        p.isKicking = false; return;
                    }
                }

                // Rebote Cuerpo
                if (dist < p.radius + ball.radius) {
                    let nx = dx / dist, ny = dy / dist;
                    ball.x = p.x + nx * (p.radius + ball.radius);
                    ball.y = p.y + ny * (p.radius + ball.radius);
                    let speed = Math.min(Math.sqrt(ball.vx * ball.vx + ball.vy * ball.vy) + 1.5, 13);
                    ball.vx = nx * speed + p.vx * 0.5;
                    ball.vy = ny * speed + p.vy * 0.5;
                }
            });
        }

        // --- DIBUJADO DE GRÁFICOS HD ---
        function drawStadium() {
            // Cielo degradado
            let sky = ctx.createLinearGradient(0, 0, 0, groundY);
            sky.addColorStop(0, "#0b1b36");
            sky.addColorStop(1, "#1e437a");
            ctx.fillStyle = sky;
            ctx.fillRect(0, 0, canvas.width, groundY);

            // Gradas
            ctx.fillStyle = "#0a111a";
            ctx.fillRect(0, groundY - 200, canvas.width, 200);
            
            // Público animado
            for (let i = 0; i < 400; i++) {
                let px = (Math.sin(i * 98) * 0.5 + 0.5) * canvas.width;
                let py = (Math.cos(i * 45) * 0.5 + 0.5) * 180 + (groundY - 190);
                ctx.fillStyle = i % 4 === 0 ? "#f1c40f" : (i % 3 === 0 ? "#e74c3c" : "#ecf0f1");
                ctx.globalAlpha = Math.random() * 0.5 + 0.5;
                ctx.beginPath(); ctx.arc(px, py, 1.5, 0, Math.PI*2); ctx.fill();
            }
            ctx.globalAlpha = 1.0;

            // Focos del estadio
            ctx.fillStyle = "rgba(255, 255, 255, 0.08)";
            ctx.beginPath(); ctx.moveTo(50, 0); ctx.lineTo(350, groundY); ctx.lineTo(-100, groundY); ctx.fill();
            ctx.beginPath(); ctx.moveTo(750, 0); ctx.lineTo(900, groundY); ctx.lineTo(450, groundY); ctx.fill();

            // Césped (Patrón HD)
            for (let i = 0; i < canvas.width; i += 50) {
                ctx.fillStyle = (i / 50) % 2 === 0 ? "#1d8a2a" : "#229e31";
                ctx.fillRect(i, groundY, 50, canvas.height - groundY);
            }
            
            // Líneas de cal del campo
            ctx.fillStyle = "rgba(255,255,255,0.85)";
            ctx.fillRect(canvas.width / 2 - 3, groundY, 6, canvas.height - groundY);
            ctx.fillRect(0, groundY, canvas.width, 4); // Línea de banda
        }

        function drawGoal(x, isLeft) {
            // Sombra del arco
            ctx.fillStyle = "rgba(0,0,0,0.3)";
            let shX = isLeft ? 10 : canvas.width - goalWidth - 10;
            ctx.fillRect(shX, groundY, goalWidth, 10);

            // Red
            ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
            ctx.lineWidth = 1;
            let startX = isLeft ? 0 : canvas.width - goalWidth;
            for (let i = groundY - goalHeight; i <= groundY; i += 12) { ctx.beginPath(); ctx.moveTo(startX, i); ctx.lineTo(startX + goalWidth, i); ctx.stroke(); }
            for (let i = startX; i <= startX + goalWidth; i += 12) { ctx.beginPath(); ctx.moveTo(i, groundY - goalHeight); ctx.lineTo(i, groundY); ctx.stroke(); }

            // Postes con reflejo (Efecto metálico)
            let grad = ctx.createLinearGradient(startX, 0, startX + 10, 0);
            grad.addColorStop(0, "#ffffff"); grad.addColorStop(1, "#aaaaaa");
            
            ctx.strokeStyle = grad; ctx.lineWidth = 8; ctx.lineCap = "round";
            ctx.beginPath();
            if (isLeft) { ctx.moveTo(0, groundY - goalHeight); ctx.lineTo(goalWidth, groundY - goalHeight); ctx.lineTo(goalWidth, groundY); } 
            else { ctx.moveTo(canvas.width, groundY - goalHeight); ctx.lineTo(canvas.width - goalWidth, groundY - goalHeight); ctx.lineTo(canvas.width - goalWidth, groundY); }
            ctx.stroke();
        }

        function drawShadow(x, y, radius) {
            ctx.fillStyle = "rgba(0,0,0,0.4)";
            ctx.beginPath();
            ctx.ellipse(x, groundY, radius * 0.8, radius * 0.2, 0, 0, Math.PI * 2);
            ctx.fill();
        }

        function drawCabezon(p) {
            drawShadow(p.x, p.y, p.radius);

            ctx.save();
            // Recorte circular base para la cabeza y camiseta
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.clip();

            // 1. Piel (Rostro)
            ctx.fillStyle = "#f1c27d"; 
            ctx.fillRect(p.x - p.radius, p.y - p.radius, p.radius * 2, p.radius * 2);

            // 2. Cabello (Parte superior)
            ctx.fillStyle = "#3e2723"; 
            ctx.fillRect(p.x - p.radius, p.y - p.radius, p.radius * 2, p.radius * 0.4);

            // 3. Camiseta Tricolor (Parte Inferior)
            let jerseyY = p.y + p.radius * 0.1; // Inicio de la camiseta
            let jerseyH = p.radius * 0.9;
            let bandHeight = jerseyH / p.team.length; // Divide el espacio por la cantidad de colores

            for(let i=0; i < p.team.length; i++) {
                ctx.fillStyle = p.team[i];
                ctx.fillRect(p.x - p.radius, jerseyY + (bandHeight * i), p.radius * 2, bandHeight + 1);
            }
            ctx.restore();

            // Borde del cabezón
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.lineWidth = 3; ctx.strokeStyle = "#111"; ctx.stroke();

            // Rostro: Ojo
            ctx.beginPath();
            let eyeOffsetX = p.faceRight ? 12 : -12;
            ctx.arc(p.x + eyeOffsetX, p.y - 8, 7, 0, Math.PI * 2);
            ctx.fillStyle = "#fff"; ctx.fill(); ctx.stroke();
            
            // Rostro: Pupila
            ctx.beginPath();
            let pupilOffsetX = p.faceRight ? 15 : -15;
            ctx.arc(p.x + pupilOffsetX, p.y - 8, 3, 0, Math.PI * 2);
            ctx.fillStyle = "#000"; ctx.fill();

            // Rostro: Sonrisa
            ctx.beginPath();
            let smileX = p.faceRight ? 12 : -12;
            ctx.arc(p.x + smileX, p.y + 5, 5, 0, Math.PI, false);
            ctx.strokeStyle = "#000"; ctx.lineWidth = 2; ctx.stroke();

            // Botín dinámico
            ctx.beginPath();
            let footBaseX = p.faceRight ? 10 : -34;
            if (p.isKicking) footBaseX += p.faceRight ? 24 : -24;
            
            ctx.roundRect(p.x + footBaseX, p.y + p.radius - 2, 24, 14, 7);
            ctx.fillStyle = p.team[0]; // Color primario de la bandera
            ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = "#111"; ctx.stroke();
        }

        function drawBall() {
            drawShadow(ball.x, ball.y, ball.radius);

            ctx.save();
            ctx.translate(ball.x, ball.y);
            ctx.rotate(ball.rotation);

            // Base blanca
            ctx.beginPath(); ctx.arc(0, 0, ball.radius, 0, Math.PI * 2);
            ctx.fillStyle = "#f5f6fa"; ctx.fill();
            ctx.lineWidth = 2; ctx.strokeStyle = "#2f3640"; ctx.stroke();
            
            // Diseño Pentágono clásico (Telstar)
            ctx.fillStyle = "#2f3640";
            ctx.beginPath();
            for(let i=0; i<5; i++) {
                let angle = i * (Math.PI * 2 / 5) - Math.PI/2;
                let px = Math.cos(angle) * ball.radius * 0.4;
                let py = Math.sin(angle) * ball.radius * 0.4;
                if(i===0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
            }
            ctx.closePath(); ctx.fill();

            // Líneas hacia los bordes
            for(let i=0; i<5; i++) {
                let angle = i * (Math.PI * 2 / 5) - Math.PI/2;
                ctx.beginPath();
                ctx.moveTo(Math.cos(angle) * ball.radius * 0.4, Math.sin(angle) * ball.radius * 0.4);
                ctx.lineTo(Math.cos(angle) * ball.radius, Math.sin(angle) * ball.radius);
                ctx.stroke();
            }

            ctx.restore();
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawStadium();
            drawGoal(0, true);
            drawGoal(canvas.width - goalWidth, false);

            if(gameState === "playing" || gameState === "gameover") {
                drawCabezon(p1);
                drawCabezon(p2);
                drawBall();
            }
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
    """
    return html_content
