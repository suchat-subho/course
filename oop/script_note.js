document.addEventListener('DOMContentLoaded', function() {
    const notesContainer = document.getElementById('notes-container');
    const sideNav = document.getElementById('sidenav');
    //alert(webAppURL);
    fetch(webAppURL)
        .then(response => {
            if (!response.ok) {
                throw new Error('Unable to access JSON');
            }
            document.getElementById('loading').style.display = 'none';
            return response.json();
        })
        .then(data => {
            URI = window.location.href;
            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                    const noteData = data[key];
                    const note = document.createElement('div');
                    note.className = 'note';
                    //note.id="${noteData.ShortURL}"
                    //console.log("noteData:" + Object.keys(noteData)); // View all properties of the object
                    shortURI = URI + "?url=" + noteData.ShortURL;
                    let comment = !noteData.Comment || noteData.Comment.length === 0
                                 ? "" : `<div class="green-box"><p><strong>Note:</strong> ${noteData.Comment}</p></div>`;
                    
                    let ticker_new = !noteData.tag || noteData.tag.length === 0 ? "" : noteData.tag.includes("new") ? `<img src="../icon/new.gif" alt="New" style="width: 20px; height: auto;">`: ``;
                    console.log("new-important:"+noteData.tag);
                    let ticker_imp = !noteData.tag || noteData.tag.length === 0 ? "" : noteData.tag.includes("imp") ? `<img src="../icon/imp.gif" alt="Important " style="width: 20px; height: auto;">`: ``;
                    note.innerHTML = `
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                            <h3 style="margin: 0;">${noteData.Description}</h3>
                            <span>${ticker_new}</span>
                            <span>${ticker_imp}</span>
                        </div> 
                        <p><strong>Actual URL:</strong> <em>${noteData.URL}</em></p>
                        <p><strong>Short URL:</strong> <em>${shortURI}</em></p>
                        <p><a href="${shortURI}" target="_blank" class="button">Go to Short URL</a></p>
                        ${comment}
                    `;
                    notesContainer.appendChild(note);
                    //const nav = document.createElement('li');
                    //nav.innerHTML=`<li><a href="#${noteData.ShortURL}">${noteData.Description}</a></li>`;
                    //sidenav.appendChild(nav);
                }
            }
        })
        .catch(error => {
            console.log(error.message);
        });
});
