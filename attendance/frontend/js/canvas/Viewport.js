export default class Viewport {

    constructor(canvas) {

        this.canvas = canvas;

        this.scale = 1;
        this.offsetX = 0;
        this.offsetY = 0;

    }

    fit(image) {

        const sx = this.canvas.width / image.width;
        const sy = this.canvas.height / image.height;

        this.scale = Math.min(sx, sy);

        this.offsetX =
            (this.canvas.width - image.width * this.scale) / 2;

        this.offsetY =
            (this.canvas.height - image.height * this.scale) / 2;

    }

}
