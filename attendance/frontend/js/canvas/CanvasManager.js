import ImageLoader from "./ImageLoader.js";
import Renderer from "./Renderer.js";
import Viewport from "./Viewport.js";

export default class CanvasManager {

    constructor(canvas) {

        this.canvas = canvas;
        this.ctx = canvas.getContext("2d");

        this.viewport = new Viewport(canvas);
        this.renderer = new Renderer(canvas, this.ctx, this.viewport);

        this.image = null;

        this.resize();

        window.addEventListener("resize", () => this.resize());
    }

    resize() {

        const parent = this.canvas.parentElement;

        this.canvas.width = parent.clientWidth;
        this.canvas.height = parent.clientHeight;

        if (this.image) {
            this.viewport.fit(this.image);
            this.renderer.draw(this.image);
        }
    }

    async load(url) {

        this.image = await ImageLoader.load(url);

        this.viewport.fit(this.image);

        this.renderer.draw(this.image);
    }
}
