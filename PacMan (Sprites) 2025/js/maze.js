export default class Maze {
  constructor(ctx, initialGrid, tileSize, rows, cols) {
    this.ctx = ctx;
    this.initialGrid = initialGrid;
    this.tileSize = tileSize;
    this.rows = rows;
    this.cols = cols;
    this.grid = [];
  }

  reset() {
    this.grid = this.initialGrid.map(row => row.slice());
  }

  countFood() {
    let count = 0;
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        if (this.grid[r][c] === 2) count++;
      }
    }
    return count;
  }

  canMove(x, y, width, height) {
    const leftCol = Math.floor(x / this.tileSize);
    const rightCol = Math.floor((x + width - 1) / this.tileSize);
    const topRow = Math.floor(y / this.tileSize);
    const bottomRow = Math.floor((y + height - 1) / this.tileSize);

    if (
      leftCol < 0 ||
      rightCol >= this.cols ||
      topRow < 0 ||
      bottomRow >= this.rows
    ) return false;

    for (let r = topRow; r <= bottomRow; r++) {
      for (let c = leftCol; c <= rightCol; c++) {
        if (this.grid[r][c] === 1) return false;
      }
    }

    return true;
  }

  draw() {
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        const x = c * this.tileSize;
        const y = r * this.tileSize;

        switch (this.grid[r][c]) {
          case 0:
            this.ctx.fillStyle = "#000";
            this.ctx.fillRect(x, y, this.tileSize, this.tileSize);
            break;
          case 1:
            this.ctx.fillStyle = "#0000ff";
            this.ctx.fillRect(x, y, this.tileSize, this.tileSize);
            break;
          case 2:
            this.ctx.fillStyle = "#ffff00";
            this.ctx.beginPath();
            this.ctx.arc(
              x + this.tileSize / 2,
              y + this.tileSize / 2,
              this.tileSize / 6,
              0,
              Math.PI * 2
            );
            this.ctx.fill();
            break;
        }
      }
    }
  }
}
