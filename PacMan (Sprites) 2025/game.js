// const canvas = document.getElementById("gameCanvas");
// const ctx = canvas.getContext("2d");
//
// const startBtn = document.getElementById("startBtn");
// const restartBtn = document.getElementById("restartBtn");
//
// const tileSize = 40;
// const rows = 15;
// const cols = 20;
//
// // 1 — стіна, 2 — їжа
// const initialMaze = [
//   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
//   [1,2,2,2,2,2,1,2,2,2,2,1,2,2,2,2,2,2,2,1],
//   [1,2,1,1,1,2,1,2,1,1,2,1,2,1,1,1,1,1,2,1],
//   [1,2,1,0,1,2,1,2,1,1,2,1,2,1,0,0,0,1,2,1],
//   [1,2,1,0,1,2,1,2,2,2,2,1,2,1,0,1,0,1,2,1],
//   [1,2,1,0,1,2,1,1,1,1,2,1,2,1,0,1,0,1,2,1],
//   [1,2,2,0,2,2,2,2,2,1,2,2,2,2,0,2,0,2,2,1],
//   [1,2,1,0,1,1,1,1,2,1,1,1,1,1,0,1,1,1,2,1],
//   [1,2,1,0,1,2,2,2,2,2,2,2,2,1,0,1,0,0,2,1],
//   [1,2,1,0,1,2,1,1,1,1,1,1,2,1,0,1,0,1,2,1],
//   [1,2,2,2,2,2,1,0,0,0,0,1,2,2,2,2,0,1,2,1],
//   [1,2,1,1,1,2,1,0,1,1,0,1,1,1,1,1,0,1,2,1],
//   [1,2,2,2,1,2,2,0,2,2,0,2,2,2,2,2,0,2,2,1],
//   [1,2,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
//   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
// ];
//
// let maze;
// let player;
// let enemies;
// let keys;
// let score;
// let totalFood;
// let gameOver;
// let animationId;
//
// const playerSprite = new Image();
// playerSprite.src = "assets/sprites/pacman.png";
//
// function resetGame() {
//   maze = JSON.parse(JSON.stringify(initialMaze));
//   score = 0;
//   totalFood = 0;
//   maze.forEach(row => row.forEach(cell => { if (cell === 2) totalFood++; }));
//   gameOver = false;
//
//   player = {
//     x: 1 * tileSize,
//     y: 1 * tileSize,
//     speed: 2,
//     width: 32,
//     height: 32,
//     frameX: 0,
//     frameY: 0,
//     maxFrame: 3,
//     frameDelay: 0,
//     frameInterval: 8,
//     direction: "right"
//   };
//
//   enemies = [
//     { x: 18 * tileSize, y: 1 * tileSize, dir: "left" },
//     { x: 10 * tileSize, y: 10 * tileSize, dir: "up" }
//   ];
//
//   keys = {
//     ArrowUp: false,
//     ArrowDown: false,
//     ArrowLeft: false,
//     ArrowRight: false
//   };
// }
//
// window.addEventListener("keydown", (e) => {
//   if (keys.hasOwnProperty(e.key)) keys[e.key] = true;
// });
//
// window.addEventListener("keyup", (e) => {
//   if (keys.hasOwnProperty(e.key)) keys[e.key] = false;
// });
//
// function canMove(x, y, width, height) {
//   const corners = [
//     { x: x, y: y },
//     { x: x + width - 1, y: y },
//     { x: x, y: y + height - 1 },
//     { x: x + width - 1, y: y + height - 1 }
//   ];
//   return corners.every(corner => {
//     const row = Math.floor(corner.y / tileSize);
//     const col = Math.floor(corner.x / tileSize);
//     return maze[row] && maze[row][col] !== 1;
//   });
// }
//
// function movePlayer() {
//   let newX = player.x;
//   let newY = player.y;
//
//   if (keys.ArrowLeft) {
//     newX -= player.speed;
//     player.direction = "left";
//   }
//   if (keys.ArrowRight) {
//     newX += player.speed;
//     player.direction = "right";
//   }
//   if (keys.ArrowUp) {
//     newY -= player.speed;
//     player.direction = "up";
//   }
//   if (keys.ArrowDown) {
//     newY += player.speed;
//     player.direction = "down";
//   }
//
//   if (canMove(newX, player.y, player.width, player.height)) player.x = newX;
//   if (canMove(player.x, newY, player.width, player.height)) player.y = newY;
//
//   const row = Math.floor(player.y / tileSize);
//   const col = Math.floor(player.x / tileSize);
//   if (maze[row][col] === 2) {
//     maze[row][col] = 0;
//     score++;
//     if (score === totalFood) gameOver = "win";
//   }
// }
//
// function drawMaze() {
//   for (let row = 0; row < rows; row++) {
//     for (let col = 0; col < cols; col++) {
//       const cell = maze[row][col];
//       if (cell === 1) {
//         ctx.fillStyle = "#444";
//         ctx.fillRect(col * tileSize, row * tileSize, tileSize, tileSize);
//       } else if (cell === 2) {
//         ctx.fillStyle = "#fff";
//         ctx.beginPath();
//         ctx.arc(col * tileSize + tileSize / 2, row * tileSize + tileSize / 2, 4, 0, Math.PI * 2);
//         ctx.fill();
//       }
//     }
//   }
// }
//
// function drawPlayer() {
//   const centerX = player.x + player.width / 2;
//   const centerY = player.y + player.height / 2;
//
//   ctx.save();
//   ctx.translate(centerX, centerY);
//
//   switch (player.direction) {
//     case "left": ctx.scale(-1, 1); break;
//     case "up": ctx.rotate(-Math.PI / 2); break;
//     case "down": ctx.rotate(Math.PI / 2); break;
//   }
//
//   ctx.drawImage(
//     playerSprite,
//     player.frameX * player.width,
//     player.frameY * player.height,
//     player.width,
//     player.height,
//     -player.width / 2,
//     -player.height / 2,
//     player.width,
//     player.height
//   );
//
//   ctx.restore();
//
//   player.frameDelay++;
//   if (player.frameDelay >= player.frameInterval) {
//     player.frameX = (player.frameX + 1) % (player.maxFrame + 1);
//     player.frameDelay = 0;
//   }
// }
//
// function drawEnemies() {
//   ctx.fillStyle = "red";
//   enemies.forEach(enemy => {
//     ctx.beginPath();
//     ctx.arc(enemy.x + tileSize / 2, enemy.y + tileSize / 2, 14, 0, Math.PI * 2);
//     ctx.fill();
//
//     let dx = 0, dy = 0;
//     switch (enemy.dir) {
//       case "up": dy = -1; break;
//       case "down": dy = 1; break;
//       case "left": dx = -1; break;
//       case "right": dx = 1; break;
//     }
//
//     const newX = enemy.x + dx;
//     const newY = enemy.y + dy;
//
//     if (canMove(newX, newY, tileSize, tileSize)) {
//       enemy.x = newX;
//       enemy.y = newY;
//     } else {
//       const dirs = ["up", "down", "left", "right"];
//       enemy.dir = dirs[Math.floor(Math.random() * dirs.length)];
//     }
//
//     if (
//       Math.abs(enemy.x - player.x) < 20 &&
//       Math.abs(enemy.y - player.y) < 20
//     ) {
//       gameOver = "lose";
//     }
//   });
// }
//
// function updateUI() {
//   document.getElementById("score").textContent = score;
// }
//
// function showGameOver() {
//   ctx.fillStyle = "rgba(0,0,0,0.8)";
//   ctx.fillRect(0, 0, canvas.width, canvas.height);
//   ctx.fillStyle = "white";
//   ctx.font = "36px Arial";
//   ctx.textAlign = "center";
//   ctx.fillText(
//     gameOver === "win" ? "Ви виграли!" : "Програш!",
//     canvas.width / 2,
//     canvas.height / 2
//   );
// }
//
// function gameLoop() {
//   ctx.clearRect(0, 0, canvas.width, canvas.height);
//   drawMaze();
//
//   if (!gameOver) {
//     movePlayer();
//     drawPlayer();
//     drawEnemies();
//   } else {
//     showGameOver();
//     cancelAnimationFrame(animationId);
//     startBtn.style.display = "none";
//     restartBtn.style.display = "inline-block";
//     return;
//   }
//
//   updateUI();
//   animationId = requestAnimationFrame(gameLoop);
// }
//
// // --- Кнопки ---
// startBtn.addEventListener("click", () => {
//   startBtn.style.display = "none";
//   restartBtn.style.display = "none";
//   resetGame();
//   gameLoop();
// });
//
// restartBtn.addEventListener("click", () => {
//   resetGame();
//   restartBtn.style.display = "none";
//   gameLoop();
// });
//
// // Початковий стан
// resetGame();
