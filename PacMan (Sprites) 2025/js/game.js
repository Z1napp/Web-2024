import Maze from "./maze.js";
import Player from "./player.js";
import Enemy from "./enemy.js";
import InputHandler from "./input.js";
import UI from "./ui.js";

export default class Game {
  constructor(canvas, ctx, tileSize, rows, cols, initialMaze) {
    this.canvas = canvas;
    this.ctx = ctx;
    this.tileSize = tileSize;
    this.rows = rows;
    this.cols = cols;
    this.initialMaze = initialMaze;

    this.maze = null;
    this.player = null;
    this.enemies = [];
    this.inputHandler = new InputHandler();
    this.ui = new UI();

    this.score = 0;
    this.totalFood = 0;
    this.gameOver = false;
    this.animationId = null;

    this.playerSprite = new Image();
    this.playerSprite.src = "assets/sprites/pacman.png";
  }

  reset() {
    this.maze = new Maze(this.ctx, this.initialMaze, this.tileSize, this.rows, this.cols);
    this.maze.reset();

    this.score = 0;
    this.totalFood = this.maze.countFood();
    this.gameOver = false;

    this.player = new Player(this.playerSprite, this.tileSize);
    this.player.setPosition(1 * this.tileSize, 1 * this.tileSize);

    this.enemies = [
      new Enemy(18 * this.tileSize, 1 * this.tileSize, this.tileSize),
      new Enemy(10 * this.tileSize, 10 * this.tileSize, this.tileSize),
    ];

    this.inputHandler.reset();
  }

  start() {
    if (this.animationId) cancelAnimationFrame(this.animationId);
    this.gameLoop();
  }

  canMove(x, y, width, height) {
    return this.maze.canMove(x, y, width, height);
  }

  update() {
    if (this.gameOver) return;

    this.player.move(this.inputHandler.keys, this.canMove.bind(this));
    this.checkFoodCollision();
    this.enemies.forEach(enemy => {
      enemy.move(this.canMove.bind(this));
      if (this.isPlayerCaught(enemy)) this.gameOver = "lose";
    });

    if (this.score === this.totalFood) {
      this.gameOver = "win";
    }
  }

  checkFoodCollision() {
    const row = Math.floor(this.player.y / this.tileSize);
    const col = Math.floor(this.player.x / this.tileSize);
    if (this.maze.grid[row][col] === 2) {
      this.maze.grid[row][col] = 0;
      this.score++;
    }
  }

  isPlayerCaught(enemy) {
    const dx = Math.abs(enemy.x - this.player.x);
    const dy = Math.abs(enemy.y - this.player.y);
    return dx < 20 && dy < 20;
  }

  draw() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.maze.draw();

    this.player.draw(this.ctx);

    this.enemies.forEach(enemy => enemy.draw(this.ctx));
  }

  gameLoop() {
    this.update();
    this.draw();

    this.ui.updateScore(this.score);

    if (this.gameOver) {
      this.ui.showGameOver(this.ctx, this.canvas, this.gameOver);
      this.animationId = null;
      document.getElementById("startBtn").style.display = "none";
      document.getElementById("restartBtn").style.display = "inline-block";
      return;
    }

    this.animationId = requestAnimationFrame(() => this.gameLoop());
  }
}
