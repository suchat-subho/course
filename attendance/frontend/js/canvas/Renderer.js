export default class Renderer {

    constructor(canvas, ctx, viewport) {

        this.canvas = canvas;
        this.ctx = ctx;
        this.viewport = viewport;

    }

    draw(image) {

        const ctx = this.ctx;

        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        ctx.drawImage(
            image,
            this.viewport.offsetX,
            this.viewport.offsetY,
            image.width * this.viewport.scale,
            image.height * this.viewport.scale
        );

    }

}
