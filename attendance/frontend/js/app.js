/******************************************************************************
 * app.js
 ******************************************************************************/

import * as API from "./api.js";
import { state } from "./state.js";
import { renderSidebar } from "./ui/sidebar.js";
import CanvasManager from "./canvas/CanvasManager.js";

let canvasManager;

window.addEventListener("DOMContentLoaded", initialize);

async function initialize() {
    try {
        await API.initialize();

        canvasManager = new CanvasManager(
            document.getElementById("annotationCanvas")
        );

        bindEvents();

        renderSidebar(selectImage);

        if (state.images.length > 0) {
            await selectImage(0);
        }

    } catch (err) {
        console.error(err);
        alert("Failed to initialize the application.");
    }
}

function bindEvents() {

    document.getElementById("fitBtn")
        ?.addEventListener("click", () => canvasManager.fit());

    document.getElementById("previousBtn")
        ?.addEventListener("click", previousImage);

    document.getElementById("nextBtn")
        ?.addEventListener("click", nextImage);

    document.getElementById("saveBtn")
        ?.addEventListener("click", saveAnnotations);
}

async function selectImage(index) {

    if (index < 0 || index >= state.images.length)
        return;

    state.currentIndex = index;

    renderSidebar(selectImage);

    const image = state.images[index];

    updateImageInfo(image);

    await canvasManager.load(
        API.getImageURL(image.filename)
    );
}

function updateImageInfo(image) {

    document.getElementById("imageInfo").textContent =
        `${image.filename} | ${image.class} | ${image.date} | Students: ${image.count} | ${image.status}`;
}

function previousImage() {

    if (state.currentIndex > 0)
        selectImage(state.currentIndex - 1);
}

function nextImage() {

    if (state.currentIndex < state.images.length - 1)
        selectImage(state.currentIndex + 1);
}

function saveAnnotations() {

    console.log("Save annotations (not implemented yet)");
}
