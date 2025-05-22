import { tileSize, rows, cols, initialMaze } from "./config.js";
import Game from "./game.js";

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const startBtn = document.getElementById("startBtn");
const restartBtn = document.getElementById("restartBtn");

const game = new Game(canvas, ctx, tileSize, rows, cols, initialMaze);

startBtn.addEventListener("click", () => {
  startBtn.style.display = "none";
  restartBtn.style.display = "none";
  game.reset();
  game.start();
});

restartBtn.addEventListener("click", () => {
  game.reset();
  restartBtn.style.display = "none";
  game.start();
});
