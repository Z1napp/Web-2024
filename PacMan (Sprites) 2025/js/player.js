export default class Player {
  constructor(sprite, tileSize) {
    this.sprite = sprite;
    this.tileSize = tileSize;

    this.x = 0;
    this.y = 0;
    this.speed = 2;

    this.width = 32;
    this.height = 32;

    this.frameX = 0;
    this.frameY = 0;
    this.maxFrame = 3;
    this.frameDelay = 0;
    this.frameInterval = 8;

    this.direction = "right";
  }

  setPosition(x, y) {
    this.x = x;
    this.y = y;
  }

  move(keys, canMove) {
    let newX = this.x;
    let newY = this.y;

    if (keys.ArrowLeft) {
      newX -= this.speed;
      this.direction = "left";
    }
    if (keys.ArrowRight) {
      newX += this.speed;
      this.direction = "right";
    }
    if (keys.ArrowUp) {
      newY -= this.speed;
      this.direction = "up";
    }
    if (keys.ArrowDown) {
      newY += this.speed;
      this.direction = "down";
    }

    if (canMove(newX, this.y, this.width, this.height)) this.x = newX;
    if (canMove(this.x, newY, this.width, this.height)) this.y = newY;

    this.animate();
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
