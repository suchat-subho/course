/******************************************************************************
 * sidebar.js
 *
 * Sidebar UI for browsing classroom images.
 ******************************************************************************/

import { state } from "../state.js";

const imageList = document.getElementById("imageList");
const searchBox = document.getElementById("searchBox");

/**
 * Render sidebar.
 * @param {Function} onSelect Callback when an image is selected.
 */
export function renderSidebar(onSelect) {

    if (!imageList) return;

    imageList.innerHTML = "";

    state.images.forEach((image, index) => {

        const li = document.createElement("li");

        li.className = "image-item";

        if (index === state.currentIndex) {
            li.classList.add("selected");
        }

        li.dataset.index = index;
        li.dataset.filename = image.filename;

        li.innerHTML = `
            <div class="filename">${image.filename}</div>
            <div class="meta">
                <span>${image.class}</span>
                <span class="badge ${statusClass(image.status)}">
                    ${image.status}
                </span>
            </div>
        `;

        li.addEventListener("click", () => {
            onSelect(index);
        });

        imageList.appendChild(li);
    });

    enableSearch(onSelect);
}

/**
 * Filter sidebar images.
 */
function enableSearch(onSelect) {

    if (!searchBox) return;

    searchBox.oninput = () => {

        const keyword = searchBox.value.trim().toLowerCase();

        imageList.innerHTML = "";

        state.images.forEach((image, index) => {

            const text =
                `${image.filename} ${image.class} ${image.date}`.toLowerCase();

            if (!text.includes(keyword))
                return;

            const li = document.createElement("li");

            li.className = "image-item";

            if (index === state.currentIndex)
                li.classList.add("selected");

            li.innerHTML = `
                <div class="filename">${image.filename}</div>
                <div class="meta">
                    <span>${image.class}</span>
                    <span class="badge ${statusClass(image.status)}">
                        ${image.status}
                    </span>
                </div>
            `;

            li.addEventListener("click", () => {
                onSelect(index);
            });

            imageList.appendChild(li);

        });

    };

}

/**
 * Convert status into CSS class.
 */
function statusClass(status) {

    switch (status) {

        case "Completed":
            return "done";

        case "Review":
            return "review";

        default:
            return "pending";

    }

}
