export default class UI {
  constructor() {
    this.scoreElement = document.getElementById("score");
  }

  updateScore(score) {
    this.scoreElement.textContent = score;
  }

  showGameOver(ctx, canvas, result) {
    ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "white";
    ctx.font = "48px Arial";
    ctx.textAlign = "center";

    if (result === "win") {
      ctx.fillText("Ви виграли!", canvas.width / 2, canvas.height / 2);
    } else {
      ctx.fillText("Гру завершено. Ви програли.", canvas.width / 2, canvas.height / 2);
    }
  }
}
