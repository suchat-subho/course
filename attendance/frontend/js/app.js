import * as API from "./api.js";
import { state } from "./state.js";
import { renderSidebar } from "./ui/sidebar.js";
import CanvasManager from "./canvas/CanvasManager.js";

let canvasManager;

window.addEventListener("DOMContentLoaded", async () => {

    await API.initialize();

    canvasManager = new CanvasManager(
        document.getElementById("annotationCanvas")
    );

    renderSidebar(selectImage);

    if (state.images.length > 0) {
        selectImage(0);
    }
});

async function selectImage(index) {

    state.currentIndex = index;

    renderSidebar(selectImage);

    const image = state.images[index];

    document.getElementById("imageInfo").textContent =
        `${image.filename} | ${image.class} | ${image.date} | Students: ${image.count}`;

    await canvasManager.load(
        API.getImageURL(image.filename)
    );
}
