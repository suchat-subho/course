document.addEventListener('DOMContentLoaded', function () {

    const notesContainer = document.getElementById('notes-container');
    const sideNav = document.getElementById('sidenav');

    fetch(webAppURL)
        .then(response => {
            if (!response.ok) {
                throw new Error('Unable to access JSON');
            }
            return response.json();
        })
        .then(data => {
            const URI = window.location.href;

            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                    const noteData = data[key];

                    const note = document.createElement('div');
                    note.className = 'note';

                    const shortURI = URI + "?url=" + noteData.ShortURL;

                    const comment = (!noteData.Comment || noteData.Comment.length === 0)
                        ? ""
                        : `<div class="green-box"><p><strong>Note:</strong> ${noteData.Comment}</p></div>`;

                    note.innerHTML = `
                        <h3>${noteData.Description}</h3>
                        <p><strong>Actual URL:</strong> <em>${noteData.URL}</em></p>
                        <p><strong>Short URL:</strong> <em>${shortURI}</em></p>
                        <p><a href="${shortURI}" target="_blank" class="button">Go to Short URL</a></p>
                        ${comment}
                    `;

                    notesContainer.appendChild(note);
                }
            }

            /* ✅ HIDE LOADER AFTER CONTENT IS READY */
            if (typeof hideLoader === "function") {
                hideLoader();
            }
        })
        .catch(error => {
            console.error(error.message);

            /* Hide loader even on failure */
            if (typeof hideLoader === "function") {
                hideLoader();
            }
        });
});

window.addEventListener("load", () => {
    if (typeof hideLoader === "function") {
        hideLoader();
    }
});