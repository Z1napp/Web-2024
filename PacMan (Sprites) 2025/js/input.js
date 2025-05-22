export default class InputHandler {
  constructor() {
    this.keys = {};

    window.addEventListener("keydown", (e) => {
      this.keys[e.key] = true;
      e.preventDefault();
    });

    window.addEventListener("keyup", (e) => {
      this.keys[e.key] = false;
      e.preventDefault();
    });
  }

  reset() {
    this.keys = {};
  }
}
