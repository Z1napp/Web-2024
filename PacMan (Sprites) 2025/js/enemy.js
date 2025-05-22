export default class Enemy {
  constructor(x, y, tileSize) {
    this.tileSize = tileSize;
    this.x = x;
    this.y = y;

    this.speed = 2; // швидкість руху в пікселях
    this.width = 32;
    this.height = 32;

    this.frameX = 0;
    this.frameY = 0;
    this.maxFrame = 1; // кількість кадрів анімації - став 1, якщо спрайт статичний
    this.frameDelay = 0;
    this.frameInterval = 10;

    this.direction = "left"; // початковий напрямок (можна міняти)

    this.sprite = new Image();
    this.sprite.src = "assets/sprites/enemy.png";

    // Цілі для руху (як у Player)
    this.targetX = Math.floor(this.x / tileSize);
    this.targetY = Math.floor(this.y / tileSize);
    this.isMoving = false;
  }

  move(canMove) {
    // Простий рух ворога — наприклад, хаотичний вибір напрямку, якщо не рухається
    if (!this.isMoving) {
      // Випадково вибираємо напрямок руху
      const directions = [
        { dx: -1, dy: 0, dir: "left" },
        { dx: 1, dy: 0, dir: "right" },
        { dx: 0, dy: -1, dir: "up" },
        { dx: 0, dy: 1, dir: "down" },
      ];

      const possibleMoves = directions.filter(({ dx, dy }) => {
        const newX = this.targetX + dx;
        const newY = this.targetY + dy;
        return canMove(newX * this.tileSize, newY * this.tileSize, this.width, this.height);
      });

      if (possibleMoves.length > 0) {
        const move = possibleMoves[Math.floor(Math.random() * possibleMoves.length)];
        this.targetX += move.dx;
        this.targetY += move.dy;
        this.direction = move.dir;
        this.isMoving = true;
      }
    }

    // Якщо рухаємось — плавно рухаємося до цілі
    if (this.isMoving) {
      const targetPixelX = this.targetX * this.tileSize;
      const targetPixelY = this.targetY * this.tileSize;

      if (this.x < targetPixelX) {
        this.x += this.speed;
        if (this.x > targetPixelX) this.x = targetPixelX;
      } else if (this.x > targetPixelX) {
        this.x -= this.speed;
        if (this.x < targetPixelX) this.x = targetPixelX;
      }

      if (this.y < targetPixelY) {
        this.y += this.speed;
        if (this.y > targetPixelY) this.y = targetPixelY;
      } else if (this.y > targetPixelY) {
        this.y -= this.speed;
        if (this.y < targetPixelY) this.y = targetPixelY;
      }

      if (this.x === targetPixelX && this.y === targetPixelY) {
        this.isMoving = false;
      }

      this.animate();
    }
  }

  animate() {
    this.frameDelay++;
    if (this.frameDelay >= this.frameInterval) {
      this.frameX = (this.frameX + 1) % (this.maxFrame + 1);
      this.frameDelay = 0;
    }
  }

  draw(ctx) {
    const centerX = this.x + this.width / 2;
    const centerY = this.y + this.height / 2;

    ctx.save();
    ctx.translate(centerX, centerY);

    switch (this.direction) {
      case "left":
        ctx.scale(-1, 1);
        break;
      case "up":
        ctx.rotate(-Math.PI / 2);
        break;
      case "down":
        ctx.rotate(Math.PI / 2);
        break;
    }

    ctx.drawImage(
      this.sprite,
      this.frameX * this.width,
      this.frameY * this.height,
      this.width,
      this.height,
      -this.width / 2,
      -this.height / 2,
      this.width,
      this.height
    );

    ctx.restore();
  }
}
