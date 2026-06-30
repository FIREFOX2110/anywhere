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
    <title>Fútbol Cabezones - Edición Mundial</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: #111;
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
            text-shadow: 2px 2px 5px rgba(0,0,0,0.8);
            font-size: 28px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        #top-bar {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 10px;
            background: #222;
            padding: 10px 30px;
            border-radius: 10px;
            border: 2px solid #555;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        .score-team { font-size: 24px; font-weight: bold; width: 120px; text-align: center; }
        .score-number { font-size: 32px; font-weight: bold; padding: 0 15px; }
        #timer-box {
            background: #ffcc00;
            color: #000;
            padding: 5px 15px;
            border-radius: 5px;
            font-size: 24px;
            font-weight: 900;
            border: 2px solid #fff;
        }
        
        #game-container {
            position: relative;
        }
        canvas {
            border: 4px solid #fff;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.9);
            border-radius: 8px;
            background: #000; /* El fondo se dibuja en JS */
        }

        /* Menús Superpuestos */
        .overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.85);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            z-index: 10;
        }
        .menu-box {
            background: #2a2a2a;
            padding: 30px;
            border-radius: 12px;
            border: 2px solid #555;
            text-align: center;
        }
        select {
            padding: 10px;
            font-size: 16px;
            margin: 10px;
            border-radius: 5px;
            background: #fff;
            color: #000;
            font-weight: bold;
        }
        button {
            padding: 12px 25px;
            font-size: 18px;
            font-weight: bold;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 15px;
            transition: 0.2s;
        }
        button:hover { background: #218838; transform: scale(1.05); }

        .controls-hint {
            margin-top: 15px;
            display: flex;
            gap: 40px;
            font-size: 13px;
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 8px;
        }
    </style>
</head>
<body>

    <h1>🏆 Copa Mundial Cabezones 🏆</h1>
    
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
                <h2>SELECCIONA TUS EQUIPOS</h2>
                <div>
                    <label style="color: #ff4d4d; font-weight: bold;">Jugador 1:</label>
                    <select id="team1-select"></select>
                </div>
                <div>
                    <label style="color: #3399ff; font-weight: bold;">Jugador 2:</label>
                    <select id="team2-select"></select>
                </div>
                <button onclick="startGame()">¡JUGAR PARTIDO!</button>
            </div>
        </div>

        <div id="game-over-overlay" class="overlay" style="display: none;">
            <div class="menu-box">
                <h2 id="winner-text" style="font-size: 30px; color: #ffcc00;">¡TIEMPO FINALIZADO!</h2>
                <button onclick="showMenu()">Volver al Menú</button>
            </div>
        </div>
    </div>

    <div class="controls-hint">
        <div><strong>P1:</strong> A / D (Mover) | W (Saltar) | <b>ESPACIO (Patear)</b></div>
        <div><strong>P2:</strong> ← / → (Mover) | ↑ (Saltar) | <b>↓ (Patear)</b></div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // --- DATOS DE SELECCIONES ---
        const teams = {
            "Ecuador": { c1: "#ffdd00", c2: "#002366" },
            "Argentina": { c1: "#75AADB", c2: "#ffffff" },
            "Brasil": { c1: "#009c3b", c2: "#ffdf00" },
            "España": { c1: "#aa151b", c2: "#000066" },
            "Francia": { c1: "#002395", c2: "#ffffff" },
            "Alemania": { c1: "#ffffff", c2: "#000000" }
        };

        // Poblar selects
        const select1 = document.getElementById("team1-select");
        const select2 = document.getElementById("team2-select");
        for(let t in teams) {
            select1.innerHTML += `<option value="${t}">${t}</option>`;
            select2.innerHTML += `<option value="${t}">${t}</option>`;
        }
        select1.value = "Ecuador";
        select2.value = "Brasil";

        // --- ESTADO DEL JUEGO ---
        let gameState = "menu"; // 'menu', 'playing', 'gameover'
        let timeLeft = 90;
        let lastTime = 0;
        let score1 = 0;
        let score2 = 0;

        // Físicas globales
        const gravity = 0.6;
        const friction = 0.82;
        const groundY = 340; 
        const goalWidth = 60;
        const goalHeight = 140;

        // Entidades
        const p1 = { x: 180, y: 200, vx: 0, vy: 0, radius: 38, isGrounded: false, speed: 6.5, jumpForce: 12.5, faceRight: true, isKicking: false, kickTimer: 0, team: teams["Ecuador"] };
        const p2 = { x: 620, y: 200, vx: 0, vy: 0, radius: 38, isGrounded: false, speed: 6.5, jumpForce: 12.5, faceRight: false, isKicking: false, kickTimer: 0, team: teams["Brasil"] };
        const ball = { x: 400, y: 100, vx: 0, vy: 0, radius: 14 };

        // Controles
        const keys = {};
        window.addEventListener("keydown", e => {
            keys[e.code] = true;
            if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) e.preventDefault();
        });
        window.addEventListener("keyup", e => keys[e.code] = false);

        // --- FUNCIONES DE CONTROL DE JUEGO ---
        function showMenu() {
            gameState = "menu";
            document.getElementById("game-over-overlay").style.display = "none";
            document.getElementById("menu-overlay").style.display = "flex";
        }

        function startGame() {
            // Asignar equipos
            let t1 = select1.value;
            let t2 = select2.value;
            p1.team = teams[t1];
            p2.team = teams[t2];
            
            document.getElementById("name1").innerText = t1.substring(0,3).toUpperCase();
            document.getElementById("name2").innerText = t2.substring(0,3).toUpperCase();

            // Resetear stats
            score1 = 0; score2 = 0;
            timeLeft = 90;
            updateScoreUI();
            
            document.getElementById("menu-overlay").style.display = "none";
            resetPositions(1);
            
            gameState = "playing";
            lastTime = Date.now();
        }

        function endGame() {
            gameState = "gameover";
            let text = "¡EMPATE!";
            if(score1 > score2) text = `¡${select1.value} GANA!`;
            if(score2 > score1) text = `¡${select2.value} GANA!`;
            
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
            ball.x = 400; ball.y = 120; ball.vx = scorer === 1 ? -4 : 4; ball.vy = -6;
        }

        // --- LÓGICA PRINCIPAL ---
        function update() {
            if (gameState !== "playing") return;

            // Timer
            let now = Date.now();
            if (now - lastTime >= 1000) {
                timeLeft--;
                lastTime = now;
                document.getElementById("timer-box").innerText = timeLeft;
                if (timeLeft <= 0) endGame();
            }

            // Movimiento P1
            if (keys["KeyA"]) { p1.vx = -p1.speed; p1.faceRight = false; }
            else if (keys["KeyD"]) { p1.vx = p1.speed; p1.faceRight = true; }
            else p1.vx *= friction;
            if (keys["KeyW"] && p1.isGrounded) { p1.vy = -p1.jumpForce; p1.isGrounded = false; }
            if (keys["Space"] && !p1.isKicking) { p1.isKicking = true; p1.kickTimer = 10; }

            // Movimiento P2
            if (keys["ArrowLeft"]) { p2.vx = -p2.speed; p2.faceRight = false; }
            else if (keys["ArrowRight"]) { p2.vx = p2.speed; p2.faceRight = true; }
            else p2.vx *= friction;
            if (keys["ArrowUp"] && p2.isGrounded) { p2.vy = -p2.jumpForce; p2.isGrounded = false; }
            if (keys["ArrowDown"] && !p2.isKicking) { p2.isKicking = true; p2.kickTimer = 10; }

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

            if (ball.y + ball.radius > groundY) { ball.y = groundY - ball.radius; ball.vy = -ball.vy * 0.75; ball.vx *= 0.97; }
            if (ball.y - ball.radius < 0) { ball.y = ball.radius; ball.vy = -ball.vy * 0.75; }

            // Rebote en largueros
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

            // Colisiones y Patadas
            [p1, p2].forEach(p => {
                let dx = ball.x - p.x;
                let dy = ball.y - p.y;
                let dist = Math.sqrt(dx * dx + dy * dy);

                if (p.isKicking) {
                    let footX = p.x + (p.faceRight ? 35 : -35);
                    let footY = p.y + p.radius - 5;
                    let fDist = Math.sqrt(Math.pow(ball.x - footX, 2) + Math.pow(ball.y - footY, 2));
                    
                    if (fDist < p.radius + ball.radius) {
                        ball.vx = p.faceRight ? 15 : -15; ball.vy = -8;
                        p.isKicking = false; return;
                    }
                }

                if (dist < p.radius + ball.radius) {
                    let nx = dx / dist, ny = dy / dist;
                    ball.x = p.x + nx * (p.radius + ball.radius);
                    ball.y = p.y + ny * (p.radius + ball.radius);
                    let speed = Math.min(Math.sqrt(ball.vx * ball.vx + ball.vy * ball.vy) + 1.5, 12);
                    ball.vx = nx * speed + p.vx * 0.4;
                    ball.vy = ny * speed + p.vy * 0.4;
                }
            });
        }

        // --- DIBUJADO ---
        function drawStadium() {
            // Cielo de noche
            let grad = ctx.createLinearGradient(0, 0, 0, groundY);
            grad.addColorStop(0, "#001133");
            grad.addColorStop(1, "#1a4477");
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, canvas.width, groundY);

            // Gradas
            ctx.fillStyle = "#111";
            ctx.fillRect(0, groundY - 180, canvas.width, 180);
            
            // Público (puntitos aleatorios)
            for (let i = 0; i < 300; i++) {
                let px = (Math.sin(i * 123) * 0.5 + 0.5) * canvas.width;
                let py = (Math.cos(i * 321) * 0.5 + 0.5) * 160 + (groundY - 170);
                ctx.fillStyle = i % 3 === 0 ? "#ffcc00" : (i % 2 === 0 ? "#ff4d4d" : "#3399ff");
                ctx.fillRect(px, py, 3, 3);
            }

            // Luces del estadio
            ctx.fillStyle = "rgba(255, 255, 255, 0.1)";
            ctx.beginPath(); ctx.moveTo(100, 0); ctx.lineTo(300, groundY); ctx.lineTo(0, groundY); ctx.fill();
            ctx.beginPath(); ctx.moveTo(700, 0); ctx.lineTo(800, groundY); ctx.lineTo(500, groundY); ctx.fill();

            // Cancha (Franjas de césped)
            for (let i = 0; i < canvas.width; i += 80) {
                ctx.fillStyle = (i / 80) % 2 === 0 ? "#1e992d" : "#1a8a27";
                ctx.fillRect(i, groundY, 80, canvas.height - groundY);
            }
            
            // Línea central
            ctx.fillStyle = "rgba(255,255,255,0.6)";
            ctx.fillRect(canvas.width / 2 - 2, groundY, 4, canvas.height - groundY);
        }

        function drawGoal(x, isLeft) {
            ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
            ctx.lineWidth = 1.5;
            let startX = isLeft ? 0 : canvas.width - goalWidth;
            
            for (let i = groundY - goalHeight; i <= groundY; i += 14) { ctx.beginPath(); ctx.moveTo(startX, i); ctx.lineTo(startX + goalWidth, i); ctx.stroke(); }
            for (let i = startX; i <= startX + goalWidth; i += 14) { ctx.beginPath(); ctx.moveTo(i, groundY - goalHeight); ctx.lineTo(i, groundY); ctx.stroke(); }

            ctx.strokeStyle = "#fff"; ctx.lineWidth = 6; ctx.lineCap = "round";
            ctx.beginPath();
            if (isLeft) { ctx.moveTo(0, groundY - goalHeight); ctx.lineTo(goalWidth, groundY - goalHeight); ctx.lineTo(goalWidth, groundY); } 
            else { ctx.moveTo(canvas.width, groundY - goalHeight); ctx.lineTo(canvas.width - goalWidth, groundY - goalHeight); ctx.lineTo(canvas.width - goalWidth, groundY); }
            ctx.stroke();
        }

        function drawCabezon(p) {
            // Camiseta (Mitad superior / Mitad inferior)
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, Math.PI, 0); // Arriba
            ctx.fillStyle = p.team.c1;
            ctx.fill();
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI); // Abajo
            ctx.fillStyle = p.team.c2;
            ctx.fill();
            
            // Borde cabeza
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.lineWidth = 3; ctx.strokeStyle = "#111"; ctx.stroke();

            // Ojo
            ctx.beginPath();
            let eyeOffsetX = p.faceRight ? 14 : -14;
            ctx.arc(p.x + eyeOffsetX, p.y - 12, 8, 0, Math.PI * 2);
            ctx.fillStyle = "#fff"; ctx.fill(); ctx.stroke();
            
            // Pupila
            ctx.beginPath();
            let pupilOffsetX = p.faceRight ? 17 : -17;
            ctx.arc(p.x + pupilOffsetX, p.y - 12, 3.5, 0, Math.PI * 2);
            ctx.fillStyle = "#000"; ctx.fill();

            // Botín
            ctx.beginPath();
            let footBaseX = p.faceRight ? 12 : -32;
            if (p.isKicking) footBaseX += p.faceRight ? 22 : -22;
            
            ctx.roundRect(p.x + footBaseX, p.y + p.radius - 4, 22, 13, 6);
            ctx.fillStyle = p.team.c1; // Botín combina con la camiseta
            ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = "#000"; ctx.stroke();
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawStadium();
            drawGoal(0, true);
            drawGoal(canvas.width - goalWidth, false);

            if(gameState === "playing" || gameState === "gameover") {
                drawCabezon(p1);
                drawCabezon(p2);

                // Balón
                ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
                ctx.fillStyle = "#fff"; ctx.fill();
                ctx.strokeStyle = "#000"; ctx.lineWidth = 2.5; ctx.stroke();
                
                ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.radius * 0.5, 0, Math.PI, true);
                ctx.strokeStyle = "#333"; ctx.lineWidth = 1.5; ctx.stroke();
            }
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        // Iniciar
        gameLoop();
    </script>
</body>
</html>
    """
    return html_content
